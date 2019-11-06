## story_greet <!--- The name of the story. It is not mandatory, but useful for debugging. --> 
* greet <!--- User input expressed as intent. In this case it represents users message 'Hello'. --> 
 - utter_name <!--- The response of the chatbot expressed as an action. In this case it represents chatbot's response 'Hello, how can I help?' --> 

## story_name
* name{"name":"Sam"}
 - utter_greet
 
## story_joke_01
* joke
 - action_joke

## story_test_02
* test{"conditions":"diabetes"}
- action_test

## story_pincode_03
* pincodes{"pincode":"302029"}
 - action_pincode
 
## story_order_product
* greet
 - utter_name
* name{"name":"Sam"}
 - utter_greet
* order_product{"product":"laptop"}
 - utter_ask_model_name
* order_model{"model":"hp"}
 - action_order_product
 - utter_place_order
* test{"conditions":"diabetes"}
 - action_test
 - utter_ask_pincode
* pincodes{"pincode":"302029"}
 - action_pincode
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