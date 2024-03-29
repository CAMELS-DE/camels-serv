import os
import json

from flask import Blueprint, jsonify

from camels_serv.core import config

static_blueprint = Blueprint('static', __name__)


@static_blueprint.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'CAMELS-DE API - static data API',
        'endpoints': [
            {
                'url': '/static/germany.geojson',
                'description': 'Return the admisnistrative boundary level 2 of Germany, extracted from OpenStreetMap as GeoJSON',
                'methods': ['GET']
            },
        ]
    })

@static_blueprint.route('/<string:name>', methods=['GET'])
def get_static_file(name: str):
    # build the file name
    fname = os.path.join(config.STATICPATH, name)

    # load
    if not os.path.exists(fname):
        return jsonify({
            'status': 404,
            'message': f'The file {fname} was not found.'
        }), 404
    
    # load geojson and return
    with open(fname, 'r') as f:
        js = json.load(f)
    
    return js
