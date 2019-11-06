# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 18:15:51 2019

@author: Manish
"""
from flask import Flask, request, jsonify
from sklearn.externals import joblib
import traceback
import pandas as pd
import numpy as np
from flask import request
from datetime import datetime
from flask_cors import CORS, cross_origin 
import sys
import os
import datetime
import calendar
import pickle
from flask import render_template, make_response
import datetime
import time
from dateutil import relativedelta
from flask import Flask, session, jsonify, request
import os
import traceback
import json
import requests

import mysql.connector

import requests
#training

from rasa_nlu.training_data import load_data
from rasa_nlu.model import Trainer
from rasa_nlu import config
from rasa_nlu.model import Interpreter



# Your API definition
app = Flask(__name__)
#for localhost
cors = CORS(app, resources={r"/": {"origins": "http://localhost:5000"}})


# Your API definition
app = Flask(__name__)
#for localhost
cors = CORS(app, resources={r"/": {"origins": "http://localhost:5000"}})

"""
@app.route('/train', methods=['POST','GET'])
@cross_origin(origin='localhost')


def train_rasa():

    training_data = load_data("data\nlu.md")

    trainer = Trainer(config.load("config.yml"))

    trainer.train(training_data)

    model_directory = trainer.persist("models")
    print("data trained successfully")

    return model_directory
"""
@app.route('/intent', methods=['POST','GET'])
@cross_origin(origin='localhost')

def intent():
    try:
    
        url="http://localhost:5005/model/parse"
        #json content
        headers = {'content-type': 'application/json'}
   
        #json input in postman
       #json input in postman
        json_input = request.json
        inp_msg  = json_input["text"]
        print("1",inp_msg)
    
        in_json = {"text" : inp_msg}
        #return_list_of_dicts.append(out_dict)
            #out_json = json.dumps(out_dict,ensure_ascii= False)
        in_json = json.dumps(in_json,ensure_ascii= False)

        response = requests.request("POST", url, data=in_json, headers=headers)
        print("2",response)
        print("3",response.status_code)
        print("4",response.text)
        print("5",response.json())  
        
        #parsed json for finding intent and entities
        #print(response.text)
        json_response=response.text
       
        parsed_json = (json.loads(json_response))
        print(json.dumps(parsed_json))
        intent= parsed_json["intent"]
        entities= parsed_json["entities"]
        print("intent:", intent)
        
        
        print("entities:", entities)
       #json response in postman

        return jsonify(response.json())
    
        #return jsonify(response.text)

        #return jsonify(intent)
        #return jsonify(entities)






    except:
        return jsonify({'trace': traceback.format_exc()})

@app.route('/html', methods=['POST','GET'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])

def html():
    return render_template("index.html")




@app.route('/chat', methods=['POST','GET'])
@cross_origin(origin='localhost')

def chat():
    try:
        
        #rasa url

        url = "http://localhost:5005/webhooks/rest/webhook/"
        #json content
        headers = {'content-type': 'application/json'}
    
        #payload = "{ \"message\": \" i want to do engineering\"}"
        
        #json input in postman
        json_input = request.json
        inp_msg  = json_input["message"]
        print("1",inp_msg)
    
        in_json = {"message" : inp_msg}
        print(in_json)
        #return_list_of_dicts.append(out_dict)
            #out_json = json.dumps(out_dict,ensure_ascii= False)
        in_json = json.dumps(in_json,ensure_ascii= False)
        print("2", in_json)
        
        response = requests.request("POST", url, data=in_json, headers=headers)
        #print(response)
        #print("3",response.status_code)
        #print("4",response.text)
        print("5",response.json())   
        
        
        #parsed reply json fro bot
        #print(response.text)
        json_response=response.text
       
        parsed_json = (json.loads(json_response))
        print(json.dumps(parsed_json))
        replied= parsed_json[0]
        print("reply:", replied)
        
        
        
        #database insertion
        
        def insert_rasadb():
                             #database connection

            try:
                local_connection = mysql.connector.connect(
                                                           host="localhost",
                                                           user="root",
                                                           passwd="",
                                                           database="rasadb"
                                                           )
                local_cursor = local_connection.cursor()
                sql = "insert into rasatb (message, reply) values ('%s','%s')" %(inp_msg,replied)
                
                print (sql)
                # Execute dml and commit changes
                local_cursor.execute(sql,json_input)
                local_connection.commit()
                local_cursor.close()  
                
                print("recorded successfully into rasatb table ")
            except mysql.connector.Error as error:
                print("Failed to insert into MySQL table {}".format(error))

            finally:
                if (local_connection.is_connected()):
                    
                    local_cursor.close()
                    local_connection.close()
                    print("MySQL connection is closed")
                    
                    
        insert_rasadb()
                    
                    
            
                        
                
            
        
        
        #json response in postman
        return jsonify(response.json())
        #return jsonify(response.text)

        #return jsonify(replied)






    except:
        return jsonify({'trace': traceback.format_exc()})

 


if __name__ == '__main__':
    app.run()

