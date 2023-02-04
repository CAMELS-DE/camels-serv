import os

from flask import Blueprint, jsonify, request, redirect
from dotenv import load_dotenv

from camels_serv.core.auth import get_github_access_token, get_github_user_info

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login', methods=['GET'])
def login():
    # Github login email
    url = f"https://github.com/login/oauth/authorize?scope=user:email&client_id={CLIENT_ID}&scope=read:user&scope=read:org"
    return redirect(url, code=302)


@auth_blueprint.route('/github/callback', methods=['GET', 'POST'])
def github_callback():
    args = request.args

    # extrace the access token
    request_token = args.get('code')

    # create a access_token
    response = get_github_access_token(CLIENT_ID, CLIENT_SECRET, request_token)

    # check if that worked
    if not 'access_token' in response:
        return jsonify(response), 401

    # return user info
    user = get_github_user_info(response['access_token'])

    # update the access token with retrieved user info
    response.update(user)
    return jsonify(response), 200 if 'login' in response else 400
