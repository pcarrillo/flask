from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt

app = Flask(__name__) 
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///tareas.db"
db = SQLAlchemy(app)


#Modelo
class MiTarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.String(200),nullable=False)
    completada = db.Column(db.Integer, default=0)
    fecha_creacion = db.Column(db.DateTime, default=dt.now)
    
    def __repr__(self)-> str:
        return f"Tarea {self.id}"

@app.route("/", methods=["POST","GET"])
def home():
    # Add a Task
    if request.method == "POST":
        tarea_actual = request.form["content"]
        nueva_tarea = MiTarea(contenido=tarea_actual)
        try:
            db.session.add(nueva_tarea)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR: {e}")
            return f"ERROR: {e}"
    
    else:
    # Listar tareas
        tareas = MiTarea.query.order_by(MiTarea.fecha_creacion).all()
        return render_template("index.html", tareas=tareas)                            
    return render_template("index.html")

@app.route("/borrar/<int:id>")
def borrar(id:int):
    borrar_tarea = MiTarea.query.get_or_404(id)
    try:
        db.session.delete(borrar_tarea)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR: {e}"
    
        

#Actualizar
@app.route("/actualizar/<int:id>", methods=["POST", "GET"])
def actualizar(id:int):
    tarea = MiTarea.query.get_or_404(id)
    if request.method=="POST":
        tarea.contenido = request.form["content"]
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR: {e}"
    else:
        return render_template("actualizar.html", tarea=tarea)


if __name__ == '__main__': 
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)