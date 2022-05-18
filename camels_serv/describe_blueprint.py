from flask import Blueprint, jsonify
import json

from camels_serv.processState import ProcessState

describe = Blueprint('describe', __name__)


@describe.route('/pegel.json', methods=['GET', 'POST'])
def return_state_describe():
    # create a ProcessState instance
    state = ProcessState()

    # get the GeoDataFrame
    gdf = state.describe()

    # return as geojson
    js = json.loads(gdf.to_json())

    return jsonify(js)
