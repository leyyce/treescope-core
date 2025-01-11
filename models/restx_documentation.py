import copy
from flask_restx import fields
from sqlalchemy import inspect
import sys

SQLALCHEMY_TYPES_NULLABLE = {
    "ARRAY": fields.List,
    "INT": fields.Integer,
    "CHAR": fields.String,
    "VARCHAR": fields.String,
    "NCHAR": fields.String,
    "NVARCHAR": fields.String,
    "TEXT": fields.String,
    "text": fields.String,
    "FLOAT": fields.String,
    "NUMERIC": fields.String,
    "REAL": fields.Float,
    "DECIMAL": fields.Float,
    "TIMESTAMP": fields.Float,
    "DATETIME": fields.DateTime,
    "BOOLEAN": fields.Boolean,
    "BIGINT": fields.Integer,
    "INTEGER": fields.Integer
}


SQLALCHEMY_TYPES = {
    "ARRAY": fields.List(fields.String(), required=True),
    "INT": fields.Integer(required=True),
    "CHAR": fields.String(required=True),
    "VARCHAR": fields.String(required=True),
    "NCHAR": fields.String(required=True),
    "NVARCHAR": fields.String(required=True),
    "TEXT": fields.String(required=True),
    "text": fields.String(required=True),
    "FLOAT": fields.String(required=True),
    "NUMERIC": fields.String(required=True),
    "REAL": fields.Float(required=True),
    "DECIMAL": fields.Float(required=True),
    "TIMESTAMP": fields.Float(required=True),
    "DATETIME": fields.DateTime(required=True),
    "BOOLEAN": fields.Boolean(required=True),
    "BIGINT": fields.Integer(required=True),
    "INTEGER": fields.Integer(required=True)
}

def create_restx_model(sqlAlchemyModel, namespace):
    model = {}
    mapper = inspect(sqlAlchemyModel)
    for column in mapper.attrs:
        if str(type(column)) == "<class 'sqlalchemy.orm.relationships.Relationship'>":
            model[column.key] = fields.Nested(namespace.model(column.key, create_restx_model(str_to_class(column.argument), namespace)))
        elif str(type(column)) == "<class 'sqlalchemy.orm.relationships.RelationshipProperty'>":
            continue
        else:
            if len(column.columns[0].foreign_keys) != 0: #skip foreign keys in model
                continue
            model[column.columns[0].name] = SQLALCHEMY_TYPES[ str(column.columns[0].type) .split( "(" ) [0] ] if column.columns[0].nullable == False else SQLALCHEMY_TYPES_NULLABLE[ str( column.columns[0].type ).split( "(" ) [0] ]
            doc = copy.copy(column.doc)
            if doc != None:
                model[column.columns[0].name].description = doc
            #model[column.columns[0].name].description = "TEST"
    return model
    
def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)
    
    # 
    

