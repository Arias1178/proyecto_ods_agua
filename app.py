from flask import Flask, render_template, request
import joblib
import pandas as pd

# Inicializar la app Flask
app = Flask(__name__)

# Cargar el modelo entrenado
modelo = joblib.load("modelo_agua.pkl")

#Menu
@app.route("/", methods=["GET", "POST"])
def menu_formulario():
    seccion = None
    if request.method == "POST":
        seccion = request.form.get("seccion")
    return render_template("menu.html", seccion=seccion)

#ODS
@app.route("/ods/")
def mapaHTML():
    return render_template("ods.html")

#Analisis de viabilidad
@app.route("/viabilidad/")
def mapaHTML():
    return render_template("viabilidad.html")

#Justificacion
@app.route("/justificacion/")
def mapaHTML():
    return render_template("justificacion.html")

#Objetivos de negocio
@app.route("/objetivoneg/")
def mapaHTML():
    return render_template("objetivoneg.html")

#Preguntas Claves
@app.route("/preguntas/")
def mapaHTML():
    return render_template("preguntas.html")

#Evaluacion de Datos
@app.route("/evaluacion/")
def mapaHTML():
    return render_template("evaluacion.html")

@app.route("/Campaña", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        # Recibir los datos del formulario
        datos = {
            'ph': float(request.form['ph']),
            'Hardness': float(request.form['hardness']),
            'Solids': float(request.form['solids']),
            'Chloramines': float(request.form['chloramines']),
            'Sulfate': float(request.form['sulfate']),
            'Conductivity': float(request.form['conductivity']),
            'Organic_carbon': float(request.form['organic_carbon']),
            'Trihalomethanes': float(request.form['trihalomethanes']),
            'Turbidity': float(request.form['turbidity'])
        }
        
        # Crear un DataFrame con los datos
        datos_df = pd.DataFrame([datos])
        
        # Asegúrate de que los nombres de las columnas coincidan exactamente con los del modelo
        datos_df.columns = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity']

        # Realizar la predicción
        prediccion = modelo.predict(datos_df)

        # Determinar el mensaje que se mostrará
        if prediccion == 1:
            resultado = "El agua es potable."
        else:
            resultado = "El agua no es potable."

        return render_template('resultado.html', prediccion=resultado)

    return render_template('index.html')
