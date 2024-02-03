import sys
import dotenv
import json
import requests
from flask import Flask, request, abort

config = dotenv.dotenv_values('.env')
app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def respond_to_text():
    print(request.method, file=sys.stdout)
    if request.method == 'POST':
        contents = request.get_json()

        print(contents, file=sys.stdout)
        print(config['KISI_API_KEY'], file=sys.stdout)

        msg = contents['body'].strip()

        for num in config['ALLOWED_NUMBERS'].split(','):
            if num not in contents['from']:
                print("Wrong number!", file=sys.stderr)
                abort(400)

        if len(contents) != 2:
            return("Message must have length of 2")
            abort(400)

        try: 
            open_sesame(msg)
            return {
                'status': "success",
                'msg': ''
            }

        except Exception as e:
            return {
                'status': 'error',
                'msg': str(e)
            }   
    else:
        abort(400)


def open_sesame(msg):
    locks = do_kisi_request('GET', '/locks', None)
    if not locks.ok:
        raise Exception("Locks not found!")
    print(locks.json(), file=sys.stdout)

def do_kisi_request(method, endpoint, params):
    authstring = 'KISI-LOGIIN ' + config['KISI_API_KEY']
    headers = {
       'Content-Type': 'application/json',
       'Accept': 'application/json',
       'Authorization': authstring
    }
    print(authstring, file=sys.stdout)
    print(headers, file=sys.stdout)

    return requests.request('GET', 'https://api.kisi.io' + endpoint, params=params, headers=headers)
