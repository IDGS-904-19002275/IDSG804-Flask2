from flask import Flask, request, render_template, redirect

import forms
from clases import Calculadora

app = Flask(__name__)

@app.route('/')
def mainn():
    return redirect('/cajas_dinamica')

@app.route('/alumnos', methods=['GET', 'POST'])
def alumnos():
    registrar_Alumno = forms.UserForm(request.form)
    Mat = ''
    Nom = ''
        
    if request.method == 'POST':
        Mat = registrar_Alumno.matricula.data
        Nom = registrar_Alumno.nombre.data
    
    return render_template('alumnos.html', form = registrar_Alumno, mat=Mat, nom = Nom)

@app.route('/cajas_dinamica', methods=['GET', 'POST'])
def cajas_dinamica(): 
    Active = False
    Ns = 0
    
    if request.method == 'POST':
        Ns = int(request.form.get('numero'))
        Active = Ns != 0
    
    return render_template('CajasDinamicas.html', active = Active, ns = Ns, name="Cajas Dinámicas")


@app.route('/calcular', methods=['GET', 'POST'])
def calcular():

    Numeros = Calculadora.get_Array(request.form)
    
    return render_template("OtroCajasDinamicas.html",
                           numeros = Numeros,
                           repetidos = Calculadora.contar_repeticiones(Numeros),
                           comas = Calculadora.concatenar_Numeros(Numeros),
                           promedio = Calculadora.promedio(Numeros),
                           nMenor = Calculadora.num_Menor(Numeros),
                           nMayor = Calculadora.num_Mayor(Numeros),
                           name = "Resultado de " + str(len(Numeros)) + " números")




    # Numeros = Calculadora.get_Array(request.form)

    # return render_template("OtroCajasDinamicas.html",
    #                        numeros = Numeros,
    #                        repetidos = Calculadora.repeticiones(Numeros),
    #                        comas = Calculadora.concatenar_Numeros(Numeros),
    #                        promedio = Calculadora.promedio(Numeros),
    #                        nMenor = Calculadora.num_Menor(Numeros),
    #                        nMayor = Calculadora.num_Mayor(Numeros),
    #                        name = "Resultado de " + str(len(Numeros)) + " números")


if __name__ == "__main__":
    app.run(debug = True)
