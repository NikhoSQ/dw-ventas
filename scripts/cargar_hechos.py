import pandas as pd
from sqlalchemy import create_engine

# 1. Conexión a la base de datos
engine = create_engine("postgresql://postgres:admin123@localhost:5432/dw_ventas")

# 2. Leer el CSV original otra vez
df = pd.read_csv("datos_crudos/Sample_ Superstore.csv", encoding="latin1")
df['Order Date'] = pd.to_datetime(df['Order Date'], format="mixed")

# 3. Leer las dimensiones YA CARGADAS en la base de datos (con sus IDs)
dim_tiempo = pd.read_sql("SELECT id_tiempo, fecha FROM dim_tiempo", engine)
dim_tiempo = pd.read_sql("SELECT id_tiempo, fecha FROM dim_tiempo", engine)
dim_tiempo['fecha'] = pd.to_datetime(dim_tiempo['fecha'])
dim_producto = pd.read_sql("SELECT id_producto, nombre_producto, categoria, subcategoria FROM dim_producto", engine)
dim_cliente = pd.read_sql("SELECT id_cliente, nombre_cliente, segmento FROM dim_cliente", engine)
dim_region = pd.read_sql("SELECT id_region, region, pais FROM dim_region", engine)

# 4. Cruzar (merge) el CSV original con cada dimensión para obtener sus IDs

# Cruce con Tiempo
df = df.merge(dim_tiempo, left_on='Order Date', right_on='fecha', how='left')

# Cruce con Producto
df = df.merge(
    dim_producto,
    left_on=['Product Name', 'Category', 'Sub-Category'],
    right_on=['nombre_producto', 'categoria', 'subcategoria'],
    how='left'
)

# Cruce con Cliente (recuerda: usamos Customer ID como nombre_cliente)
df = df.merge(
    dim_cliente,
    left_on=['Customer ID', 'Segment'],
    right_on=['nombre_cliente', 'segmento'],
    how='left'
)

# Cruce con Región
df = df.merge(
    dim_region,
    left_on=['Region', 'Country'],
    right_on=['region', 'pais'],
    how='left'
)

# 5. Armar la tabla de hechos final con los nombres de columna correctos
fact_ventas = df[['id_tiempo', 'id_producto', 'id_cliente', 'id_region', 'Quantity', 'Sales', 'Profit']].copy()
fact_ventas.columns = ['id_tiempo', 'id_producto', 'id_cliente', 'id_region', 'cantidad', 'monto_venta', 'ganancia']

# 6. Verificar que no haya IDs vacíos (nulos) antes de cargar
print("Filas totales:", len(fact_ventas))
print("Filas con algún ID nulo:", fact_ventas.isnull().any(axis=1).sum())

# 7. Cargar a PostgreSQL
fact_ventas.to_sql('fact_ventas', engine, if_exists='append', index=False)

print("¡Tabla de hechos cargada con éxito!")