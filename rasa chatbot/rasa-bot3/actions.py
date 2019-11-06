from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import requests
import json
from rasa_core_sdk import Action
import mysql.connector
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.forms import FormAction
import requests
import json

import pypyodbc 
import pandas as pd
import numpy as np
logger = logging.getLogger(__name__)


cnxn = pypyodbc.connect("Driver={SQL Server Native Client 11.0};"
					"Server=10.0.1.210;"
					"Database=kayawell;"
					"uid=tl_01;pwd=pass@123")





sql="""SELECT SPE.Id AS WId,ExpertId AS WExpertId, PlanName AS WPlanName,RegularPrice AS WRegularPrice,SalePrice AS WSalePrice,
PackageDetails AS WPackageDetails,SPE.IsActive AS WIsActive,
D.DoctorName AS WDoctorName,
STUFF((
	SELECT ', ' +AM.MasterValue
	--CAST( ConditionId AS VARCHAR(12))
	FROM PlanConditionMapping PM
	 LEFT JOIN AllMaster AM ON PM.ConditionId=AM.MasterCode 
   WHERE SubscribeId = SPE.Id And  MasterType='Symptoms'
	FOR XML PATH('')
),1,1,'') AS WConditions,D.DoctorId as ExpertId,
(CASE WHEN  isnull(SPE.SolutionType,'') = 'Lab Test' Then 
STUFF((
	SELECT ', ' +AM.TestName		
	FROM PlanMapLabTest PM
	 LEFT JOIN LabMaster AM ON PM.LabTestId=AM.Id
  where SubscribeId = SPE.Id
	FOR XML PATH('')
),1,1,'') 
else ''  end  ) as Labtest
,(CASE WHEN  isnull(SPE.SolutionType,'') = 'Lab Test' Then 
STUFF((
	SELECT ', ' +AM.Title		
	FROM PlanMapVaccination PM
	 LEFT JOIN UserContentFAQ AM ON PM.Id=AM.Id
   WHERE SubscribeId = SPE.Id And AM.ContentType='8'
	FOR XML PATH('')
),1,1,'') 
else ''  end  ) as Vaccination
FROM SubscriptionPlanOfExperts SPE 
LEFT JOIN KayaDoctorProfile  D ON SPE.ExpertId=D.UserProfileId 
inner JOin Doctor doc on d.UserProfileId=doc.UserProfileId
WHERE
SPE.ExpertId='14440'
AND SPE.IsActive=1"""

df = pd.read_sql_query(sql,cnxn)


class ActionJoke(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_joke"

    def run(self, dispatcher, tracker, domain):
        # what your action should do
        request = requests.get('http://api.icndb.com/jokes/random').json() #make an apie call
        joke = request['value']['joke'] #extract a joke from returned json response
        dispatcher.utter_message(joke) #send the message back to the user
        return []


class ActionOrderProduct(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_order_product"

    def run(self, dispatcher, tracker, domain):
        product = tracker.get_slot('product')
        model = tracker.get_slot('model')
        response = "Your product is {}, model is {}. what do you want else related to database?".format(product, model)
        dispatcher.utter_message(response) #send the message back to the user
        return []
		
	
class ActionDatabase(Action):

    def name(self):
        return "action_test"

    def run(self, dispatcher, tracker, domain):
        conditions=tracker.get_slot('conditions')
       
        df2=df.loc[:,["wplanname","wconditions"]]
        dfx = df2[df2['wconditions'].str.contains("Diabetes")] 
        dfx = dfx.reset_index(drop=True)
        plan_name=dfx.wplanname.sample(n=2).to_string(index=False)
                
        msg = "Hi, we have full body check up: {} it covers all {}".format(plan_name,conditions)
        dispatcher.utter_message(msg)
        return []

class ActionPincode(Action):

    def name(self):
        return "action_pincode"

    def run(self, dispatcher, tracker, domain):
        pincode=tracker.get_slot('pincode')
        url="https://www.kayawell.com/Appointment/CheckThyrocarePinCodeAvailability?zipcode={}".format(pincode)
        
        response = requests.get(url)
        data = response.json()
        if data==True:
            msg = "{} our service is availabel in this pincode {}".format(data,pincode)
            dispatcher.utter_message(msg)
            return [] 
        else:
            msg = "{} our service is not availabel in this pincode {}".format(data,pincode)
            dispatcher.utter_message(msg)
            return [] 


      