from flask import Flask, render_template, redirect
from roma_model import Datos, Entity, Person, Place, Event, Date, Type, db

app = Flask(__name__)


Datos = Datos()

# Grabación exitosa de nodo y asignación de relación
def grabarNodo():
    db.begin()
    try:
        cooper = Person(name="Cooper").save()    
        tipo = Type.nodes.get(name='Persona')
        cooper.type.connect(tipo)
        db.commit()
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    
    
@app.route("/")
def home():    
    return render_template("index.html", opcion="Inicio")
    




if __name__ =='__main__':
    app.run(debug=True)