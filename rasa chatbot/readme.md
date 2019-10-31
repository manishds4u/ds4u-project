#helping link
link: https://github.com/dadecoza/starter-pack-rasa-stack

1>>>>>>#rasa-bot-1

#simple local database connection with response throgh action

#command to server and chatbot


#step1: run action and endpoint

python -m rasa_core_sdk.endpoint --actions actions

#chat in console i.e. cmd

step2:

rasa shell 



#for converting json to md:

from rasa_nlu.convert import convert_training_data

convert_training_data(data_file="nlu.json", out_file="out_file.md", output_format="md", language="")
