## story_greet <!--- The name of the story. It is not mandatory, but useful for debugging. --> 
* greet <!--- User input expressed as intent. In this case it represents users message 'Hello'. --> 
 - utter_name <!--- The response of the chatbot expressed as an action. In this case it represents chatbot's response 'Hello, how can I help?' --> 

## story_name
* name{"name":"Sam"}
 - utter_greet
 

## story_test_02
* test{"conditions":"diabetes"}
- action_test

## story_pincode_03
* pins{"pin":"302029"}
 - action_pin
 


## story_till_pincode
* greet
 - utter_name
 - action_button
* name{"name":"Sam"}
 - utter_greet
* test{"conditions":"liver cancer"}
 - action_test
 - utter_ask_pin
* pins{"pin":"302029"}
 - action_pin
* ask_package_price
 - action_price
* ask_no_test
 - action_test
* ask_home_charge
 - utter_ask_home_charge
 - utter_ask_book_interest
* ask_book
 - appointment_form
 - form{"name": "appointment_form"}
 - form{"name": null}
 - utter_slots_values
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
 - action_button
* name{"name":"Sam"}
 - utter_greet
* test{"conditions":"liver cancer"}
 - action_test
 - utter_ask_pin
* pins{"pin":"302029"}
 - action_pin
* ask_package_price
 - action_price
* ask_no_test
 - action_test
* ask_home_charge
 - utter_ask_home_charge
 - utter_ask_book_interest
* ask_book
 - appointment_form
 - form{"name": "appointment_form"}
 - form{"name": null}
 - utter_slots_values
 - utter_book_confirm
* book_confirm
 - action_book_api
 - utter_book_congrats
* thank
 - utter_thanks
* bye
 - utter_goodbye 
 
 
 


