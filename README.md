# Data Warehouse de Análisis de Ventas

Proyecto personal de inteligencia de negocios: diseño e implementación de un data warehouse completo, desde el modelado de datos hasta la visualización final, usando el dataset público "Sample Superstore".

## Objetivo
Responder la pregunta de negocio: ¿qué productos, categorías y regiones generan más ventas y ganancia?

## Tecnologías usadas
- **PostgreSQL** — modelado dimensional (esquema estrella)
- **Python (pandas, SQLAlchemy)** — proceso ETL (extracción, transformación y carga)
- **Power BI** — dashboard interactivo con KPIs y segmentadores

## Arquitectura
Se diseñó un esquema estrella con 4 dimensiones (`dim_tiempo`, `dim_producto`, `dim_cliente`, `dim_region`) y una tabla de hechos (`fact_ventas`), cargando cerca de 10,000 registros de ventas.

## Contenido del repositorio
- `scripts/` — scripts de Python para el proceso ETL (carga de dimensiones y hechos)
- `datos_crudos/` — dataset original (CSV)
- `Datawerehouse-verntas.pbix` — archivo de Power BI con el dashboard final

## Dashboard
El dashboard incluye:
- KPIs generales (ventas totales, ganancia total, número de ventas)
- Ventas por categoría de producto
- Ventas y ganancia por región
- Tendencia de ventas en el tiempo
- Filtros interactivos por categoría y región

## Principales hallazgos
Las regiones West y East generan más ventas, pero la proporción de ganancia frente a venta es más baja de lo esperado en todas las regiones — una señal de posible oportunidad de mejora en precios o costos.

## Qué aprendí
Este fue mi primer proyecto de punta a punta en el área de datos: modelado dimensional, construcción de un pipeline ETL real (incluyendo depuración de errores de formato de fechas y cruces de datos), y diseño de un dashboard orientado a negocio.
