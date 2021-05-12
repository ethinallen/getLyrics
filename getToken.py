import requests
import keys

def getToken():
    data = {
      'client_id': keys.client_id,
      'client_secret': keys.client_secret,
      'grant_type': 'client_credentials'
    }

    response = requests.post('https://api.genius.com/oauth/token', data=data)
    return response.json()['access_token']

if __name__ == "__main__":
    print(getToken())
