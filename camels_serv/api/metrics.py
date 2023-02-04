from flask import Blueprint, jsonify

from camels_serv.core.dataset_metrics import DatasetMetrics


metric_blueprint = Blueprint('metrics', __name__)


@metric_blueprint.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'CAMELS-DE API - metrics API',
        'endpoints': [
            {
                'url': '/metrics/list',
                'description': 'List all metrics that are currently available.',
                'methods': ['GET', 'POST']
            },
            {
                'url': '/metrics/<METRIC>',
                'description': 'Return the full metric, including the Metric plotly figure, title and body.',
                'methods': ['GET', 'POST']
            },
            {
                'url': '/metrics/<METRIC>.<plotly | description>.json',
                'description': 'Return the only one part of the metric. Can be either the plotly figure or the description body, including title, body and links.',
                'methods': ['GET', 'POST']
            }
        ]
    })


@metric_blueprint.route('/<string:name>', methods=['GET', 'POST'])
def get_card(name: str):
    # initialize the Metric Loader
    metrics = DatasetMetrics()

    # create the full info
    try:
        info = metrics.load_plotly_description(name)
        info['figure'] = metrics.load_plotly_figure(name)
        
        # return
        return jsonify(info)       
    except FileNotFoundError as e:
        return jsonify({
            'status': 404,
            'message': str(e)
        }), 404


@metric_blueprint.route('/<string:name>.<string:extension>.json', methods=['GET', 'POST'])
def get_resource(name: str, extension: str):
    # initialize the Metric Loader
    metrics = DatasetMetrics()

    try:
        # check the extension
        if extension.lower() == 'plotly':
            return jsonify(metrics.load_plotly_figure(name))
        elif extension.lower() == 'description':
            return jsonify(metrics.load_plotly_description(name))
        else:
            return jsonify({
                'status': 400,
                'message': f"The requested resource of type '{extension}' is not supported."
            }), 400
    except FileNotFoundError as e:
        return jsonify({
            'status': 404,
            'message': str(e)
        }), 404
