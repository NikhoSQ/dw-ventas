import pandas as pd
from sqlalchemy import create_engine

# 1. EXTRAER: leer el CSV
df = pd.read_csv("datos_crudos/Sample_ Superstore.csv", encoding="latin1")
#print(df.columns.tolist())
# 2. TRANSFORMAR: limpiar y preparar los datos
df['Order Date'] = pd.to_datetime(df['Order Date'], format="mixed")

# --- Dimensión Tiempo ---
dim_tiempo = df[['Order Date']].drop_duplicates().rename(columns={'Order Date': 'fecha'})
dim_tiempo['anio'] = dim_tiempo['fecha'].dt.year
dim_tiempo['mes'] = dim_tiempo['fecha'].dt.month
dim_tiempo['nombre_mes'] = dim_tiempo['fecha'].dt.strftime('%B')
dim_tiempo['trimestre'] = dim_tiempo['fecha'].dt.quarter
dim_tiempo['dia_semana'] = dim_tiempo['fecha'].dt.strftime('%A')

# --- Dimensión Producto ---
dim_producto = df[['Product Name', 'Category', 'Sub-Category']].drop_duplicates()
dim_producto.columns = ['nombre_producto', 'categoria', 'subcategoria']

# --- Dimensión Cliente ---
dim_cliente = df[['Customer ID', 'Segment']].drop_duplicates()
dim_cliente.columns = ['nombre_cliente', 'segmento']

# --- Dimensión Región ---
dim_region = df[['Region', 'Country']].drop_duplicates()
dim_region.columns = ['region', 'pais']

# 3. CARGAR: conectar a PostgreSQL
# Reemplaza 'admin123' por la contraseña que pusiste al instalar PostgreSQL
engine = create_engine("postgresql://postgres:admin123@localhost:5432/dw_ventas")

# Cargar dimensiones primero
dim_tiempo.to_sql('dim_tiempo', engine, if_exists='append', index=False)
dim_producto.to_sql('dim_producto', engine, if_exists='append', index=False)
dim_cliente.to_sql('dim_cliente', engine, if_exists='append', index=False)
dim_region.to_sql('dim_region', engine, if_exists='append', index=False)

print("¡Dimensiones cargadas con éxito!")