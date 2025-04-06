import pandas as pd
import glob
import os

# Ruta de la carpeta origen de los archivos Excel
ruta_origen = r"C:\Users\djseb\Desktop\Delitos Policia\Violencia Intrafamiliar"

# Nombre de la carpeta de origen (para nombrar el CSV)
nombre_carpeta = os.path.basename(ruta_origen)

# Ruta de los archivos Excel
ruta_archivos = os.path.join(ruta_origen, "*.xlsx")

# Ruta de la carpeta destino
ruta_destino = r"C:\Users\djseb\Desktop\Delitos Policia\CSV Extraidos"

# Asegurar que la carpeta destino exista
os.makedirs(ruta_destino, exist_ok=True)

# Lista para almacenar los DataFrames
dataframes = []

# Leer todos los archivos Excel en la carpeta
for archivo in glob.glob(ruta_archivos):
    # Cargar todas las hojas del archivo en un diccionario de DataFrames
    xls = pd.ExcelFile(archivo)
    
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet, skiprows=0)  # Asegura que no salte filas

        if not df.empty:
            # Eliminar columnas completamente vacías
            df = df.dropna(how='all', axis=1)

            if not df.empty:
                # Determinar la última columna con datos
                ultima_columna = df.columns[-1]

                # Eliminar filas donde la última columna sea NaN
                df = df.dropna(subset=[ultima_columna])

                # Agregar al conjunto de datos
                dataframes.append(df)

# Unir todos los DataFrames en uno solo
df_final = pd.concat(dataframes, ignore_index=True)

# Nombre del archivo CSV
nombre_csv = f"{nombre_carpeta}.csv"
ruta_csv = os.path.join(ruta_destino, nombre_csv)

# Guardar el DataFrame en un archivo CSV
df_final.to_csv(ruta_csv, index=False, encoding="utf-8")

print(f"Proceso finalizado. Archivo CSV generado: {ruta_csv}")
