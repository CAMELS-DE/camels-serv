from sys import version_info

from flask import Flask, jsonify
from flask_cors import CORS

from camels_serv import __version__


def get_app():
    # build main app object
    app = Flask(__name__)
    CORS(app, origin='*')

    # import bluprints and register
    from camels_serv.api.process_state import process_blueprint
    app.register_blueprint(process_blueprint, url_prefix='/state')

    from camels_serv.api.static import static_blueprint
    app.register_blueprint(static_blueprint, url_prefix='/static')

    from camels_serv.api.data import data_blueprint
    app.register_blueprint(data_blueprint, url_prefix='/data')

    from camels_serv.api.metrics import metric_blueprint
    app.register_blueprint(metric_blueprint, url_prefix='/metrics')

    from camels_serv.api.auth import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # define the 'landing page' api endpoint
    @app.route('/', methods=['GET', 'POST'])
    def index():
        info = {
            'message': 'Welcome to CAMELS-DE API. Maybe you wanted to visit https://camels-de.org',
            'api_version': __version__,
            'python_version': f"{version_info.major}.{version_info.minor}.{version_info.micro}",
            'api_endpoints': [
                {
                    'url': '/data',
                    'description': 'Data retrieval API. Load CAMELS-DE subsets here.',
                    'methods': ['GET']
                },
                {
                    'url': '/state',
                    'description': 'Current processing state of the CAMELS-DE dataset',
                    'methods': ['GET']
                },
                {
                    'url': '/static',
                    'description': 'Static, auxiliary data like adminsitrative boundaries, processed from OpenStreetMap',
                    'methods': ['GET']
                },
                {
                    'url': '/metrics',
                    'descirption': 'CAMELS-DE dataset metrics API. Can be used to retrieve and save dataset-wide metrics.',
                    'methods': ['GET']
                }
            ]
        }

        return jsonify(info)

    return app


def run(**kwargs):
    # set some defaults
    if 'host' not in kwargs:
        kwargs['host'] = '0.0.0.0'
    
    app = get_app()
    app.run(**kwargs)


if __name__ == '__main__':
    import fire
    fire.Fire(run)

