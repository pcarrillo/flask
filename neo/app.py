from flask import Flask, render_template, redirect, request
from datetime import datetime as dt
from neomodel import db, config, StructuredNode, RelationshipTo, RelationshipFrom
import webview
import os


#################################
# Documentación oficial de Neo4j: 
# https://neo4j.com/blog/developer/py2neo-end-migration-guide/
#
##################################


app = Flask(__name__)

config.DATABASE_URL = "bolt://neo4j:sarcalatraba@localhost:7687"
config.DATABASE_NAME ="neo4j"


    
base_path = os.path.dirname(
            os.path.abspath(__file__)
        )
    
ruta = os.path.join(base_path, "ui", "index.html")
    
#Opciones de navegación


def cambiar_relacion(nodo_inicio, nodo_destino, relacion_actual, relacion_nueva):
    query = f"match (n1:{nodo_inicio})-[r:{relacion_actual}]-(n2:{nodo_destino}) merge (n1)-[r2:{relacion_nueva}]->(n2) delete r return n1, r2, n2"
    return query

def cambiar_tipo_entidad(id, tipo_original, nuevo_tipo):
    query =f"MATCH (n1:Entity)-[r:hasOrHadCategory]-(n2:Type) WHERE elementId(n1) = '{id}' MERGE (n1)-[r2:hasOrHadCategory]->(n3:Type{{name:'{nuevo_tipo}'}}) DELETE r RETURN n1, r2, n3"
    return query
    


@app.route("/")
def home():
    return render_template("index.html", opcion="Inicio")





@app.route("/entidades")
def entidades():
    
    
    query ="MATCH (c:Entity)-[r:hasOrHadCategory]->(t:Type) RETURN elementId(c) as id, c.name as nombre ,t.name as tipo ORDER BY c.name"
    results, meta = db.cypher_query(query)
    results_as_dict = [dict(zip(meta, row)) for row in results]

    return render_template("entidades.html", opcion="entidades", entidades=results_as_dict)
    
@app.route("/entidades/ver/<id>")
def entidades_ver(id):
    query = f"MATCH (e:Entity)-[r:hasOrHadCategory]->(t:Type) WHERE elementId(e) ='{id}' RETURN elementId(e) as id, e.name as nombre,  t.name as tipo"
    results, meta = db.cypher_query(query)
    entidad = [dict(zip(meta, row)) for row in results]   
    #return f"Viendo entidad {id} + {ver_entidad}"    
    return render_template("entidad.html", entidad=entidad)    
    
    #return f"Viendo entidad {id}"
@app.route("/entidades/crear")
def entidades_crear():
    
    query ="MATCH (n:Type) RETURN elementId(n) as id, n.name as nombre ORDER BY n.name ASC"
    results, meta = db.cypher_query(query)
    tipos = [dict(zip(meta, row)) for row in results]    
    return render_template("nueva_entidad.html", tipos=tipos)



@app.route("/entidades/guardar", methods=["post"])
def entidades_guardar():
    if request.method=="POST":
        entidad_nombre = request.form["nombre"]
        entidad_tipo = request.form.get("tipo")
        query = "MERGE (e:Entity{name:'" + str(entidad_nombre) + "'})"
        query = query + " MERGE(t:Type{name:'" + str(entidad_tipo) + "'}) "
        query = query + "MERGE (e)-[r:hasOrHadCategory]->(t) RETURN e, r, t"                           
        try:                
            results, meta = db.cypher_query(query)        
        except Exception as e:
            return f"ERROR: {e}"
        
        return redirect("/entidades")
    
@app.route("/entidades/editar/<id>", methods=["POST", "GET"])
def entidades_actualizar(id):         
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
                query_nuevo_tipo = cambiar_tipo_entidad(id,tipo_original, nuevo_tipo)                
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
                        
          


if __name__ =='__main__':
    app.run(debug=True)
    #webview.create_window("ROMA Test", "/", width=1400, height=850)
    #webview.start()