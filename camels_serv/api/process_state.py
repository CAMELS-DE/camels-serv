from flask import Blueprint, jsonify, response
import json

from camels_serv.core.processState import ProcessState

process_blueprint = Blueprint('describe', __name__)


@process_blueprint.route('/process/pegel<format:str>', methods=['GET', 'POST'])
def return_state_describe(format: str = '.json'):
    # create a ProcessState instance
    state = ProcessState()

    # get the GeoDataFrame
    gdf = state.describe()

    # return as geojson
    if 'json' in format.lower():
        js = json.loads(gdf.to_json())
        return jsonify(js)
    elif 'csv' in format.lower():
        csv = gdf.to_csv()
        return csv
    else:
        return jsonify({
            'status': 404,
            'message': f'The format {format} is not supported.'
        }), 404
