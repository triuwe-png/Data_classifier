import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def clasificar_datos(df):
    df_num = df.select_dtypes(include=["number"]).fillna(0)

    if df_num.shape[1] < 2:
        return pd.DataFrame({"Error": ["Se necesitan al menos 2 columnas numéricas."]})

    scaler = StandardScaler()
    scaled = scaler.fit_transform(df_num)

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    etiquetas = kmeans.fit_predict(scaled)

    df["Clasificación"] = etiquetas
    return df