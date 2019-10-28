from gevent.monkey import patch_all
patch_all()
from gevent.local import local
from psycogreen.gevent import patch_psycopg
patch_psycopg()

from flask import Flask, request, render_template
from flask_cors import CORS

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson import ApiException
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, RelationsOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from os import urandom, environ
import datetime as dt
import json

import tables_wks

''' 
    Flask Server Configuration 
'''
flask_server = Flask(__name__)
flask_server.config['SECRET_KEY'] = urandom(16)
flask_server.config['WTF_CSRF_SECRET_KEY'] = urandom(16)
CORS(flask_server)

''' 
    Flask Server Routes 
'''

@flask_server.route("/", methods=['GET', 'POST'])
def root():
    now = dt.datetime.utcnow() - dt.timedelta(hours=3)
    now_str = dt.datetime.strftime(now, "%H:%M:%S - %d/%m/%Y")
    idented_resp = None
    idented_models = None
    msg = None
    if request.method == 'POST':
        #print(request.form)
        try:
            # Extract form data
            nlu_apikey = request.form['nlu_apikey']
            nlu_url = request.form['nlu_url']
            custom_model = request.form['custom_model']
            limit = request.form['limit']
            mentions = request.form['mentions']
            sentiment = request.form['sentiment']
            emotion = request.form['emotion']
            data = request.form['data']
            flag = "both"

            # Build NLU object:
            authenticator = IAMAuthenticator(nlu_apikey)
            nlu_object = NaturalLanguageUnderstandingV1(version='2019-07-12', authenticator=authenticator)
            nlu_object.set_service_url(nlu_url)
            
            # List models:
            model_list = nlu_object.list_models().get_result()
            if len(model_list['models']) != 0:
                idented_models = json.dumps(model_list, indent=2)
            #print(model_list)
            #print(type(model_list))
            #print(model_list['models'])
            #print(type(model_list['models']))

            # Execute API Call to NLU
            if custom_model != "default":
                response = nlu_object.analyze(
                    text=data, 
                    features=Features(
                        entities=EntitiesOptions(limit=int(limit), mentions=mentions, model=custom_model, sentiment=sentiment, emotion=emotion), 
                        relations=RelationsOptions(model=custom_model)
                    )
                ).get_result()
                # Entities Table
                entities_table = tables_wks.gen_entities_table(response["entities"])
                # Relations Table
                relations_table = tables_wks.gen_relations_table(response["relations"])
            else:
                response = nlu_object.analyze(
                    text=data, 
                    features=Features(
                        entities=EntitiesOptions(limit=int(limit), mentions=mentions, sentiment=sentiment, emotion=emotion), 
                        relations=RelationsOptions()
                    )
                ).get_result()
                #print(json.dumps(response, indent=2))
                #print(response["entities"])
                #print(response["relations"])
                # Entities Table
                entities_table = tables_wks.gen_entities_table(response["entities"])
                # Relations Table
                relations_table = tables_wks.gen_relations_table(response["relations"])
        except ApiException as ex:
            msg = ex.message
        finally:
            if msg != None:
                return render_template(
                    'form.html',
                    msg=msg, 
                    timestamp=now_str
                )
            else:
                return render_template(
                    'result.html',
                    relations_table = relations_table,
                    entities_table = entities_table,
                    data=data,
                    model=custom_model,
                    model_list=idented_models,
                    msg=msg, 
                    timestamp=now_str
                )
    else:
        return render_template('form.html')


''' 
    Main 
'''
if __name__ == '__main__':
    flask_server.run(
        host="0.0.0.0", 
        port=int(environ.get("PORT", 5000)), 
        debug=False
    )
