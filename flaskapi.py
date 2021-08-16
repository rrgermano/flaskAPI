from flask import Flask, request
import json

def abrir(file):
    n = 0
    chave = 0
    opened = open(file, 'r').read()
    while True:
        if opened[n] != "}":
            n += 1
        else:
            chave += 1
            n += 1
        if chave == 2:
            return opened[:n + 1]

def modify(name, attribute, value):
    dict[name][attribute]=value
    open(path+"general.json","r+").write(json.dumps(dict))
    print(dict)

app = Flask(__name__)

@app.route("/", methods=['GET'])
def get_general():
   return abrir(path+'general.json'), 200

@app.route("/illumination", methods =  ['POST'])
def post_illumination():
    posted = request.get_json()
    n = len(posted.items())
    flag = True
    if n>0 and "on" in posted:
        if isinstance(posted['on'], str):
            modify('illumination', 'on', posted['on'])
            posted.pop('on')
            n-=1
            flag = False
        else:
            return json.dumps({"success":False, "should be": "on should be a boolean variable"}), 204
    if n>0 and 'off' in posted:
            if isinstance(posted['off'], str):
                    modify('illumination', 'off', posted['off'])
                    posted.pop('off')
                    n-=1
                    flag = False
            else:
                return json.dumps({"success": False, "should be": "off should be a string variable"}), 204
    if n>0 and 'automatic' in posted:
            if isinstance(posted['automatic'], bool):
                modify('illumination', 'automatic', posted['automatic'])
                posted.pop('automatic')
                n-=1
                flag = False
            else:
                return json.dumps({"success": False, "should be": "automatic should be a boolean variable"}), 204
    if n==0 and not flag:
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    elif n==0 and flag:
            return json.dumps({'success':False, 'should be':'json'}), 204
    else:
            return json.dumps({'success':False, 'should be': 'A json with "automatic" or "on" or "off" as attributes'}), 203

@app.route("/illumination", methods = ['GET'])
def get_illumination():
        response = json.loads(abrir(path+'general.json'))['illumination']
        return json.dumps(response), 200

@app.route("/ventilation", methods = ['POST'])
def post_ventilation():
    posted = request.get_json()
    n = len(posted.items())
    flag = True
    if n>0 and 'set_temperature'in posted:
        if isinstance(posted['set_temperature'], int) or isinstance(posted['set_temperature'], float):
            modify('ventilation', 'set_temperature', posted['set_temperature'])
            posted.pop('set_temperature')
            n -=1
            flag = False
        else:
            return json.dumps({"success": False, "should be": "set_temperature should be a integer or a float variable"}), 204
    if n>0 and 'automatic' in posted:
        if isinstance(posted['automatic'], bool):
            modify('ventilation', 'automatic', posted['automatic'])
            posted.pop('automatic')
            n-=1
            flag = False
        else:
            return json.dumps({"success": False, "should be": "automatic should be a boolean variable"}), 204
    if n>0 and 'set_velocity' in posted:
        if isinstance(posted['set_velocity'], int) or isinstance(posted['set_velocity'], float):
            modify('ventilation', 'set_velocity', posted['set_velocity'])
            posted.pop('set_velocity')
            flag = False
        else:
            return json.dumps({"success": False, "should be": "set_velocity should be a integer or float variable"}), 204
    if n==0 and not flag:
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    elif n==0 and flag:
        return json.dumps({'success':False, 'should be':'Json'}), 204
    else:
        return json.dumps({'success':False, 'should be': 'A Json with "set_temperature" or "automatic" or "set_velocity" as attributes'}), 203

@app.route("/ventilation", methods = ['GET'])
def get_ventilation():
	response = json.loads(abrir(path+'general.json'))['ventilation']
	return json.dumps(response), 200


@app.route("/light", methods = ['POST'])
def post_light():
    posted = request.get_json()
    n = len(posted.items())
    flag = True
    if n > 0 and 'set_light' in posted:
        if isinstance(posted['set_light'], bool):
            modify('illumination', 'set_light', posted['set_light'])
            posted.pop('set_light')
            n -= 1
            flag = False
        else:
            return json.dumps({"success":False, "should be": "set_light should be a boolean variable"}), 204
    if n == 0 and not flag:
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    elif n == 0 and flag:
        return json.dumps({'success': False, 'should be': 'Json'}), 204
    else:
        return json.dumps({'success': False, 'should be': 'A Json with set_light as attribute'}), 203

@app.route("/light", methods = ['GET'])
def get_light():
    response = json.loads(abrir(path + 'general.json'))['illumination']['set_light']
    light = {"set_light":response}
    return json.dumps(light), 200

#Program Start


#Variaveis API ou Geral
path = "/home/pi/Desktop/dicts/"
dict = json.loads(abrir(path+'general.json'))


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=80)



