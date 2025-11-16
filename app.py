from flask import Flask, render_template, redirect, request
from datetime import datetime as dt
from neomodel import db, config, StructuredNode, RelationshipTo, RelationshipFrom, UniqueIdProperty
import os
from roma_model import Datos, Entity, Place, Event, Date, Type, CorporateBody, Name, Identifier


#################################
# Documentación oficial de Neo4j: 
# https://neo4j.com/blog/developer/py2neo-end-migration-guide/
#
##################################


app = Flask(__name__)


Datos = Datos()

    
base_path = os.path.dirname(
            os.path.abspath(__file__)
        )
    
ruta = os.path.join(base_path, "ui", "index.html")
    
#Opciones de navegación


# def cambiar_relacion(nodo_inicio, nodo_destino, relacion_actual, relacion_nueva):
#     query = f"match (n1:{nodo_inicio})-[r:{relacion_actual}]-(n2:{nodo_destino}) merge (n1)-[r2:{relacion_nueva}]->(n2) delete r return n1, r2, n2"
#     return query

# def cambiar_tipo_entidad(id, tipo_original, nuevo_tipo):
#     query =f"MATCH (n1:Entity)-[r:hasOrHadCategory]-(n2:Type) WHERE elementId(n1) = '{id}' MERGE (n1)-[r2:hasOrHadCategory]->(n3:Type{{name:'{nuevo_tipo}'}}) WHERE elementId(n1) = '{id}' DELETE r RETURN n1, r2, n3"
#     return query
    
# def buscar_atributos_de_entidad():
#     query =f"MATCH (e:Entity)-[r]-(a) RETURN type(r) as relaciones, a.name as Llegada"
#     results, meta = db.cypher_query(query)
#     results_as_dict = [dict(zip(meta, row)) for row in results]
#     return results_as_dict


@app.route("/")
def home():
    return render_template("index.html", opcion="Inicio")


######### Personas ###############


@app.route("/personas")
def personas():
    personas = Datos.Personas_ver()
    return render_template("personas/index.html", personas=personas)

@app.route("/personas/ver/<id>")
def personas_ver(id):
    persona = Datos.Personas_show(id) 
    predicates = Datos.Predicates_index() 
    return render_template("/personas/show.html", persona=persona, predicates=predicates)
    

@app.route("/personas/crear", methods=['POST'])
def personas_crear():
    if request.method=="POST":
        db.begin()
        try:
            entidad = Entity(name=request.form["nombre"]).save()
            tipo = Type.nodes.get(name="Person")
            entidad.type.connect(tipo)
            db.commit()
        except Exception as e:
            print(f"Error: {e}")
            db.rollback()
        return redirect("/personas")

########## Recursos documentales ############### 

@app.route("/recursos_documentales")
def recursos_documentales():
    return render_template("recursos_documentales.html")

############# Instituciones ####################

@app.route("/instituciones")
def instituciones():
    instituciones = Datos.Instituciones_ver()
    return render_template("instituciones/index.html", instituciones=instituciones)

@app.route("/instituciones/ver/<id>")
def instituciones_ver(id):    
    institucion = Datos.buscarEntidad(id)  
    return render_template("/instituciones/show.html", institucion=institucion)

@app.route("/instituciones/nueva")
def instituciones_nueva():
    return render_template("/instituciones/edit.html")



@app.route("/instituciones/crear", methods=['POST'])
def instituciones_crear():
    if request.method=="POST":
        
        formulario = (f"Identificador: {request.form["identificador"]}\nNombre Aut: {request.form["forma-autorizada-nombre"]}\nForma Paralela: {request.form["forma-paralela-nombre"]}\nOtra forma: {request.form["otra-forma-nombre"]}\nTipo: {request.form.get("tipo")}")
        print(formulario)
        
        db.begin()
        try:                     
            #Crear entidad y asignar tipo
            institucion = CorporateBody(name=request.form["forma-autorizada-nombre"]).save()            
            tipo = Type.nodes.get(name="Corporate Body")
            institucion.type.connect(tipo)
            
            #Asignar identificador
            ident = Identifier(name=request.form["identificador"]).save()
            institucion.identifier.connect(ident)
            
            #Forma autorizada del nombre
            auth_name = Name(name=request.form["forma-autorizada-nombre"]).save()
            auth_name_type = Type(name='Forma autorizada del nombre').save()
            auth_name.type.connect(auth_name_type)
            institucion.authorize_name.connect(auth_name)
            
            #Forma paralela del nombre
            paral_name = Name(name=request.form["forma-paralela-nombre"]).save()
            paral_name_type = Type(name='Forma paralela de nombre').save()
            paral_name.type.connect(paral_name_type)
            institucion.parallel_name.connect(paral_name)
            
            #Otras formas del nombre
            other_name = Name(name=request.form["otra-forma-nombre"]).save()
            other_name_type = Type(name='Otra forma de nombre').save()
            other_name.type.connect(other_name_type)
            institucion.other_name.connect(other_name)
            
            #Tipo
            tipo2 = Type(name=request.form.get("tipo")).save()
            institucion.type.connect(tipo2)
                        
            db.commit()
        except Exception as e:
            print(f"Error: {e}")
            db.rollback()      
    instituciones =   Datos.Instituciones_ver()
    return render_template("/instituciones/index.html", instituciones=instituciones)

