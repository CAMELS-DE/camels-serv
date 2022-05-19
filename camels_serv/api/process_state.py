import json
import io

from flask import Blueprint, jsonify, send_file, jsonify

from camels_serv.core.processState import ProcessState

process_blueprint = Blueprint('describe', __name__)


@process_blueprint.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'CAMELS-DE API - processing state API',
        'endpoints': [
            {
                'url': '/state/pegel.<csv|json|gpkg>',
                'description': 'Get the current processing status of each pegel',
                'methods': ['GET', 'POST']
            }
        ]
    })
@process_blueprint.route('/pegel<string:format_>', methods=['GET', 'POST'])
def return_state_describe(format_: str = '.json'):
    # create a ProcessState instance
    state = ProcessState()

    # get the GeoDataFrame
    gdf = state.describe()

    # return as geojson
    if 'json' in format_.lower():
        js = json.loads(gdf.to_json())
        return jsonify(js)
    elif 'csv' in format_.lower():
        csv = gdf.to_csv()
        return csv
    elif 'gpkg' in format_.lower():
        buffer = io.BytesIO()
        gdf.to_file(buffer, layer='pegel', driver='GPKG')
        buffer.seek(0)

        # make the response
        return send_file(
            buffer,
            mimetype='application/geopackage+sqlite3',
            as_attachment=True,
            attachment_filename='camels_pegel.gpkg'
        )

    else:
        return jsonify({
            'status': 404,
            'message': f'The format {format_} is not supported.'
        }), 404
