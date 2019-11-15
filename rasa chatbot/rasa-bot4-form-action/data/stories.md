## happy path
* greet
    - utter_greet
* appointment_booking
    - appointment_form
    - form{"name": "appointment_form"}
    - form{"name": null}
    - utter_slots_values
* thankyou
    - action_name

## unhappy path
* greet
    - utter_greet
* appointment_booking
    - appointment_form
    - form{"name": "appointment_form"}
* chitchat
    - utter_chitchat
    - appointment_form
    - form{"name": null}
    - utter_slots_values
* thankyou
    - action_name

## very unhappy path
* greet
    - utter_greet
* appointment_booking
    - appointment_form
    - form{"name": "appointment_form"}
* chitchat
    - utter_chitchat
    - appointment_form
* chitchat
    - utter_chitchat
    - appointment_form
* chitchat
    - utter_chitchat
    - appointment_form
    - form{"name": null}
    - utter_slots_values
* thankyou
    - action_name

## stop but continue path
* greet
    - utter_greet
* appointment_booking
    - appointment_form
    - form{"name": "appointment_form"}
* stop
    - utter_ask_continue
* affirm
    - appointment_form
    - form{"name": null}
    - utter_slots_values
* thankyou
    - action_name

## stop and really stop path
* greet
    - utter_greet
* appointment_booking
    - appointment_form
    - form{"name": "appointment_form"}
* stop
    - utter_ask_continue
* deny
    - action_deactivate_form
    - form{"name": null}

## chitchat stop but continue path
* appointment_booking
    - appointment_form
    - form{"name": "appointment_form"}
* chitchat
    - utter_chitchat
    - appointment_form
* stop
    - utter_ask_continue
* affirm
    - appointment_form
    - form{"name": null}
    - utter_slots_values
* thankyou
    - action_name

## stop but continue and chitchat path
* greet
    - utter_greet
* appointment_booking
    - appointment_form
    - form{"name": "appointment_form"}
* stop
    - utter_ask_continue
* affirm
    - appointment_form
* chitchat
    - utter_chitchat
    - appointment_form
    - form{"name": null}
    - utter_slots_values
* thankyou
    - action_name

## chitchat stop but continue and chitchat path
* greet
    - utter_greet
* appointment_booking
    - appointment_form
    - form{"name": "appointment_form"}
* chitchat
    - utter_chitchat
    - appointment_form
* stop
    - utter_ask_continue
* affirm
    - appointment_form
* chitchat
    - utter_chitchat
    - appointment_form
    - form{"name": null}
    - utter_slots_values
* thankyou
    - action_name

## chitchat, stop and really stop path
* greet
    - utter_greet
* appointment_booking
    - appointment_form
    - form{"name": "appointment_form"}
* chitchat
    - utter_chitchat
    - appointment_form
* stop
    - utter_ask_continue
* deny
    - action_deactivate_form
    - form{"name": null}
