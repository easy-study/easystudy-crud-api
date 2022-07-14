from flask import Flask
from flask import request
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
import os


app = Flask(__name__)

client = MongoClient(os.environ.get('MONGODB_URI'))
db = client.test
db_cursos = db.cursos


@app.route('/')
def obter_todos():
    return dumps(list(db_cursos.find()))


@app.route('/<id>')
def obter(id):
    return dumps(db_cursos.find_one({"_id": ObjectId(id)}))


@app.route('/', methods=['POST'])
def criar():
    return dumps(db_cursos.insert_one(request.json).inserted_id)


@app.route('/<id>', methods=['PUT'])
def atualizar(id):
    query = {"_id": ObjectId(id)}
    valores = {"$set": request.json}

    db_cursos.update_one(query, valores)
    return f'Curso "{id}" atualizado com sucesso'


@app.route('/<id>', methods=['DELETE'])
def apagar(id):
    db_cursos.delete_one({"_id": ObjectId(id)})
    return f'Curso {id} apagado!!!!'


if __name__ == '__main__':
    app.run()