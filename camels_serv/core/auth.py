import requests


def get_github_access_token(client_id: str, client_secret: str, request_token: str) -> dict:
    # build the url
    url = f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={request_token}"

    # access Github oauth API
    response = requests.post(url, headers=dict(accept='application/json'))

    # extract the access token
    access_token = response.json()

    # return
    return access_token


def is_camels_member(access_token: str) -> bool:
    # use the list of organizations for the authenticated user
    # https://docs.github.com/en/rest/orgs/orgs?apiVersion=2022-11-28#list-organizations-for-the-authenticated-user
    url = "https://api.github.com/user/orgs"

    # check format of token
    if not access_token.lower().startswith('token ') and not access_token.lower().startswith('bearer '):
        access_token = f"token {access_token}"
    
    # reach out
    response = requests.get(url, headers={'Authorization': access_token})
    gh_data = response.json()
    if not isinstance(gh_data, list):
        print(gh_data)
        return False

    # filter the list for camels login
    orgs = [org for org in gh_data if org['login'] == 'CAMELS-DE']

    return len(orgs)


def get_github_user_info(access_token: str) -> dict:
    # use the Github user API
    url = "https://api.github.com/user"
 
    # check format of token
    if not access_token.lower().startswith('token ') and not access_token.lower().startswith('bearer '):
        access_token = f"token {access_token}"
    
    # reach out
    response = requests.get(url, headers={'Authorization': access_token})

    return response.json()

