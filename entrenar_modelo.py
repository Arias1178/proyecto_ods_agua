import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# 1. Cargar el dataset
df = pd.read_csv("C:/Users/santi/OneDrive/Escritorio/proyecto_ods_agua/water_potability.csv")


# 2. Imputar valores faltantes con la mediana
df.fillna(df.median(), inplace=True)

# 3. Dividir en características y variable objetivo
X = df.drop("Potability", axis=1)
y = df["Potability"]

# 4. Dividir en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 5. Inicializar y entrenar el modelo XGBoost
modelo = XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    use_label_encoder=False,
    eval_metric='logloss'
)
modelo.fit(X_train, y_train)

# 6. Evaluar el modelo
y_pred = modelo.predict(X_test)
print("Precisión del modelo:", accuracy_score(y_test, y_pred))
print("Reporte de clasificación:\n", classification_report(y_test, y_pred))
print("Matriz de confusión:\n", confusion_matrix(y_test, y_pred))

# 7. Guardar el modelo entrenado
joblib.dump(modelo, "modelo_agua.pkl")
print("Modelo guardado exitosamente como 'modelo_agua.pkl'")
