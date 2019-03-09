from flask import Flask
app = Flask(__name__)

url = "http://130.82.239.210"

import requests
import json

@app.route("/")
# def getList():
#     r = requests.get(url+"/signal/KBI_Tankfuellstand_Prozent/value")
#     j = r.json()
#     data = json.loads(json.dumps(j))
#
#     print(j.get('value'))
#     return "worked"

# determines whether there is any space in the car
@app.route("/space")
def isSpace():
    list = ['AB_Gurtschloss_BF', 'AB_Gurtschloss__Reihe2_FA', 'AB_Gurtschloss__Reihe2_MI', 'AB_Gurtschloss__Reihe2_BF']
    count = 0

    for name in list:
        r = requests.get(url + '/signal/' + name + '/value')
        data = json.loads(json.dumps(r.json()))
        try:
            if data.get('measurement').get('value') == 2:
                count += 1
        except:
            continue

    return "Number of places in the car: " + str(count)

# determines whether the drives revs the car more than usual
# def higherRev(threshhold):