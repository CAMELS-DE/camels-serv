from flask import Flask
from flask_cors import CORS


def get_app():
    # build main app object
    app = Flask(__name__)
    CORS(app, origin='*')

    # import bluprints and register
    from camels_serv.describe_blueprint import describe
    app.register_blueprint(describe)

    return app


if __name__ == '__main__':
    app = get_app()
    app.run(debug=False, host="0.0.0.0")
