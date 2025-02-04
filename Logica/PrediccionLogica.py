import pandas as pd
import numpy as nppip 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

from fastapi import Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from Persistencia.PersistenciaFacade import AccesoDatosFacade

class PrediccionLogica:
    def __init__(self):
        self.facade = AccesoDatosFacade()
    
    def generar_dataset(self, db : Session):
        dataset = self.facade.generar_dataset(db)
        try:
            dataset_entrenado = self.generar_prediccion(dataset, 12)
            self.facade.dataset_entrenado_insert(dataset_entrenado, db)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Ocurrion un error: {str(e)}") from e

        return JSONResponse(
                status_code=200,
                content={"message": "Se ha generado correctamente el entrenamiento y se han guardado los datos"}
            )

    def generar_prediccion(self, dataset, meses_futuros = 12):
        # Cargar el dataset
        data = pd.DataFrame(dataset)

        # Asegurar que la columna fecha sea del tipo datetime
        data['fecha'] = pd.to_datetime(data['fecha'])

        # Añadir columnas de Mes y Año
        data['mes'] = data['fecha'].dt.month
        data['anio'] = data['fecha'].dt.year

        # Codificar las columnas categóricas (usuario y categoria)
        le_usuario = LabelEncoder()
        le_categoria = LabelEncoder()

        data['Usuario_encoded'] = le_usuario.fit_transform(data['usuario'])
        data['Categoría_encoded'] = le_categoria.fit_transform(data['categoria'])

            
        # Ordenar por usuario, categoría y fecha
        data = data.sort_values(by=['usuario', 'categoria', 'fecha'])

        # Crear la columna "monto_mismo_mes_anterior" para capturar el gasto del mismo mes del año anterior
        data['monto_mismo_mes_anterior'] = data.groupby(['usuario', 'categoria', 'mes'])['monto'].shift(1)

        # Rellenar valores NaN con 0 (para los primeros registros sin historial)
        data['monto_mismo_mes_anterior'] = data['monto_mismo_mes_anterior'].fillna(0)

        # Variables de entrada (features) y salida (target)
        X = data[['Usuario_encoded', 'Categoría_encoded', 'anio', 'mes', 'monto_mismo_mes_anterior']]
        y = data['monto']

        # Dividir datos en entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)

        # Entrenar el modelo con RandomForest
        model = RandomForestRegressor(n_estimators=500, max_depth=20, random_state=42, max_leaf_nodes=25 )
        model.fit(X_train, y_train)

        # Evaluar el modelo
        score = model.score(X_test, y_test)
        print(f"Precisión del modelo: {score:.2f}")


        # --- Generar predicciones para los próximos 12 o N meses ---

        # Obtener usuarios y categorías únicos del dataset
        usuarios_unicos = data['Usuario_encoded'].unique()
        categorias_unicas = data['Categoría_encoded'].unique()

        # Determinar la última fecha del dataset
        ultima_fecha = data['fecha'].max()

        # Generar el dataset futuro con los últimos valores históricos
        futuro = []
  
        # Extraer el último año y mes
        año_inicial = ultima_fecha.year
        mes_inicial = ultima_fecha.month + 1
        
        for usuario in usuarios_unicos:
            for categoria in categorias_unicas:
                año = año_inicial
                anios_futuros = 0
                for i in range(1, meses_futuros + 1):
                    # Calcular el mes y el año futuros
                    mes = ((mes_inicial + i - 1) % 12) or 12  # Mantener meses entre 1 y 12
                    monto_mes_anterior = data[
                        (data['Usuario_encoded'] == usuario) & 
                        (data['Categoría_encoded'] == categoria) &
                        (data['anio'] == año - 1) &  # Buscar el mismo mes del año anterior
                        (data['mes'] == mes)
                    ]['monto'].sum()
                    futuro.append([usuario, categoria, año, mes, monto_mes_anterior])
                    if mes == 12:
                        anios_futuros += 1
                        año = año_inicial + anios_futuros   # Ajustar el año si el mes excede 12

        # Convertir el futuro en DataFrame
        df_futuro = pd.DataFrame(futuro, columns=['Usuario_encoded', 'Categoría_encoded', 'anio', 'mes', 'monto_mismo_mes_anterior'])

        # Predecir montos para los mismos meses del próximo año
        df_futuro['monto'] = model.predict(df_futuro[['Usuario_encoded', 'Categoría_encoded', 'anio', 'mes', 'monto_mismo_mes_anterior']])

        # Decodificar usuario y categoría
        df_futuro['usuario'] = le_usuario.inverse_transform(df_futuro['Usuario_encoded'])
        df_futuro['categoria'] = le_categoria.inverse_transform(df_futuro['Categoría_encoded'])

        # Concatenar las columnas 'Año' y 'Mes' en el formato 'YYYY-MM'
        df_futuro['fecha'] = df_futuro['anio'].astype(str) + '-' + df_futuro['mes'].astype(str).str.zfill(2) + '-01'
        df_futuro = df_futuro[['usuario', 'categoria', 'anio', 'mes', "fecha", 'monto']]

        # Convertir el DataFrame a una lista de diccionarios
        data_dict = df_futuro.to_dict(orient='records')
        # guardar en archivo
        # df_futuro.to_csv("./predicciones_gastos.csv", index=False)
        return data_dict



    # Crear un dataframe para los próximos N meses desde la última fecha
    def generar_futuro_desde_ultima_fecha(self, usuarios, categorias, ultima_fecha, meses_futuros=12):
        futuros = []
        # Extraer el último año y mes
        año_inicial = ultima_fecha.year
        mes_inicial = ultima_fecha.month + 1
        
        for usuario in usuarios:
            for categoria in categorias:
                año = año_inicial
                anios_futuros = 0
                for i in range(1, meses_futuros + 1):
                    # Calcular el mes y el año futuros
                    mes = ((mes_inicial + i - 1) % 12) or 12  # Mantener meses entre 1 y 12
                    futuros.append([usuario, categoria, año, mes])
                    if mes == 12:
                        anios_futuros += 1
                        año = año_inicial + anios_futuros   # Ajustar el año si el mes excede 12
        return futuros

    # Filtrar datos por un usuario y categoría específicos
    def consultar_prediccion(self, usuario, categoria, db : Session):    
        return self.facade.consultar_prediccion(usuario,categoria, db)

    def consultar_historico(self, usuario, categoria, db: Session):
        return self.facade.consultar_historico(usuario, categoria, db)
    
    def consultar_prediccion_categorico(self, usuario, db : Session):
        return self.facade.consultar_prediccion_categorico(usuario, db)
    def consultar_historico_categorico(self, usuario, db : Session):
        return self.facade.consultar_historico_categorico(usuario, db)

    def consultar_categorico_mensual(self, categoria, mes, db : Session):
        return self.facade.PrediccionCrud.consultar_categorico_mensual(categoria, mes, db)
    