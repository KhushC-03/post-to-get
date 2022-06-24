import base64
import json
import random
from flask import Flask, request, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

app = Flask(__name__)


BASE_URL = 'http://127.0.0.1:5000/'
uri = "Database URL"

# Example Request


# data = {
#     'URL':"Request Url",
#     'PAYLOAD':json.dumps({"FormData Name 1":"Form Data Value 1","Form Data Name 2":"Form Data Value 2"})
# }

# r = requests.post(f'{BASE_URL}/post-to-get',data=data,timeout=4)
# redirectURL = r.json()['requesturl']



if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)




app.config['SQLALCHEMY_DATABASE_URI'] = uri

db = SQLAlchemy(app)
engine = create_engine(uri)

LETTERS = ['A', 'B', 'C', 'D', 'E','F', 'G', 'H', 'I', 'J', 'K','L', 'M', 'N', 'O', 'P', 'Q','R', 'S', 'T', 'U','V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0','1','2','3','4','5','6','7','8','9','10']
def createID(length):
    ID = []
    for i in range(length):
        if i % 2 == 0:
            ID.append(random.choice(LETTERS))
        else:
            ID.append(random.choice(NUMBERS))
    return ''.join(ID)



@app.route('/post-to-get',methods=['GET','POST'])
def posttoget():
    if request.method == 'POST':
        payload = request.form.get('PAYLOAD')
        URL = request.form.get('URL')
        try:
            CURRENTIDS = [i[0] for i in engine.execute("""SELECT ALL ID FROM posttoget;""").fetchall()]
            while True:
                NONCE = createID(15)
                if not NONCE in CURRENTIDS:
                    break
            try:
                jsondata = json.loads(payload)
            except:
                return jsonify({'message':'error','reason':"error parsing json payload"}), 400
            HTML = base64.b64encode(f"""
                <body onload=document.posttoget.submit()>
                    <form action="{URL}" method="post" id="posttoget" name="posttoget">
                        INPUTSHERE
                    </form>
                </body>
            """.replace("INPUTSHERE","".join([f"""<input type="hidden" name="{namevalue}" value="{jsondata[namevalue]}"/>""" for namevalue in jsondata])).encode()).decode()
            stringifieddata = json.dumps({'requestID':NONCE,'URL':URL,'payload':payload,'HTML':HTML})
            engine.execute(
                f"""
            INSERT INTO posttoget (id, requestdata)
            VALUES ('{NONCE}', '{stringifieddata}');
            """)
            return jsonify({'message':'success','id':NONCE,'requesturl':f'{BASE_URL}/post-to-get?ID={NONCE}','URL':URL,'payload':payload}), 200
        except Exception as ex:
            return jsonify({'message':'error','reason':str(ex),'id':NONCE,'requesturl':f'{BASE_URL}/post-to-get?ID={NONCE}'}), 400
    elif request.method == 'GET':
        try:
            ID = request.args['ID']
        except:
            return jsonify({'message':'error','reason':'request id not provided'})
        try:
            stringifieddata = engine.execute(f"""
                SELECT requestdata from posttoget
                WHERE id = '{ID}';
                """  ).first()[0]  
            HTML = base64.b64decode(json.loads(stringifieddata)['HTML']).decode("utf-8")
            return render_template_string(HTML), 200
        except Exception as ex:
            return jsonify({'message':'error','reason':str(ex),'id':ID,'requesturl':f'{BASE_URL}/post-to-get?ID={ID}'}), 400
    else:
        return 'Incorrect Request Method'

if __name__ == "__main__":
    app.run()
