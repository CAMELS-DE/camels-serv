from flask import Blueprint, jsonify, request

from camels_serv.core.dataset_metrics import DatasetMetrics
from camels_serv.core.auth import is_camels_member


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


@metric_blueprint.route('/list', methods=['GET', 'POST'])
def list_metrics():
    # initialize the Metric Loader
    metrics = DatasetMetrics()

    # load all figues
    mets = metrics.list_metrics()
    return jsonify({
        'metrics': mets,
        'count': len(mets)
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


@metric_blueprint.route('/add', methods=['POST'])
def add_resource():
    # retrieve the access token
    access_token = request.headers.get('Authorization')

    if access_token is None:
        return jsonify({
            'status': 400,
            'message': 'This is a protected route. You must be member of the https://github.com/CAMELS-DE organization and login via https://api.camels-de.org/auth/login using your Github credentials. Then supply the access_token as Authorization header'
        }), 400
    
    # make sure the user is authorized.
    if not is_camels_member(access_token):
        return jsonify({
            'status': 401,
            'message': 'Unauthorized. You are not part of the https://github.com/CAMELS-DE organization, or did not finish the login process.'
        }), 401
    
    # load the body
    data = request.get_json()

    # check that everything is there
    if not 'name' in data:
        return jsonify({
            'status': 400,
            'message': "The data is missing the 'name' attribute. Can't add metrics without name."
        })
    
    # instantiate a metric
    metric = DatasetMetrics()
    metric.save_new_metric(**data)

    return jsonify({
        'status': 201,
        'message': f"Success. The metric {data['name']} was created. Access it at: https://api.camels-de.org/metrics/{data['name']}"
    }), 201
