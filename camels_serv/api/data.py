from flask import Blueprint, jsonify


data_blueprint = Blueprint('data', __name__)


@data_blueprint.route('/', methods=['GET', 'POST'])
def index():
    return jsonify({
        'message': 'CAMELS-DE API - data retrieval API',
        'endpoints': [],
        'warning': 'Not implemented. The data retrieval API is not yet implemented. Come back, when the dataset is published. Until then use the processing state API: /state.'
    })
