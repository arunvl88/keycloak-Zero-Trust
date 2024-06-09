from flask import Flask, redirect, request, jsonify
import requests

app = Flask(__name__)

# Configuration
CLIENT_ID = 'Cloudflare-client'
CLIENT_SECRET = <client_secret>
AUTH_URL = 'https://keycloak.arunblog.org/realms/myrealm/protocol/openid-connect/auth'
TOKEN_URL = 'https://keycloak.arunblog.org/realms/myrealm/protocol/openid-connect/token'
USERINFO_URL = 'https://keycloak.arunblog.org/realms/myrealm/protocol/openid-connect/userinfo'
REDIRECT_URI = 'http://localhost:5000/callback'
SCOPES = 'openid email profile'

# Routes
@app.route('/')
def home():
    # Redirect user to Keycloak's OAuth 2.0 server
    auth_endpoint = f'{AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={SCOPES}'
    return redirect(auth_endpoint)

@app.route('/callback')
def callback():
    # Get authorization code from callback URL
    code = request.args.get('code')

    # Exchange authorization code for access token
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    token_response = requests.post(TOKEN_URL, data=token_data)
    token_json = token_response.json()

    # Extract access token
    access_token = token_json.get('access_token')
    if not access_token:
        return jsonify({'error': 'Failed to get access token', 'details': token_json}), 400

    # Fetch user info
    user_info_response = requests.get(USERINFO_URL, headers={'Authorization': f'Bearer {access_token}'})
    user_info_json = user_info_response.json()

    # Return user info and token details
    return jsonify({
        'access_token': token_json,
        'user_info': user_info_json
    })

if __name__ == '__main__':
    app.run(debug=True)
