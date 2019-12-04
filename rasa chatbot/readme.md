1>

## RASA FRESH INSTALLATION ON ANY SYSTEM

STEP1: FIRST INSTALL THIS TWO SOFTWARE WHICH IS RASA DEPENDENCY SOFTWARE FOR SYSTEM

refer google drive link for download rasa dependency software: 

google drive email:

manishkr.ds4@gmail.com

https://drive.google.com/drive/folders/1CFIsVv5xMhG2jGN_jjl3a9dZF-foQPXG

1.1> install:  microsoft visual c++ build tools version 14.0.25420.1

1.2> install: Microsoft Visual C++ 2015 Redistributable (x64) - 14.0.23026.0

step2:

creating virtualenvironment

2.1> pip install virtualenv

2.2> virualenv rasaenv

2.3> rasaenv\Scripts\activate

2.4> pip install rasa==1.3.7

step3: 

successfuly installed rasa then run rasa command

rasa init

rasa train

rasa run actions





2.
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



## to install rasa x on UI

pip install rasa-x -i https://pypi.rasa.com/simple
