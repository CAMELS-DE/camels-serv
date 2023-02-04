from flask import Blueprint, jsonify


metric_blueprint = Blueprint('metrics', __name__)


@metric_blueprint.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'CAMELS-DE API - metrics API',
        'endpoints': []
    })
