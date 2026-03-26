import requests
import pyodbc
from datetime import datetime

def etl_feriados_calendario():
    # ==========================================
    # 1. CONFIGURACIÓN DE VARIABLES
    # ==========================================
    url_api = "https://api.boostr.cl/holidays/2025.json"
    anio_proceso = 2025    
    SERVIDOR = r'NBK-AV-MIBARRA\SQLEXPRESS'
    BASE_DE_DATOS = 'ESTUDIOSCOMERCIALES' 
    
    # Cadena de conexión usando Autenticación de Windows
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=LH-GESTIONDOS2;DATABASE=ESTUDIOSCOMERCIALES;Trusted_Connection=yes;'
    
    
    try:
        # ==========================================
        # 2. EXTRACCIÓN (Extraer datos de la API)
        # ==========================================
        print(f"1. Conectando a la API para el año {anio_proceso}...")
        respuesta = requests.get(url_api)
        respuesta.raise_for_status() # Si la página se encuentra caida 404 o 500 detiene el código
        datos_json = respuesta.json()
        
        if datos_json.get('status') != 'success':
            print("Error: La API no devolvió un estado de éxito.")
            return

        lista_feriados = datos_json.get('data', [])
        print(f"   -> ¡Éxito! Se encontraron {len(lista_feriados)} feriados.\n")

        # ==========================================
        # 3. CARGA (Insertar en SQL Server)
        # ==========================================
        print("2. Conectando a SQL Server...")
        conexion = pyodbc.connect(conn_str)
        cursor = conexion.cursor()
        print("   -> Conexión establecida.\n")

        print("3. Limpiando la tabla dbo.feriado (Truncate)...")
        cursor.execute("TRUNCATE TABLE dbo.feriado")
        
        print("4. Insertando nuevos registros...")
        #id_counter = 1
        
        # Consulta SQL preparada
        query_insert = """
            INSERT INTO dbo.feriado ( Fecha, Detalle, Irrenunciable, Activo)
            VALUES ( ?, ?, ?, ?)
        """
        
        for feriado in lista_feriados:
            fecha_str = feriado.get('date')
            titulo = feriado.get('title')
            
            # Truncamos a 60 caracteres por si acaso, tal como en tu tabla
            if titulo and len(titulo) > 60:
                titulo = titulo[:60]
                
            irrenunciable = 1 if feriado.get('inalienable') else 0
            activo = 1
            
            # Ejecutamos el insert fila por fila
            cursor.execute(query_insert, ( fecha_str, titulo, irrenunciable, activo))
           #id_counter += 1
            
        #print(f"   -> Se insertaron {id_counter - 1} feriados correctamente.\n")

        conexion.commit() # Guarda insert generados

        # ==========================================
        # 4. EJECUCIÓN DE PROCEDIMIENTO ALMACENADO
        # ==========================================
        print(f"5. Ejecutando SP usp_GenerarCalendario para el año {anio_proceso}...")
        query_sp = "EXEC dbo.usp_ETLCargaCalendarioAnual"
        cursor.execute(query_sp)
        print("   -> Procedimiento ejecutado con éxito.\n")


        
        # ==========================================
        # 5. CONFIRMAR CAMBIOS (COMMIT)
        # ==========================================
        conexion.commit()
        print("=== PROCESO ETL FINALIZADO CORRECTAMENTE ===")

    except pyodbc.Error as e:
        print(f"\n❌ Error de Base de Datos: {e}")
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error de API: {e}")
    except Exception as e:
        print(f"\n❌ Error General: {e}")
    finally:
        # Siempre cerramos la conexión pase lo que pase
        if 'conexion' in locals():
            conexion.close()

# Punto de entrada
if __name__ == "__main__":
    etl_feriados_calendario()