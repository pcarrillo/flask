from flask import Flask, render_template, redirect, request
from neomodel import db, config, StructuredNode, RelationshipTo, RelationshipFrom


app = Flask(__name__)

config.DATABASE_URL = "bolt://neo4j:sarcalatraba@localhost:7687"
config.DATABASE_NAME ="neo4j"

