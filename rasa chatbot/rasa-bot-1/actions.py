# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import requests
import json
from rasa_core_sdk import Action
import mysql.connector

logger = logging.getLogger(__name__)


class ActionJoke(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_joke"

    def run(self, dispatcher, tracker, domain):
        # what your action should do
        request = json.loads(requests.get('https://api.chucknorris.io/jokes/random').text)  # make an api call
        joke = request['value']  # extract a joke from returned json response
        dispatcher.utter_message(joke)  # send the message back to the user
        return []





class ActionId(Action):

    def name(self):
        return "action_id"

    def run(self, dispatcher, tracker, domain):
        local_connection = mysql.connector.connect(
												   host="localhost",
												   user="root",
												   passwd="",
												   database="rasadb")
        local_cursor = local_connection.cursor()
        sql="select message from rasatb WHERE UserId=2"
        local_cursor.execute(sql)
        myresult = local_cursor.fetchall()
        name=myresult[0][0]
        msg = 'Hello {}!'.format(name)
        dispatcher.utter_message(msg)
        return []




		

