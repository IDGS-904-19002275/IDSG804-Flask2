from flask import Flask,render_template,request
from flask import flash,make_response
import forms
import traductor
from flask_wtf.csrf import CSRFProtect
from flask import Flask, request, render_template, redirect
from CajasDinamicas import Calculadora

app = Flask (__name__)
app.config['SECRET_KEY']="Esta es una clave encriptada"
csrf=CSRFProtect()

@app.route("/formprueba")
def formprueba():
  
    return render_template("formprueba.html")

@app.route("/Alumnos",methods=['GET','POST'])
def Alumnos():
    reg_alum=forms.UserForm(request.form)
    datos = list()
    if request.method == 'POST' and reg_alum.validate():
        datos.append(reg_alum.matricula.data)
        datos.append(reg_alum.nombre.data)
        print(reg_alum.matricula.data)
        print(reg_alum.nombre.data)
    return render_template("Alumnos.html", form=reg_alum,datos=datos)


@app.route('/')
def mainn():
    return redirect('/cajas_dinamica')

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

@app.route("/traductor", methods=['GET','POST'])
def traducir():
    req_in = traductor.traducirIn(request.form)
    req_out = traductor.traducirOut(request.form)
    datos = list()
    pal2 = ''
    if request.method == 'POST':
        if req_out.envio.data == 'tra' and req_out.validate():
            palabra = ''
            for d in req_out.pal.data:
                palabra += d.lower()

            e=open('traductor_esp.txt','r')
            i=open('traductor_ing.txt','r')
            dicionarioE = e.readlines()
            dicionarioI = i.readlines()

            if req_out.idioma.data == 'esp':
                for item in dicionarioE:
                    if palabra in item:
                        pal2 += dicionarioI[dicionarioE.index(item)]+', '
            else:
                for item in dicionarioI:
                    if palabra in item:
                        pal2 += dicionarioE[dicionarioI.index(item)]+', '
                        
            e.close()
            i.close()
            datos.append('La palabra traducida fue: "'+palabra+'"')


        if req_in.envio.data == 'gua' and req_in.validate():
            esp = ''
            ing = ''
            for d in req_in.esp.data:
                esp += d.lower()
            for d in req_in.ing.data:
                ing += d.lower()
            datos.append('Palabra guardada (esp) '+esp)
            datos.append('Palabra guardada (ing) '+ing)
            e=open('traductor_esp.txt','a')
            i=open('traductor_ing.txt','a')
            e.write(esp+'\n')
            i.write(ing+'\n')
            e.close()
            i.close()

    return render_template("traductor.html",formIn=req_in,formOut=req_out, datos=datos,pal2 = pal2)

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run()