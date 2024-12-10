from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
import os

# Configuración de la base de datos para PostgreSQL
DB_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/efacture"

# Crear la conexión a la base de datos
engine = create_engine(DB_URL)
metadata = MetaData()
# metadata.reflect(bind=engine)  # Refleja todas las tablas de la base de datos
metadata.reflect(bind=engine, schema='efacture_repo')
Base = declarative_base()

# Carpeta donde guardar los modelos generados
OUTPUT_FOLDER = "Models"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Mapeo de tipos de datos SQL a Python/SQLAlchemy
SQL_TO_PYTHON = {
    "INTEGER": "Integer",
    "BIGINT": "BigInteger",
    "VARCHAR": "String",
    "TEXT": "Text",
    "DATE": "Date",
    "TIMESTAMP": "DateTime",
    "FLOAT": "Float",
    "BOOLEAN": "Boolean",
    "DECIMAL": "Numeric",
    "JSONB": "JSON",
    "UUID": "String",  # Cambiar si usas una librería para UUID
    "SERIAL": "Integer",
}

# Función para generar modelos
def generate_model(table_name_capitalized, table_name, columns):
    class_lines = [f"class {table_name_capitalized}(Base):"]
    class_lines.append(f"    __tablename__ = '{table_name}'")
    for column in columns:
        column_name = column.name
        column_type = str(column.type).upper()
        sqlalchemy_type = SQL_TO_PYTHON.get(column_type.split("(")[0], "String")  # Default: String
        column_args = []
        if column.primary_key:
            column_args.append("primary_key=True")
        if column.nullable is False:
            column_args.append("nullable=False")
        if column.unique:
            column_args.append("unique=True")
        args_str = ", ".join(column_args)
        class_lines.append(f"    {column_name} = Column({sqlalchemy_type}, {args_str})")
    return "\n".join(class_lines)

# Recorrer todas las tablas y generar modelos
for table_name, table in metadata.tables.items():
    table_name_aux = table_name.replace("efacture_repo.", "")
    partes_mayus = [parte.capitalize() for parte in table_name_aux.split('_')]
    table_name_capitalized = "".join(partes_mayus)

    print(f"Generando modelo para la tabla: {table_name_capitalized}")
    columns = table.columns

    model_code = generate_model(table_name_capitalized, table_name, columns)
    model_code = f"from sqlalchemy import Column, Integer, String, Date, Float, Text, Boolean, DateTime, Numeric, JSON\nfrom sqlalchemy.ext.declarative import declarative_base\n\nBase = declarative_base()\n\n{model_code}"
    
    # Guardar en archivo
    model_file = os.path.join(OUTPUT_FOLDER, f"{table_name_capitalized}.py")
    with open(model_file, "w", encoding="utf-8") as file:
        file.write(model_code)

print(f"Modelos generados en la carpeta: {OUTPUT_FOLDER}")
