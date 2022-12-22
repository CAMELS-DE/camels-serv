import json
import io

from flask import Blueprint, jsonify, send_file, jsonify, make_response
import geopandas as gpd

from camels_serv.core.processState import ProcessState

process_blueprint = Blueprint('describe', __name__)


@process_blueprint.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'CAMELS-DE API - processing state API',
        'endpoints': [
            {
                'url': '/state/metadata.<csv|json|gpkg|geojson|txt>',
                'description': 'Get the current processing status of all stations available on the CAMELS-DE processing server',
                'methods': ['GET', 'POST']
            },
            {
                'url': '/state/<NUTS_LVL2>/metadata.<csv|json|gpkg|geojson|txt>',
                'description': 'Get the current processing status of all stations in the respective federal state on the CAMELS-DE processing server',
                'methods': ['GET', 'POST']
            }
        ]
    })


def _geodataframe_to_http_response(gdf: gpd.GeoDataFrame, fmt: str, fname: str = 'camels-de_metadata'):
    """Helper function to transform GeoDataFrame to flask.Response"""
    # switch format
    
    # return as geojson
    if 'json' in fmt.lower():
        js = json.loads(gdf.to_json())
        return jsonify(js)
    
    # text
    elif fmt.lower() == '.txt':
        output = make_response(gdf.to_csv(index=None, sep=' '))
        output.headers['Content-Type'] = "text/plain"
        return output
    
    # download as csv
    elif fmt.lower() == '.csv':
        output = make_response(gdf.to_csv(index=None))
        output.headers["Content-Disposition"] = f"attachment; filename={fname}.csv"
        output.headers["Content-Type"] = "text/csv"
        return output

    # make a geopackage
    elif fmt.lower() == '.gpkg':
        buffer = io.BytesIO()
        gdf.to_file(buffer, layer='pegel', driver='GPKG')
        buffer.seek(0)

        # make the response
        return send_file(
            buffer,
            mimetype='application/geopackage+sqlite3',
            as_attachment=True,
            attachment_filename=f'{fname}.gpkg'
        )

    else:
        return jsonify({
            'status': 404,
            'message': f'The format {fmt} is not supported.'
        }), 404


@process_blueprint.route('/metadata<string:format_>', methods=['GET', 'POST'])
def return_states_describe(format_: str = '.json'):
    # create a ProcessState instance
    state = ProcessState()

    # get the GeoDataFrame
    gdf = state.describe()

    # return
    return _geodataframe_to_http_response(gdf, format_, 'camels-de_metadata')

@process_blueprint.route('/<string:fedstate>/metadata<string:format_>', methods=['GET', 'POST'])
def return_fedstate_describe(fedstate: str, format_: str = 'json'):
    # create a ProcessState instance
    state = ProcessState()

    # get the geodataframe
    gdf = state.describe()

    # check if the state exists
    if fedstate.upper() not in gdf.nuts_lvl2.values:
        return jsonify({
            'status': 404,
            'message': f"The identifier '{fedstate.upper()}' is not a valid NUTS level 2 identifier, or no data at all has been provided by the respective federal state."
        }), 404
    
    # filter
    gdf = gdf.where(gdf.nuts_lvl2 == fedstate.upper()).dropna(axis=0, how='all')

    # return
    return _geodataframe_to_http_response(gdf, format_, f'{fedstate.upper()}_metadata')
    