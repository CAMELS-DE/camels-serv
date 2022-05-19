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

    # define the 'landing page' api endpoint
    @app.route('/', methods=['GET', 'POST'])
    def index():
        info = {
            'message': 'Welcome to CAMELS-DE API. Maybe you wanted to visit https://camels-de.org',
            'api_version': __version__,
            'python_version': f"{version_info.major}.{version_info.minor}.{version_info.micro}",
            'api_endpoints': [
                {
                    'url': '/state',
                    'description': 'Current processing state of the CAMELS-DE dataset',
                    'methods': ['GET']
                }
            ]
        }

        return jsonify(info)

    return app


if __name__ == '__main__':
    app = get_app()
    app.run(debug=True, host="0.0.0.0")
