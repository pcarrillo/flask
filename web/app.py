from flask import Flask, render_template
from neomodel import db, config, StructuredNode, RelationshipTo, RelationshipFrom
import webview
import sys
import threading

app = Flask(__name__)

config.DATABASE_URL = "bolt://neo4j:sarcalatraba@localhost:7687"
config.DATABASE_NAME ="neo4j"


@app.route('/')
def hello_world():
    query ="MATCH (c:Entity)-[r:hasOrHadCategory]->(t:Type) RETURN elementId(c) as id, c.name as nombre ,t.name as tipo ORDER BY c.name"
    results, meta = db.cypher_query(query)
    results_as_dict = [dict(zip(meta, row)) for row in results]
    print(results_as_dict)
    return render_template("index.html", entidades=results_as_dict)
    
    
    #return 'Hello World! Niño!!!'

#def start_server():
#    app.run(host='0.0.0.0', port=80)

if __name__ == '__main__':
    app.run(debug=True)
# Inicio de modo ventana - > todo será comentado

    # t = threading.Thread(target=start_server)
    # t.daemon = True
    # t.start()

    # webview.create_window("PyWebView & Flask", "http://localhost/")
    # webview.start()
    # sys.exit()