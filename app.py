from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Cargar el modelo de Machine Learning
modelo = joblib.load('modelo_agua.pkl')  # Más adelante creamos este modelo

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/resultado", methods=["POST"])
def resultado():
    # 1. Recibir datos del formulario
    ph = float(request.form["ph"])
    color = float(request.form["color"])
    turbidez = float(request.form["turbidez"])
    conductividad = float(request.form["conductividad"])
    oxigeno = float(request.form["oxigeno"])

    # 2. Preparar los datos en el formato que espera el modelo
    datos_usuario = np.array([[ph, color, turbidez, conductividad, oxigeno]])

    # 3. Hacer predicción
    prediccion = modelo.predict(datos_usuario)[0]  # Sacamos el primer valor (0 o 1, por ejemplo)

    # 4. Definir mensaje de salida
    if prediccion == 0:
        resultado = "El agua es limpia y segura. ✅"
    elif prediccion == 1:
        resultado = "El agua está contaminada. ⚠️"
    else:
        resultado = "El agua no es apta y no puede ser recuperada. ❌"

    return render_template("resultado.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)