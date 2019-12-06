## story_greet <!--- The name of the story. It is not mandatory, but useful for debugging. --> 
* greet <!--- User input expressed as intent. In this case it represents users message 'Hello'. --> 
 - utter_name <!--- The response of the chatbot expressed as an action. In this case it represents chatbot's response 'Hello, how can I help?' --> 

## story_name
* names{"name":"Sam"}
 - utter_greet
 

## story_test_02
* test{"conditions":"diabetes"}
- action_test

## story_pincode_03
* pins{"pin":"302029"}
 - action_pin
 
## story_booking_00
* ask_book_0
 - appointment_form
 - form{"name": "appointment_form"}
 - form{"name": null}
 - utter_slots_values
 - action_book_apiask_book_0
 - utter_book_confirm
 
 ## story_booking_01
* ask_book_1
 - appointment_form
 - form{"name": "appointment_form"}
 - form{"name": null}
 - utter_slots_values
 - action_book_apiask_book_1
 - utter_book_confirm


 ## story_booking_02
* ask_book_2
 - appointment_form
 - form{"name": "appointment_form"}
 - form{"name": null}
 - utter_slots_values
 - action_book_apiask_book_2
 - utter_book_confirm
 
 
  ## story_booking_03
* ask_book_3
 - appointment_form
 - form{"name": "appointment_form"}
 - form{"name": null}
 - utter_slots_values
 - action_book_apiask_book_3
 - utter_book_confirm
 
  ## story_booking_04
* ask_book_4
 - appointment_form
 - form{"name": "appointment_form"}
 - form{"name": null}
 - utter_slots_values
 - action_book_apiask_book_4
 - utter_book_confirm
 - utter_book_confirm
 
 ## story_booking_05
* ask_book_5
 - appointment_form
 - form{"name": "appointment_form"}
 - form{"name": null}
 - utter_slots_values
 - action_book_apiask_book_5
 - utter_book_confirm
 

## story_till_pincode
* greet
 - utter_name
* names{"name":"Sam"}
 - utter_greet
* test{"conditions":"liver cancer"}
 - action_test
 - utter_ask_pin
 - action_button
* pins{"pin":"302029"}
 - action_pin
* ask_package_price
 - action_price
* ask_no_test
 - action_test
* ask_home_charge
 - utter_ask_home_charge
 - utter_ask_book_interest
* ask_book_0
 - appointment_form
 - form{"name": "appointment_form"}
 - form{"name": null}
 - utter_slots_values
 - action_book_apiask_book_0
 - utter_book_confirm
* ask_book_1
 - appointment_form
 - form{"name": "appointment_form"}
 - form{"name": null}
 - utter_slots_values
 - action_book_apiask_book_1
 - utter_book_confirm
 * ask_book_2
 - appointment_form
 - form{"name": "appointment_form"}
 - form{"name": null}
 - utter_slots_values
 - action_book_apiask_book_2
 - utter_book_confirm
 * ask_book_3
 - appointment_form
 - form{"name": "appointment_form"}
 - form{"name": null}
 - utter_slots_values
 - action_book_apiask_book_3
 - utter_book_confirm
  * ask_book_4
 - appointment_form
 - form{"name": "appointment_form"}
 - form{"name": null}
 - utter_slots_values
 - action_book_apiask_book_4
 - utter_book_confirm
 * ask_book_5
 - appointment_form
 - form{"name": "appointment_form"}
 - form{"name": null}
 - utter_slots_values
 - action_book_apiask_book_5
 - utter_book_confirm
* book_confirm
 - action_book_api
 - utter_book_congrats
* thank
 - utter_thanks
* bye
 - utter_goodbye 

## story_thanks
* thank
 - utter_thanks

## story_goodbye
* bye
 - utter_goodbye

## story_till_book
* greet
 - utter_name
* names{"name":"Sam"}
 - utter_greet
* test{"conditions":"liver cancer"}
 - action_test
 - utter_ask_pin
 - action_button
* pins{"pin":"302029"}
 - action_pin
* ask_package_price
 - action_price
* ask_no_test
 - action_test
* ask_home_charge
 - utter_ask_home_charge
 - utter_ask_book_interest
* ask_book_0
 - appointment_form
 - form{"name": "appointment_form"}
 - form{"name": null}
 - utter_slots_values
 - action_book_apiask_book_0
 - utter_book_confirm
* ask_book_1
 - appointment_form
 - form{"name": "appointment_form"}
 - form{"name": null}
 - utter_slots_values
 - action_book_apiask_book_1
 - utter_book_confirm
 * ask_book_2
 - appointment_form
 - form{"name": "appointment_form"}
 - form{"name": null}
 - utter_slots_values
 - action_book_apiask_book_2
 - utter_book_confirm
* ask_book_3
 - appointment_form
 - form{"name": "appointment_form"}
 - form{"name": null}
 - utter_slots_values
 - action_book_apiask_book_3
 - utter_book_confirm
 * ask_book_4
 - appointment_form
 - form{"name": "appointment_form"}
 - form{"name": null}
 - utter_slots_values
 - action_book_apiask_book_4
 - utter_book_confirm
 * ask_book_5
 - appointment_form
 - form{"name": "appointment_form"}
 - form{"name": null}
 - utter_slots_values
 - action_book_apiask_book_5
 - utter_book_confirm
* book_confirm
 - utter_book_congrats
* thank
 - utter_thanks
* bye
 - utter_goodbye 
 
 
 


