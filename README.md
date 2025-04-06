# ProyectoETL
Proyecto de ETL, Maestria en Inteligencia Artificial y Ciencia de Datos (UAO)

# 🔍 Análisis ETL para la Integración de Datos en Criminalidad, Resultados Operativos y Percepción Ciudadana en Colombia (2018–2024)

Este proyecto propone la implementación de un proceso completo de **ETL (Extracción, Transformación y Carga)** orientado a la integración de datos provenientes de múltiples fuentes oficiales y públicas sobre:

- Criminalidad en Colombia,
- Resultados operativos de la Policía Nacional y la Fiscalía General,
- Percepción ciudadana sobre la seguridad en el país.

> Proyecto académico desarrollado en el marco de la asignatura **ETL** en la **Universidad Autónoma de Occidente (UAO)**.

---

## 📌 Resumen

Entre los años 2018 y 2024, Colombia ha enfrentado desafíos en materia de seguridad y percepción ciudadana. Este trabajo busca unificar información dispersa a través de un flujo ETL robusto, permitiendo:

- Consolidar datos oficiales y públicos relacionados con delitos, capturas, operativos, etc.
- Contrastar estos datos con la percepción de inseguridad ciudadana.
- Facilitar análisis posteriores para entender las brechas entre la realidad objetiva y la percepción subjetiva de la seguridad.

---

## 🎯 Objetivos

- Implementar un flujo automatizado de ETL para criminalidad y percepción ciudadana en Colombia.
- Integrar datos provenientes de la Policía Nacional, Fiscalía General, encuestas y observatorios de seguridad.
- Estandarizar y validar los datos para análisis posteriores.
- Establecer las bases para un análisis comparativo entre realidad delictiva y percepción de inseguridad.

---

## 🧰 Tecnologías y Herramientas

- **Lenguaje:** Python 3.x
- **Librerías:** `pandas`, `beautifulsoup4`, `requests`, `openpyxl`
- **Base de datos:** CSV / SQLite
- **Visualización y análisis:** R / RStudio, `ggplot2`, `dplyr`
- **Otras herramientas:** Git, GitHub, Jupyter Notebooks

---

## 🔁 Proceso ETL

1. **Extracción de Datos**
   - Datos delictivos y operativos desde portales web oficiales (Policía Nacional, Fiscalía).
   - Encuestas de percepción ciudadana (DANE, Observatorios).
   - Informes de transparencia y observatorios civiles.

2. **Transformación**
   - Limpieza de inconsistencias y nulos.
   - Unificación de formatos de fechas, nombres y categorías delictivas.
   - Cruce y alineación temporal de las fuentes.

3. **Carga**
   - Almacenamiento en archivos estructurados (CSV) o base de datos SQLite.
   - Preparación para análisis exploratorio en R y generación de reportes.

👨‍💻 Autores
Este proyecto fue desarrollado por estudiantes de la Universidad Autónoma de Occidente (UAO):

🎓 Oscar Fernando Pulgarín Molina

🎓 Juan David Díaz Calero

🎓 Sebastián Urquijo Buitrago

