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

from typing import Dict, Text, Any, List, Union, Optional
from rasa_core_sdk import Action

from rasa_core_sdk import ActionExecutionRejection
from rasa_core_sdk import Tracker
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.executor import CollectingDispatcher
from rasa_core_sdk.forms import FormAction, REQUESTED_SLOT
logger = logging.getLogger(__name__)


cnxn = pypyodbc.connect("Driver={SQL Server Native Client 11.0};"
					"Server=10.0.1.210;"
					"Database=kayawell;"
					"uid=tl_01;pwd=pass@123")


sql="""SELECT  PageHits,PlanImage as PlanImage, 'https://www.kayawell.com/Wellness/'+SPE.planslug as Slug , SPE.Id AS WId,ExpertId AS WExpertId, PlanName AS WPlanName,RegularPrice AS WRegularPrice,SalePrice AS WSalePrice,
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
df_rsp=df.loc[:,["wplanname","wconditions","wregularprice","wsaleprice","planimage","slug","pagehits"]]
df_rsp['wconditions'] = df_rsp['wconditions'].map(lambda x: x.lower())

ls_p_plane=[]
ls_pr_price=[]
ls_ps_price=[]
ls_p_image=[]
ls_p_slug=[]



#buttons
but_all=[]
buttons = [{"title": "Book0", "payload": "/ask_book_0"}, {"title": "Book1", "payload": "/ask_book_1"}, {"title": "Book2", "payload": "/ask_book_2"}]

#button_0
but0=[]
but0.append(buttons[0])
but_all.append(but0)

#button_1
but1=[]
but1.append(buttons[1])
but_all.append(but1)

#button_2
but2=[]
but2.append(buttons[2])
but_all.append(but2)


class ActionDatabase(Action):
 
    def name(self):
        return "action_test"

    def run(self, dispatcher, tracker, domain):
        
        conditions=tracker.get_slot('conditions') 
        df_p = df_rsp[df_rsp['wconditions'].str.contains(conditions)] 
        df_pwp=df_p.nlargest(3, ['pagehits']) 

        #planname
        p_plane=df_pwp.iloc[:,0].to_string(index=False)
        p_plane=p_plane.splitlines()
        for i in p_plane:
            ls_p_plane.append(i.lstrip())
            
        #planeprice
        pr_price=df_pwp.iloc[:,2].to_string(index=False)
        pr_price=pr_price.splitlines()
        for i in pr_price:
            ls_pr_price.append(i.lstrip())
            
        #plane_price
        ps_price=df_pwp.iloc[:,3].to_string(index=False)
        ps_price=ps_price.splitlines()
        for i in ps_price:
            ls_ps_price.append(i.lstrip())
            
        
        #plane_image
        p_image=df_pwp.iloc[:,4].to_string(index=False)
        p_image=p_image.splitlines()
        for i in p_image:
            ls_p_image.append(i.lstrip())
        
        
        #plane_slug
        p_slug=df_pwp.iloc[:,5].to_string(index=False)
        p_slug=p_slug.splitlines()
        for i in p_slug:
            ls_p_slug.append(i.lstrip())

        msg = "Yes, We have most popular packages according your {} related query. {} test. Free home sample collection".format(conditions,ls_p_plane[0])
        dispatcher.utter_message(msg)
        return []

class ActionPincode(Action):

    def name(self):
        return "action_pin"

    def run(self, dispatcher, tracker, domain):
        pin=tracker.get_slot('pin')
        url="https://www.kayawell.com/Appointment/CheckThyrocarePinCodeAvailability?zipcode={}".format(pin)
        
        response = requests.get(url)
        data = response.json()
        if data==True:
            msg = "Yes our service is availabel in this pincode {}".format(pin)
            dispatcher.utter_message(msg)
            return [] 
        else:
            msg = "No our service is not availabel in this pincode {}".format(pin)
            dispatcher.utter_message(msg)
            return [] 
		
		
class ActionPackagePrice(Action):

    def name(self):
        return "action_price"

    def run(self, dispatcher, tracker, domain):
        
        msg = "regular price:{} INR and sale price:{} INR".format(ls_pr_price[0],ls_ps_price[0])
        dispatcher.utter_message(msg)
        return []




class RestaurantForm(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "appointment_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["fname", "lname","contact", "email", "age", "pincode", "address"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
			
            or a list of them, where a first match will be picked"""

        return {
            "fname": [
                self.from_entity(entity="fname"),
                self.from_intent(intent="fnames", value=True),
                self.from_intent(intent="deny", value=False),
            ],
			"lname": [
                self.from_entity(entity="lname"),
                self.from_intent(intent="lnames", value=True),
                self.from_intent(intent="deny", value=False),
            ],
			
            "contact": [
                self.from_entity(entity="contact"),
                self.from_intent(intent="contacts", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "email": [
                self.from_entity(entity="email"),
                self.from_intent(intent="emails", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "age": [
                self.from_entity(entity="age"),
                self.from_intent(intent="ages", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "pincode": [ self.from_entity(entity="pincode"),
                self.from_intent(intent="pincodes", value=True),
                self.from_intent(intent="deny", value=False),
			],
            "address": [ self.from_entity(entity="address"),
                self.from_intent(intent="addresses", value=True),
                self.from_intent(intent="deny", value=False),
			]
        }

    
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        dispatcher.utter_template("utter_submit", tracker)
        return []
		
		
class ActionBookApi_0(Action):

    def name(self):
        return "action_book_apiask_book_0"

    def run(self, dispatcher, tracker, domain): 
        fname=tracker.get_slot('fname')
        lname=tracker.get_slot('lname')
        contact=tracker.get_slot('contact')
        email=tracker.get_slot('email')
        age=tracker.get_slot('age')
        address=tracker.get_slot('address')
        pincode=tracker.get_slot('pincode')
        print(fname)
        print(email)
        print(age)
        
        url = "https://www.kayawell.com/api/ExpertLoginApi/SaveWellnessOrderByCRM"
        
        payload = [{
        	"PlanId": "507",
        	"PlanName": str(ls_p_plane[0]),
        	"FirstName": str(fname),
        	"LastName": str(lname),
        	"MemberEmail": str(email),
        	"MemberMobile": str(contact),
        	"OrderStatus": "Booked",
        	"Address": str(address),
        	"Pincode": str(pincode),
        	"Gender": "",
        	"age": str(age),
        	"AppinmentDate": "2019-11-22 00:00:00",
        	"ExTOrderId": "",
        	"ReachMeOn": "6367251642",
        	"IsHardCopy": "No",
        	"PlanDescription": "null",
        	"ExecutiveId" : "FB-CB",
        	"ExecutiveName" : "FB ChatBot"
        }]
        
        headers = {'Content-Type': "application/json"}
        in_json = json.dumps(payload,ensure_ascii= False)
        
        print(in_json)
        response = requests.post(url, data=in_json, headers=headers)
        
        print(response)
        out_json=response.json()
        print(out_json)
        result=out_json["Success"]
        msg = "{} your reservation is now booked".format(result)
        dispatcher.utter_message(msg)
        return []

class ActionBookApi_1(Action):

    def name(self):
        return "action_book_apiask_book_1"

    def run(self, dispatcher, tracker, domain): 
        fname=tracker.get_slot('fname')
        lname=tracker.get_slot('lname')
        contact=tracker.get_slot('contact')
        email=tracker.get_slot('email')
        age=tracker.get_slot('age')
        address=tracker.get_slot('address')
        pincode=tracker.get_slot('pincode')
        print(fname)
        print(email)
        print(age)
        
        url = "https://www.kayawell.com/api/ExpertLoginApi/SaveWellnessOrderByCRM"
        
        payload = [{
        	"PlanId": "507",
        	"PlanName": str(ls_p_plane[1]),
        	"FirstName": str(fname),
        	"LastName": str(lname),
        	"MemberEmail": str(email),
        	"MemberMobile": str(contact),
        	"OrderStatus": "Booked",
        	"Address": str(address),
        	"Pincode": str(pincode),
        	"Gender": "",
        	"age": str(age),
        	"AppinmentDate": "2019-11-22 00:00:00",
        	"ExTOrderId": "",
        	"ReachMeOn": "6367251642",
        	"IsHardCopy": "No",
        	"PlanDescription": "null",
        	"ExecutiveId" : "FB-CB",
        	"ExecutiveName" : "FB ChatBot"
        }]
        
        headers = {'Content-Type': "application/json"}
        in_json = json.dumps(payload,ensure_ascii= False)
        
        print(in_json)
        response = requests.post(url, data=in_json, headers=headers)
        
        print(response)
        out_json=response.json()
        print(out_json)
        result=out_json["Success"]
        msg = "{} your reservation is now booked".format(result)
        dispatcher.utter_message(msg)
        return []

class ActionBookApi_2(Action):

    def name(self):
        return "action_book_apiask_book_2"

    def run(self, dispatcher, tracker, domain): 
        #intent = tracker.latest_message['intent'].get('name')

        # retrieve the correct chitchat utterance dependent on the intent
        #if intent in ['ask_book_0', 'ask_book_1', 'ask_book_2']:
                    
        fname=tracker.get_slot('fname')
        lname=tracker.get_slot('lname')
        contact=tracker.get_slot('contact')
        email=tracker.get_slot('email')
        age=tracker.get_slot('age')
        address=tracker.get_slot('address')
        pincode=tracker.get_slot('pincode')
        print(fname)
        print(email)
        print(age)
        
        url = "https://www.kayawell.com/api/ExpertLoginApi/SaveWellnessOrderByCRM"
        
        payload = [{
        	"PlanId": "507",
        	"PlanName": str(ls_p_plane[2]),
        	"FirstName": str(fname),
        	"LastName": str(lname),
        	"MemberEmail": str(email),
        	"MemberMobile": str(contact),
        	"OrderStatus": "Booked",
        	"Address": str(address),
        	"Pincode": str(pincode),
        	"Gender": "",
        	"age": str(age),
        	"AppinmentDate": "2019-11-22 00:00:00",
        	"ExTOrderId": "",
        	"ReachMeOn": "6367251642",
        	"IsHardCopy": "No",
        	"PlanDescription": "null",
        	"ExecutiveId" : "FB-CB",
        	"ExecutiveName" : "FB ChatBot"
        }]
        
        headers = {'Content-Type': "application/json"}
        in_json = json.dumps(payload,ensure_ascii= False)
        
        print(in_json)
        response = requests.post(url, data=in_json, headers=headers)
        
        print(response)
        out_json=response.json()
        print(out_json)
        result=out_json["Success"]
        msg = "{} your reservation is now booked".format(result)
        dispatcher.utter_message(msg)
        return []
    
    
class ActionLinkx(Action):

    def name(self):
        return "action_link_0"

    def run(self, dispatcher, tracker, domain):
        url_img_0=str(ls_p_image[0])
        img_0="https://www.kayawell.com/Data/PlanImage/{}".format(url_img_0.lstrip())
        button_0 = but_all[0]
        dispatcher.utter_button_message('<img src="'+img_0+'" width="200" height="100">', button_0)

        return []
		
		
class ActionLinky(Action):

    def name(self):
        return "action_link_1"
    def run(self, dispatcher, tracker, domain):
        url_img_1=str(ls_p_image[1])
        img_1="https://www.kayawell.com/Data/PlanImage/{}".format(url_img_1.lstrip())
        button_1=but_all[1]
        dispatcher.utter_button_message('<img src="'+img_1+'" width="200" height="100">',button_1)
        return []


		
class ActionLinkz(Action):

    def name(self):
        return "action_link_2"
    def run(self, dispatcher, tracker, domain):
        url_img_2=str(ls_p_image[2])
        img_2="https://www.kayawell.com/Data/PlanImage/{}".format(url_img_2.lstrip())
        button_2=but_all[2]
        dispatcher.utter_button_message('<img src="'+img_2+'" width="200" height="100">', button_2)
        #dispatcher.utter_message('<img src="'+img_2+'" width="200" height="100">')

        return []
    
    
    
    