############ Entidades ############### Hola

@app.route("/entidades")
def entidades():        
    entidades = Datos.verEntidades()            
    return render_template("entidades/index.html", opcion="entidades", entidades=entidades)
    
@app.route("/entidades/ver/<id>")
def entidades_ver(id):    
    entidad = Datos.buscarEntidad(id)  
    return render_template("entidad.html", entidad=entidad)
    
    
@app.route("/entidades/crear")
def entidades_crear():    
    query ="MATCH (n:Type) RETURN elementId(n) as id, n.name as nombre, n.name_es as nombre_es ORDER BY n.name ASC"
    results, meta = db.cypher_query(query)
    tipos = [dict(zip(meta, row)) for row in results]    
    return render_template("nueva_entidad.html", tipos=tipos)


@app.route("/entidades/guardar", methods=["post"])
def entidades_guardar():
    if request.method=="POST":
        db.begin()
        try:
            entidad = Entity(name=request.form["nombre"]).save()
            tipo = Type.nodes.get(name=request.form.get("tipo"))
            entidad.type.connect(tipo)
            db.commit()
        except Exception as e:
            print(f"Error: {e}")
            db.rollback()
        
    # if request.method=="POST":
    #     entidad_nombre = request.form["nombre"]
    #     entidad_tipo = request.form.get("tipo")
    #     query = "MERGE (e:Entity{name:'" + str(entidad_nombre) + "'})"
    #     query = query + " MERGE(t:Type{name:'" + str(entidad_tipo) + "'}) "
    #     query = query + "MERGE (e)-[r:hasOrHadCategory]->(t) RETURN e, r, t"                           
    #     try:                
    #         results, meta = db.cypher_query(query)        
    #     except Exception as e:
    #         return f"ERROR: {e}"
        
        return redirect("/entidades")

@app.route("/entidades/editar/<id>", methods=["POST", "GET"])
def entidades_actualizar(id):   
    if request.method == "GET":
        entidad = Entity.nodes.get(uid=id)          
        tipos = Type.nodes.all()        
        return render_template("nueva_entidad_neo.html", entidad=entidad, tipos=tipos, opcion="editar")
    
@app.route("/entidades/editar2/<id>", methods=["POST", "GET"])
def entidades_actualizar2(id):         
    if request.method =="POST":            
        entidad_nombre = request.form["nombre"]
        #entidad_tipo = request.form.get("tipo")
        nuevo_tipo = request.form.get("tipo")
        tipo_original = request.form.get("tipo_original")
        query = f"MATCH (e:Entity) WHERE elementId(e) ='{id}' SET e.name ='" + str(entidad_nombre) +"' RETURN e.name"         
                        
        try:                
            results, meta = db.cypher_query(query)
            entidad = [dict(zip(meta, row)) for row in results] 
            
            if nuevo_tipo != tipo_original:
                query_nuevo_tipo = Datos.cambiar_tipo_entidad(id,tipo_original, nuevo_tipo)                
                try:
                    result_nt, meta_nt = db.cypher_query(query_nuevo_tipo)
                    nt = [dict(zip(meta_nt, row_nt)) for row_nt in result_nt] 
                except Exception as e:
                    return f"ERROR {e}"            
            # Reconsulto
        
            query_entidad = "MATCH (e:Entity)-[r:hasOrHadCategory]->(t:Type) WHERE elementId(e) ='" + str(id) + "' RETURN elementId(e) as id, e.name as nombre,  t.name as tipo"
            result_entidad, meta_entidad = db.cypher_query(query_entidad)
            entidad = [dict(zip(meta_entidad, row)) for row in result_entidad]
            
            return render_template("entidad.html", entidad=entidad)  
                  
        except Exception as e:
            return f"ERROR: {e}"                                    
                    
    else:
        query_entidad = "MATCH (e:Entity)-[r:hasOrHadCategory]->(t:Type) WHERE elementId(e) ='" + str(id) + "' RETURN elementId(e) as id, e.name as nombre,  t.name as tipo"
        result_entidad, meta_entidad = db.cypher_query(query_entidad)
        entidad = [dict(zip(meta_entidad, row)) for row in result_entidad]
        
        query_tipos ="MATCH (n:Type) RETURN n.name as nombre ORDER BY n.name ASC"
        results_tipos, meta_tipos = db.cypher_query(query_tipos)
        tipos = [dict(zip(meta_tipos, row2)) for row2 in results_tipos]             
        return render_template("nueva_entidad.html", entidad=entidad, tipos=tipos, opcion="editar")
 

############## Tipos #################
        
        
@app.route("/tipos") 
def tipos_ver():
    tipos = Datos.tipos_ver()           
    return render_template("tipos/index.html", opcion="tipos", tipos=tipos) 

@app.route("/tipos/ver/<id>")
def tipos_vertipo(id):
    pass              

if __name__ =='__main__':
    app.run(debug=True)
    #webview.create_window("ROMA Test", "/", width=1400, height=850)
    #webview.start()