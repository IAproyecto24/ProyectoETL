# ProyectoETL

Proyecto de ETL, Maestría en Inteligencia Artificial y Ciencia de Datos (UAO)

# 👨‍💻 Autores

Este proyecto fue desarrollado por estudiantes de la Maestría en Inteligencia Artificial y Ciencia de Datos de la Universidad Autónoma de Occidente (UAO):

🎓 Oscar Fernando Pulgarín Molina

🎓 Juan David Díaz Calero

🎓 Sebastián Urquijo Buitrago

🎓 Miguel Mauricio Meza

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
- **Librerías:** `pandas`, `beautifulsoup4`, `requests`, `openpyxl`, `firebase-admin`, , `firebase-functions`, `google-cloud-storage`, `openpyxl`, `python-dateutil`, `xlrd`, `numpy`
- **Base de datos:** CSV / firestore
- **Visualización y análisis:** R / RStudio, `ggplot2`, `dplyr`
- **Otras herramientas:** Git, GitHub, Jupyter Notebooks, firebase cloud functions, firestore, firebase hosting

---

## 🔗 Fuentes de Datos

Los datos extraídos y utilizados en este proyecto provienen de las siguientes fuentes oficiales:

- 📁 [Archivos de la Fiscalía General de la Nación (Google Drive)](https://drive.google.com/drive/folders/1-9mURIly6WvBtGJfe7vRjvEHwFfE5gWs)
- 🌐 [Estadística Delictiva - Policía Nacional de Colombia (Web Oficial)](https://www.policia.gov.co/estadistica-delictiva?page=1)
- 📁 [Archivos XLSX y CSV extraídos (Google Drive)](https://drive.google.com/drive/u/3/folders/180HfeUy5t6mAdlSFa-QZ1vqhzvLDfROp)

---

## 🔁 Proceso ETL

1. **Extracción de Datos**

   - Scraping de estadísticas delictivas desde la web de la [Policía Nacional](https://www.policia.gov.co/estadistica-delictiva?page=1).
   - Descarga y consolidación de archivos de la [Fiscalía General](https://drive.google.com/drive/folders/1-9mURIly6WvBtGJfe7vRjvEHwFfE5gWs).
   - Recolección de archivos estructurados en [XLSX y CSV](https://drive.google.com/drive/u/3/folders/180HfeUy5t6mAdlSFa-QZ1vqhzvLDfROp).

2. **Transformación**

   - Limpieza de inconsistencias y nulos.
   - Estandarización de formatos de fechas, nombres y categorías delictivas.
   - Validación y unificación de estructura para análisis conjunto.

3. **Carga**
   - Almacenamiento de los datos procesados en formato CSV o base de datos SQLite.
   - Preparación para análisis en Visual Studio Code y generación de visualizaciones estadísticas en Power BI / VS Code.

_Inicialmente se ejecuto un proceso mas manual, con el uso de Python, Jupyter notebook y Power BI, donde se hizo la extracción y el EDA. Posteriormente se implemento un pipeline automatizado._

## 🔋 Pipeline (Automatizado) ETL

Proyecto de procesamiento automatizado de datos de seguridad (Policía y Fiscalía) usando Firebase Cloud Functions (Gen2). Extrae, transforma y carga datos desde archivos Excel a Firestore, generando insights para análisis comparativos y percepción ciudadana.

Este pipeline se activa cuando se almacenan los archivos con datos raw en la carpeta `raw/policia` y `raw/fiscalia` en un bucket de firebase hosting; se activa una `cloud function` (trigger) que inicia el proceso de extracción, ahi se estandarizan los datos a archivos csv, los cuales son almacenados en el bucket en la carpeta `extracted`, ahi se activa una `cloud function` (trigger) donde se transforman los datos y se almacenan en la BD de firebase, al crearse los documentos, se activa una `cloud function` (trigger) que detecta la creación de documentos y se encarga de hacer la carga en la tabla de hechos y tablas de dimensiones.

_Se tiene un sistema de logging de errores los cuales son almacenados en la BD en una colección llamada `logs`._

### **Propósito del Proyecto** 🎯

Automatizar la integración de datos de instituciones colombianas (Policía y Fiscalía) para:

- **Estandarizar** formatos de datos dispersos.
- **Comparar** registros entre instituciones.
- **Generar métricas** sobre incidentes de seguridad (ej: uso de artefactos explosivos).
- **Facilitar análisis** de percepción ciudadana mediante tablas estructuradas.

---

### **Características Clave** 🔑

- **Automatización ETL**:
  - **Extracción**: Detección de archivos en Firebase Storage (`raw/policia/`, `raw/fiscalia/`).
  - **Transformación**: Conversión de tipos de datos, separación de fechas, limpieza de valores nulos.
  - **Carga**: Almacenamiento en Firestore (`transformed/policia/`, `transformed/fiscalia/`).
- **Arquitectura Escalable**:

  - **Cloud Functions (Gen2)**: Ejecución serverless basada en triggers de Storage.
  - **Modelo Estrella**: Tablas de hechos (`hechos`) y dimensiones (`dim_tiempo`, `dim_ubicacion`, etc.) para análisis OLAP.

- **Manejo de Errores**:
  - **Logs Centralizados**: Registro de fallos en Firestore (`logs`).
  - **Soporte Multi-formato**: Compatibilidad con XLS, XLSX y CSV.

---

### **Diagrama de Arquitectura** 🏗️

```plaintext
┌───────────────────┐               ┌──────────────────────┐
│   Firebase        │               │    Cloud Functions   │
│   Storage         │               │       (Gen 2)        │
│                   │               │                      │
│  ┌─────────────┐  │   Trigger     │ ┌──────────────────┐ │
│  │ raw/        │  ├───────────────►│ on_raw_file_upload│ │
│  │  policia/   │  │               │ │ (Extract)        │ │
│  │  fiscalia/  │  │               │ └──────────────────┘ │
│  └─────────────┘  │               │                      │
│                   │               │                      │
│  ┌─────────────┐  │   Trigger     │ ┌───────────────────┐│
│  │ extracted/  │  ├───────────────►│ on_extracted_upload││
│  │  policia/   │  │               │ │ (Transform)       ││
│  │  fiscalia/  │  │               │ └───────────────────┘│
│  └─────────────┘  │               │                      │
└───────────────────┘               └───────────┬──────────┘
                                                │
                                                │ Trigger
                                                ▼
┌──────────────────────────────────────────────────────────┐
│                 Firestore                                │
│                                                          │
│  ┌──────────────────┐        ┌──────────────────────┐    │
│  │ transformed/     │        │ Tablas de Hechos     │    │
│  │  policia/        │        │ (hechos)             │    │
│  │  fiscalia/       ├───────►│  - Origen            │    │
│  └──────────────────┘        │  - Fecha             │    │
│                              │  - Código DANE       │    │
│  ┌──────────────────┐        └──────────────────────┘    │
│  │ logs/            │                                    │
│  │  - errores       │        ┌──────────────────────┐    │
│  └──────────────────┘        │ Dimensiones          │    │
│                              │ (dim_tiempo,         │    │
│                              │  dim_ubicacion,      │    │
│                              │  dim_armas)          │    │
│                              └──────────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

![Diagrama del Pipeline](/diagrama_pipeline.png)

### **Configuración** ⚙️

#### **Requisitos**

- **Cuenta de Firebase** con Storage y Firestore habilitados.
- **Python 3.10+** (compatible con Cloud Functions Gen2).
- **CLI de Firebase** instalado globalmente.

---

#### **Instalación**

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/IAproyecto24/ProyectoETL.git
   cd proyecto
   ```

---

#### **Instalar dependencias**:

```bash
pip install -r requirements.txt
```

#### **Despliegue**:

```bash
   firebase deploy --only functions
```

#### **Estructura del proyecto**:

```plaintext
pipeline/
├── extract/ # Lógica de extracción de datos
├── transform/ # Transformación y normalización
├── load/ # Carga a Firestore y tablas
├── utils/ # Configuración y logging
├── main.py # Punto de entrada de Cloud Functions
└── requirements.txt # Dependencias
```

---

## Uso 🚀

### Subir archivos origen a las carpetas en Firebase Storage:

- **Datos de Policía:** `raw/policia/[crimen]/archivo.xlsx`
- **Datos de Fiscalía:** `raw/fiscalia/[crimen]/archivo.xls`

### Procesamiento automático:

- Los archivos se convertirán a CSV en `extracted/`.
- Los datos transformados se guardarán en Firestore (`transformed/`).

### Consultar resultados:

- **Tablas de hechos:** Colección `hechos` en Firestore.
- **Tablas de dimensiones:** Colecciones `dim_tiempo`, `dim_ubicacion`, `dim_armas` en Firestore.
- **Logs:** Colección `logs` para depuración.

### Tecnologías Utilizadas 💻

- **Firebase:** Storage, Firestore, Cloud Functions (Gen2).
- **Python:** Pandas, Firebase Admin SDK.
- **Formats:** XLS/XLSX, CSV.
