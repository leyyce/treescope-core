from flask_restx import Model, fields

pagination_base = Model('pagination_base', {
    'page': fields.Integer,
    'per_page': fields.Integer,
    'count': fields.Integer,
    'pages': fields.Integer,
    'total': fields.Integer,
    'has_next': fields.Boolean,
    'has_prev': fields.Boolean,
    'prev_num': fields.Integer,
    'next_num': fields.Integer,
})
