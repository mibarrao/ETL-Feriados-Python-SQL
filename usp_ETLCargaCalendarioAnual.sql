
-- ================================================
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<María Ibarra Orellana>
-- Create date: <25-03-2026>
-- Description:	<Generación automática para Calendario anual>
-- =============================================
ALTER PROCEDURE usp_ETLCargaCalendarioAnual
	
AS
BEGIN


DROP TABLE IF EXISTS dbo.calendario;

CREATE TABLE dbo.calendario (
    Fecha DATE PRIMARY KEY,
    DiaHabilDelMes INT,
	NumeroSemana INT, -- ¡Nueva columna agregada!
    NombreDia VARCHAR(20),
    
);

/***/


		-- 1. Configuramos el primer día de la semana como Lunes (1)
		SET DATEFIRST 1; 

		-- 2. Definimos el año que queremos generar
		DECLARE @Anio INT = 2025; -- Cambia esto al año que necesites
		DECLARE @FechaInicio DATE = DATEFROMPARTS(@Anio, 1, 1);
		DECLARE @FechaFin DATE = DATEFROMPARTS(@Anio, 12, 31);

		-- 3. CTE Recursivo para generar todas las fechas del año
		WITH GeneradorFechas AS (
			SELECT @FechaInicio AS Fecha
			UNION ALL
			SELECT DATEADD(DAY, 1, Fecha)
			FROM GeneradorFechas
			WHERE Fecha < @FechaFin
		),
		-- 4. CTE para cruzar con feriados y determinar qué tipo de día es


		ClasificadorDias AS (
			SELECT 
				gf.Fecha,
				YEAR(gf.Fecha) AS Anio,
				MONTH(gf.Fecha) AS Mes,
				DAY(gf.Fecha) AS Dia,
        
				-- Calculamos el número de semana bajo el estándar ISO
				DATEPART(ISO_WEEK, gf.Fecha) AS NumeroSemana,
        
				DATENAME(WEEKDAY, gf.Fecha) AS NombreDia,
        
				-- Si es Sábado (6) o Domingo (7), es fin de semana
				--CASE WHEN DATEPART(WEEKDAY, gf.Fecha) IN (6, 7) THEN 1 ELSE 0 END AS EsFinDeSemana,
				
				-- Si cruzó con la tabla feriados, es feriado
				CASE WHEN fer.Fecha IS NOT NULL THEN 1 ELSE 0 END AS EsFeriado,
        
				-- Es hábil SOLO si no es fin de semana y no es feriado
				CASE 
					WHEN DATEPART(WEEKDAY, gf.Fecha) IN (6, 7) THEN 0 
					WHEN fer.Fecha IS NOT NULL THEN 0 
					ELSE 1 
				END AS EsHabil
			FROM GeneradorFechas gf
			LEFT JOIN dbo.feriado fer 
				ON gf.Fecha = fer.Fecha AND fer.Activo = 1
		)
		-- 5. Insertamos el resultado final
		INSERT INTO dbo.calendario (Fecha, DiaHabilDelMes , NumeroSemana, NombreDia)
		SELECT 
			Fecha,
			 -- Calculamos el correlativo del día hábil
			CASE 
				WHEN EsHabil = 1 THEN 
					ROW_NUMBER() OVER (PARTITION BY Anio, Mes, EsHabil ORDER BY Fecha)
				ELSE 0 
			END AS DiaHabilDelMes,
			NumeroSemana,
			NombreDia
		FROM ClasificadorDias
		order by fecha 
		OPTION (MAXRECURSION 366);


END
GO
