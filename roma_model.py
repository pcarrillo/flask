from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      UniqueIdProperty, RelationshipTo, db)

class Datos:
    def __init__(self):
        config.DATABASE_URL = "bolt://neo4j:sarcalatraba@localhost:7687"
        config.DATABASE_NAME ="neo4j"
        
    ########### Métodos de la versión funcional ##########
    
    def cambiar_relacion(nodo_inicio, nodo_destino, relacion_actual, relacion_nueva):
        query = f"match (n1:{nodo_inicio})-[r:{relacion_actual}]-(n2:{nodo_destino}) merge (n1)-[r2:{relacion_nueva}]->(n2) delete r return n1, r2, n2"
        return query

    def cambiar_tipo_entidad(id, tipo_original, nuevo_tipo):
        query =f"MATCH (n1:Entity)-[r:hasOrHadCategory]-(n2:Type) WHERE elementId(n1) = '{id}' MERGE (n1)-[r2:hasOrHadCategory]->(n3:Type{{name:'{nuevo_tipo}'}}) WHERE elementId(n1) = '{id}' DELETE r RETURN n1, r2, n3"
        return query
        
    def buscar_atributos_de_entidad():
        query =f"MATCH (e:Entity)-[r]-(a) RETURN type(r) as relaciones, a.name as Llegada"
        results, meta = db.cypher_query(query)
        results_as_dict = [dict(zip(meta, row)) for row in results]
        return results_as_dict
    
    ############## Find e métodos de la v. funcional ############    
        
        
    def grabarEntidad(self, nombre, tipo):
        query = "MERGE (e:Entity {name:'" + str(nombre) + "'}) MERGE(t:Type {name:'" + str(
            tipo) + "'}) MERGE (t)-[r:TypeRelation]->(e) MERGE (e)-[r2:hasOrHadCategory]->(t) RETURN e, t,r, r2"
        results, meta = db.cypher_query(query)

    def buscarEntidad(self, id_entidad):
        query = "MATCH (e:Entity)-[r:hasOrHadCategory]->(t:Type) WHERE elementId(e) ='" + str(id_entidad) + "' RETURN elementId(e) as id, e.name as nombre,  t.name as tipo"
        results, meta = db.cypher_query(query)
        entidad = [dict(zip(meta, row)) for row in results] 
        return entidad

    def verRelacionesDeEntidad(self, id_entidad):
        query ="MATCH (e:Entity)-[r]-(m)  WHERE elementId(e) = '" + id_entidad +"'  RETURN e.name as origen, TYPE(r)  as tipo,  m.name as destino"
        results, meta = db.cypher_query(query)
        return results

    def actualizarEntidad(self, id_entidad, entidad, tipo):
        query = "MATCH (e:Entity)<-[r:TypeRelation]-(t:Type) WHERE elementId(e) ='" + str(id_entidad) + "' SET e.name = '" + str(entidad) + "' SET t.name = '" + str(tipo) + "'"
        results, meta = db.cypher_query(query)
        return results

    def verEntidades(self):
        query = "MATCH (c:Entity)-[r:hasOrHadCategory]->(t:Type) RETURN elementId(c) as id, c.name as nombre ,t.name as tipo ORDER BY c.name"
        results, meta = db.cypher_query(query)
        entidades = [dict(zip(meta, row)) for row in results] 
        return entidades
        