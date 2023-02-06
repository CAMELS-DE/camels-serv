"""
This function can be used to publish a new Plotly.js chart as a CAMELS-DE Dataset Metric.
The metric consists of the plotly chart, a title, a body (description) and optionally a list
of actions, which hold a title and a href to add a link to related documents or sources to 
the metric.
The CAMELS-DE API for creating new metrics is protected. You need to authenticate using your
Github credentials and  be part of the https://github.com/CAMELS-DE organization to get 
authorization. The function implemnts Github OAuth 2.0 device flow and will guide you through
the process.
"""
import requests
import json
import webbrowser
import time
import plotly.graph_objects as go


def save_new_metric(name: str, title: str, body: str, figure: go.Figure, actions: list = [], access_token: str = None, api_url: str = 'https://api.camels-de.org/metrics/add') -> str:
    """
    Upload a new metric to https://camels-de.org/metrics.
    You need to provide a name and the plotly figure. Addtionally, a title, body and actions are
    accepted.

    """
    # set the client id of the Github OAuth App
    client_id = "2ef8ccb234cbcc8d1d5c"

    # create a JSON request header
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    
    # check if there is an access_token
    if access_token is None:
        # get an auth code
        response = requests.post('https://github.com/login/device/code', json=dict(client_id=client_id, scope='read:org,read:user'), headers=headers)
        code_data = response.json()

        # give the code to the user
        print(f"YOUR AUTHENTICATION CODE IS: {code_data['user_code']}\nYou will be redirected to {code_data['verification_uri']}...")

        # open the authentication side
        webbrowser.open_new_tab(code_data['verification_uri'])

        # start checking if the user finished authentication
        t1 = time.time()
        
        # build the request body
        rdata = {
            'client_id': client_id,
            'device_code': code_data['device_code'],
            'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'
        }

        # loop
        while access_token is None:
            response = requests.post('https://github.com/login/oauth/access_token', json=rdata, headers=headers)
            res = response.json()

            # finish?
            if 'access_token' in res:
                access_token = res['access_token']
            else:
                time.sleep(code_data['interval'] + 1)
            
            # check how long we are waiting
            if time.time() - t1 > 15 * 60:
                print('Timeout and aborting...')
                return 
    
    # now, there is an access token.
    #build the body
    data = {
        'name': name,
        'title': title,
        'body': body, 
        'actions': actions,
        'figure': json.loads(figure.to_json())
    }

    # send to API
    # update the header
    headers = {**headers, 'Authorization': f"token {access_token}"}
    response = requests.post(api_url, json=data, headers=headers)

    # add the access token to the response
    out = response.json()
    out['access_token'] = access_token
    print(json.dumps(out, indent=4))

    # return the access token
    return access_token


if __name__ == '__main__':
    # create a figure
    fig = go.Figure(go.Scatter(x=[1,2,3,4], y=[4,8,2,1], mode='markers+lines'))

    # use the function
    save_new_metric('foobar', title='Foobar metric', body='This is not a real metric', figure=fig)
