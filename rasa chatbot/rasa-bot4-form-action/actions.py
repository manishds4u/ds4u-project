from typing import Dict, Text, Any, List, Union, Optional
from rasa_core_sdk import Action

from rasa_core_sdk import ActionExecutionRejection
from rasa_core_sdk import Tracker
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.executor import CollectingDispatcher
from rasa_core_sdk.forms import FormAction, REQUESTED_SLOT

class RestaurantForm(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "appointment_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["fname", "lname","contact", "email", "age", "pincode"]

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




class ActionName(Action):

    def name(self):
        return "action_name"

    def run(self, dispatcher, tracker, domain):
        nam=tracker.get_slot('fname')
        msg = "{} our service is availabel in this name".format(nam)
        dispatcher.utter_message(msg)
        return [] 
 