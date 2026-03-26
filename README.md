# 📅 ETL Dimensión Calendario y Feriados (Chile) / Calendar Dimension & Holidays ETL (Chile)

🇪🇸 **[ESPAÑOL]**

Este proyecto es un pipeline **ETL (Extracción, Transformación y Carga)** automatizado, construido con Python y SQL Server. Su objetivo es mantener actualizada una Dimensión de Calendario para modelos de Business Intelligence, cruzando los días del año con los feriados oficiales de Chile extraídos desde una API externa.

### 🚀 Arquitectura y Flujo de Datos
1. **Extracción (API):** Consumo de la API de Boostr (`api.boostr.cl`) mediante la librería `requests` de Python para obtener los feriados del año.
2. **Transformación:** Limpieza y parseo del formato JSON, validación de campos y estandarización de variables booleanas (feriados irrenunciables).
3. **Carga (SQL Server):** Inserción de los registros en la base de datos a través de `pyodbc` utilizando consultas parametrizadas para mayor seguridad e integridad.
4. **Orquestación:** Ejecución automática de un Procedimiento Almacenado (`usp_ETLCargaCalendarioAnual`) que genera mediante un CTE recursivo todos los días del año, cruza los feriados cargados y calcula variables analíticas clave (Días hábiles, Fines de semana, Número de semana ISO).

### 🛠️ Tecnologías Utilizadas

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQL Server](https://img.shields.io/badge/Microsoft%20SQL%20Server-CC2927?style=for-the-badge&logo=microsoft-sql-server&logoColor=white)
![Power Automate](https://img.shields.io/badge/Power%20Automate-0066FF?style=for-the-badge&logo=power-automate&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=power-bi&logoColor=black)

* **Lenguaje:** Python 3.14
* **Librerías:** `requests`, `pyodbc`
* **Base de Datos:** SQL Server 2019 Standard Edition
* **Conceptos:** Modelado Dimensional (Star Schema), REST APIs, CTEs Recursivos.

---

🇬🇧 **[ENGLISH]**

This project is an automated **ETL (Extract, Transform, Load)** pipeline built with Python and SQL Server. Its purpose is to maintain an updated Calendar Dimension (Date Dimension) for Business Intelligence models, cross-referencing all days of the year with official Chilean holidays fetched from an external API.

### 🚀 Architecture & Data Flow
1. **Extraction (API):** Consuming the Boostr API (`api.boostr.cl`) using Python's `requests` library to fetch the year's holidays.
2. **Transformation:** JSON parsing and cleansing, field validation, and standardization of boolean variables (mandatory vs. regular holidays).
3. **Loading (SQL Server):** Inserting records into the database via `pyodbc` using parameterized queries for enhanced security and data integrity.
4. **Orchestration:** Automated execution of a Stored Procedure (`usp_ETLCargaCalendarioAnual`) that uses a recursive CTE to generate all days of the year, joins the loaded holidays, and calculates key analytical variables (Business days, Weekends, ISO Week numbers).

### 🛠️ Tech Stack & Tools

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQL Server](https://img.shields.io/badge/Microsoft%20SQL%20Server-CC2927?style=for-the-badge&logo=microsoft-sql-server&logoColor=white)
![Power Automate](https://img.shields.io/badge/Power%20Automate-0066FF?style=for-the-badge&logo=power-automate&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=power-bi&logoColor=black)

* **Language:** Python 3.14
* **Libraries:** `requests`, `pyodbc`
* **Database:** SQL Server 2019 Standard Edition
* **Concepts:** Dimensional Modeling (Star Schema), REST APIs, Recursive CTEs.

---

### 📂 Archivos del Proyecto / Project Files
* `CargaFeriadosPython.py`: Script principal de extracción y carga / *Main extraction and loading script*.
* `usp_ETLCargaCalendarioAnual.sql`: Procedimiento almacenado para la generación de la dimensión / *Stored procedure for dimension generation*.
