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


sql="""SELECT  PageHits,'https://www.kayawell.com/Data/PlanImage/'+PlanImage as PlanImage, 'https://www.kayawell.com/Wellness/'+SPE.planslug as Slug , SPE.Id AS WId,ExpertId AS WExpertId, PlanName AS WPlanName,RegularPrice AS WRegularPrice,SalePrice AS WSalePrice,
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


	
class ActionDatabase(Action):
 
    def name(self):
        return "action_test"

    def run(self, dispatcher, tracker, domain):
        
        conditions=tracker.get_slot('conditions') 
        df_p = df_rsp[df_rsp['wconditions'].str.contains(conditions)] 
        df_pwp=df_p.nlargest(1, ['pagehits']) 

        p_plane=df_pwp.iloc[:,0].to_string(index=False)
        ls_p_plane.append(p_plane)
        
        pr_price=df_pwp.iloc[:,2].to_string(index=False)
        ls_pr_price.append(pr_price)
        
        ps_price=df_pwp.iloc[:,3].to_string(index=False)
        ls_ps_price.append(ps_price)
        
        p_image=df_pwp.iloc[:,4].to_string(index=False)
        ls_p_image.append(p_image)
        
        p_slug=df_pwp.iloc[:,5].to_string(index=False)
        ls_p_slug.append(p_slug)

        msg = "{} it covers all {} test. Free home sample collection".format(ls_p_plane[0],conditions)
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
		
		
class ActionBookApi(Action):

    def name(self):
        return "action_book_api"

    def run(self, dispatcher, tracker, domain):
        
        alex={
            "Data": {
                "ADDRESS": "8A SHRIGOPLA NAGAR JAIPUR",
                "BOOKED_BY": "MANISH KUMAR",
                "CUSTOMER_RATE": 650,
                "EMAIL": "8107290310@doxif.com",
                "FASTING": "FASTING",
                "MOBILE": "8107290310",
                "MODE": "PAY WHILE SAMPLE COLLECTION",
                "ORDERRESPONSE": {
                    "PostOrderDataResponse": [
                        {
                            "AGE": "24",
                            "GENDER": "F",
                            "LEAD_ID": "SP47894487",
                            "NAME": "manish kumar"
                        }
                    ]
                },
                "ORDER_NO": "KAYAW04730",
                "PAY_TYPE": "POSTPAID",
                "PRODUCT": "AAROGYAM B",
                "REF_ORDERID": "9E2DBB",
                "REPORT_HARD_COPY": "NO",
                "RESPONSE": "SUCCESS",
                "RES_ID": "RES0000",
                "SERVICE_TYPE": "HOME COLLECTION",
                "STATUS": "YET TO CONFIRM"
            },
            "Errors": [],
            "Success": "true",
            "PageCount": 0,
            "PageIndex": 0,
            "PageSize": 0,
            "ItemCount": 0,
            "TotalAmount": 0.0,
            "TotalEarning": 0.0
        }
                    
        oid=alex["Data"]["ORDER_NO"]
        msg = "Congratulations! Your order is booked succesfully and your Order id is {}".format(oid)
        dispatcher.utter_message(msg)
        return []
		

class ActionLink(Action):

    def name(self):
        return "action_link"

    def run(self, dispatcher, tracker, domain):
        image1="https://www.kayawell.com/Data/PlanImage/2018/6/76472dcd-8c98-42ed-a48a-039ef3c967c2.jpg"
        slug1="https://www.kayawell.com/Wellness/kayawell-lab/lowest-price/basic-full-body-checkup-60-tests"
        image2="https://www.kayawell.com/Data/PlanImage/2018/8/c44996d5-3acc-4af1-9be8-7302f9772f11.jpg"
        slug2="https://www.kayawell.com/Wellness/kayawell-lab/lowest-price-ln-hi/basic-full-body-checkup-60-tests"
        image3="https://www.kayawell.com/Data/PlanImage/2018/8/44e3a9cd-953a-4e6b-8d1a-310a610e96d2.jpg"
        slug3="https://www.kayawell.com/Wellness/kayawell-lab/lowest-price-ln-hi/advanced-full-body-checkup-128-tests"
        #url=str(ls_p_image[0])
        #slashparts = url.split('/')
        #var="https://www.kayawell.com/Data/PlanImage/{}".format('/'.join(slashparts[5:]) + '/')
        #dispatcher.utter_message('<a href="'+slug+'"  > <img src="'+image+'" width="200" height="100"></a><div  class="container" style="max-width:450px" >  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css"> <style type="text/css"> 	.btn-1{       display: block;       background:#07bab7;       padding: 10px 10px; color: #fff; 	} 	.btn-2{  display: block;       background:#ed4a52;       padding: 10px 10px;       color: #fff; 	} 	.padlr{ 		padding-left: 0px; 		padding-right: 0px; 	} 	.norow{ 		margin-left: 0px; 		margin-right:0px; 	} 	.carousel-control .glyphicon-chevron-left{     left: 10%;     margin-left: -10px; } .carousel-control .glyphicon-chevron-right {     right: 10%;     margin-right: -10px; } .carousel-indicators {      bottom: 27px;    }  </style>    <div id="myCarousel" class="carousel slide" data-ride="carousel">        <!-- Wrapper for slides -->     <div class="carousel-inner" >       <div class="item active row norow" >        	 		<div class="col-xs-6 padlr"> 			<div class="col-xs-12 padlr"><a target="_blank" href="javascript:void(0)"> 			<img src="https://www.kayawell.com/Data/PlanImage/2018/7/007736e7-a6c3-48af-ae0b-236b4aa9b8ad.jpg" class="img-responsive" /></a></div> 			<div class="col-xs-6 padlr"><a href="javascript:void(0)" class="btn-1" onclick="checkMyPlanName(0)">View More</a></div> 			<div class="col-xs-6 padlr"> 				<a href="javascript:void(0)" class="btn-2">Book Now</a> 			</div>       	</div>       		                    </div>        <div class="item row norow" >           	       		<div class="col-xs-6 padlr">       	<div class="col-xs-12 padlr"><a target="_blank" href="javascript:void(0)"><img src="https://www.kayawell.com/Data/PlanImage/2018/7/007736e7-a6c3-48af-ae0b-236b4aa9b8ad.jpg" class="img-responsive" /></a></div>       		<div class="col-xs-6 padlr"><a href="javascript:void(0)" class="btn-1" onclick="checkMyPlanName(1)">View More</a></div>       		<div class="col-xs-6 padlr">       			<a href="javascript:void(0)" class="btn-2">Book Now</a>       		</div>       	</div>       		       </div>           <div class="item row norow" >             	       		<div class="col-xs-6 padlr">       	<div class="col-xs-12 padlr"><a target="_blank" href="https://www.kayawell.com/Wellness/kayawell-lab/lowest-price/advanced-full-body-checkup-128-tests"><img src="https://www.kayawell.com/Data/PlanImage/2018/7/007736e7-a6c3-48af-ae0b-236b4aa9b8ad.jpg" class="img-responsive" /></a></div>       		<div class="col-xs-6 padlr"><a href="javascript:void(0)" class="btn-1" onclick="checkMyPlanName(2)">View More</a></div>       		<div class="col-xs-6 padlr">       			<a href="javascript:void(0)" class="btn-2">Book Now</a>       		</div>       	</div>       		     </div>      <!-- Left and right controls -->     <a class="left carousel-control" href="#myCarousel" data-slide="prev">       <span class="glyphicon glyphicon-chevron-left"></span>       <span class="sr-only">Previous</span>     </a>     <a class="right carousel-control" href="#myCarousel" data-slide="next">       <span class="glyphicon glyphicon-chevron-right"></span>       <span class="sr-only">Next</span>     </a>   </div>    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>   <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"></script> </div>') 
        dispatcher.utter_message('<div  class="container" style="max-width:450px" >  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css"> <style type="text/css"> 	.btn-1{       display: block;       background:#07bab7;       padding: 10px 10px; color: #fff; 	} 	.btn-2{  display: block;       background:#ed4a52;       padding: 10px 10px;       color: #fff; 	} 	.padlr{ 		padding-left: 0px; 		padding-right: 0px; 	} 	.norow{ 		margin-left: 0px; 		margin-right:0px; 	} 	.carousel-control .glyphicon-chevron-left{     left: 10%;     margin-left: -10px; } .carousel-control .glyphicon-chevron-right {     right: 10%;     margin-right: -10px; } .carousel-indicators {      bottom: 27px;    }  </style>    <div id="myCarousel" class="carousel slide" data-ride="carousel">        <!-- Wrapper for slides -->     <div class="carousel-inner" >       <div class="item active row norow" >        	 		<div class="col-xs-6 padlr"> 			<div class="col-xs-12 padlr"><a target="_blank" href="javascript:void(0)"> 			<img src="'+image1+'" class="img-responsive" /></a></div> 			<!-- <div class="col-xs-6 padlr"><a href="javascript:void(0)" class="btn-1" >View More</a></div> --> 			<div class="col-xs-12 padlr"> 				<a href="javascript:void(0)" class="btn-2" onclick="checkMyPlanName(0)">Book Now</a> 			</div>       	</div>       		                    </div>        <div class="item row norow" >           	       		<div class="col-xs-6 padlr">       	<div class="col-xs-12 padlr"><a target="_blank" href="javascript:void(0)"> 		<img src="'+image2+'" class="img-responsive"/></a></div>       		<!-- <div class="col-xs-6 padlr"><a href="javascript:void(0)" class="btn-1" onclick="checkMyPlanName(1)">View More</a></div> -->       		<div class="col-xs-12 padlr">       			<a href="javascript:void(0)" class="btn-2" onclick="checkMyPlanName(1)">Book Now</a>       		</div>       	</div>       		       </div>           <div class="item row norow" >             	       		<div class="col-xs-6 padlr">       	<div class="col-xs-12 padlr"> 		<a target="_blank" href="javascript:void(0)"> 		<img src="'+image3+'" class="img-responsive" /></a></div>       		<!-- <div class="col-xs-6 padlr"><a href="javascript:void(0)" class="btn-1" onclick="checkMyPlanName(2)">View More</a></div>-->       		<div class="col-xs-12 padlr">       			<a href="javascript:void(0)" class="btn-2" onclick="checkMyPlanName(2)">Book Now</a>       		</div>       	</div>       		     </div>      <!-- Left and right controls -->     <a class="left carousel-control" href="#myCarousel" data-slide="prev">       <span class="glyphicon glyphicon-chevron-left"></span>       <span class="sr-only">Previous</span>     </a>     <a class="right carousel-control" href="#myCarousel" data-slide="next">       <span class="glyphicon glyphicon-chevron-right"></span>       <span class="sr-only">Next</span>     </a>   </div>    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>   <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"></script> </div>') 

        return []
		
class ActionButton(Action):

    def name(self):
        return "action_button"

    def run(self, dispatcher, tracker, domain):
        
        buttons = [{"title": "book1", "payload": "/pins"}, {"title": "book2", "payload": "/bye"}]
        dispatcher.utter_button_message("There are 2 people with the name Rohan:", buttons)
        
        return []
