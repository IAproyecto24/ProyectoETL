# ProyectoETL
Proyecto de ETL, Maestria en Inteligencia Artificial y Ciencia de Datos (UAO)

# 📊 Proyecto ETL: Estadística Delictiva vs. Percepción de Inseguridad en Colombia

Este proyecto realiza un proceso completo de **Extracción, Transformación y Carga (ETL)** de datos de criminalidad a partir de la web oficial de la **Policía Nacional de Colombia**, con el objetivo de realizar un análisis comparativo con la **percepción de inseguridad de los ciudadanos colombianos**.

> Trabajo desarrollado como parte de la asignatura **ETL** en la **Universidad Autónoma de Occidente (UAO)**.

---

## 📌 Objetivo

El objetivo principal de este proyecto es diseñar y ejecutar un flujo de ETL que permita:
- Extraer información criminal pública desde la web oficial de la Policía Nacional.
- Transformar y estructurar los datos para su análisis estadístico.
- Contrastar los datos objetivos (estadísticas delictivas) con la percepción subjetiva de inseguridad de los colombianos.

---

## 🧠 Motivación

En Colombia, existe una constante discusión sobre si la percepción de inseguridad está alineada con los datos reales de criminalidad. Este proyecto busca ofrecer una herramienta técnica para estudiar esta relación mediante procesos automatizados de captura y procesamiento de datos.

---

## 🛠️ Tecnologías Utilizadas

- 🐍 **Python** (Scraping y ETL)
- 📦 **Pandas**, **BeautifulSoup**, **Requests**
- 💾 **SQLite / CSV / Excel** como destinos de carga
- 📈 **R / RStudio** para análisis estadístico y visualización (en etapa de análisis)
- 📊 Fuentes complementarias: **DANE**, **Encuesta de Percepción Ciudadana**

---

## 🔁 Flujo del Proceso ETL

1. **Extracción**  
   Se realiza scraping de los reportes públicos de delitos disponibles en la página oficial de la Policía Nacional.

2. **Transformación**  
   - Limpieza de datos (remoción de caracteres especiales, nulos, formatos de fecha)
   - Unificación de columnas y estandarización de variables
   - Generación de campos derivados

3. **Carga**  
   Los datos transformados se cargan en archivos CSV o bases de datos locales para posterior análisis.

👨‍💻 Autores
Este proyecto fue desarrollado por estudiantes de la Universidad Autónoma de Occidente (UAO):

🎓 Oscar Fernando Pulgarín Molina

🎓 Juan David Díaz Calero

🎓 Sebastián Urquijo Buitrago

