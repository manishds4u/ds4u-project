
#complete rasa running process
##1
1> To get rasa response on postman

#to run both rasa server i.e rasa nlu and rasa core

#error free

#step1: open 1st anaconda prompt then run this command

rasa run --enable-api --log-file out.log --cors "*"

or

rasa run --enable-api --log-file out.log --cors "*" --debug

step2: open 2nd anaconda prompt then run this command

rasa run actions

or 

rasa run actions --debug

finally:

then run url on postman

http://localhost:5005/webhooks/rest/webhook/

#json content":

{"message": "how are you?"}


##2
2> To run rasa via flask api on UI(FLASK/TEMPLATE/INDEX.HTML)

step1>

open spyder and run flask api code :

app.py


step2>

#to run both rasa server i.e rasa nlu and rasa core

#error free

#step2.1: open 1st anaconda prompt then run this command

rasa run --enable-api --log-file out.log --cors "*"

or

rasa run --enable-api --log-file out.log --cors "*" --debug

step2.2: open 2nd anaconda prompt then run this command

rasa run actions

or 

rasa run actions --debug

finally:

OPEN  UI(index.html) BY NAVIGATING VIA FOLDER

FLASK/TEMPLATE/INDEX.HTML

then got response from server by flask /chat api hitting


##3

chat withiN rasa cUSTOM ui BY NAVIGATING TO FOLDER (RASA UI/RASA-CUSTOM-UI-V2.0/INDEX.HTML) OR (RASA UI/RASA-WIDGET-MASTER/INDEX.HTML)

step1>

#to run both rasa server i.e rasa nlu and rasa core

#error free

#step1.1: open 1st anaconda prompt then run this command

rasa run --enable-api --log-file out.log --cors "*"

or

rasa run --enable-api --log-file out.log --cors "*" --debug

step1.2: open 2nd anaconda prompt then run this command

rasa run actions

or 

rasa run actions --debug

STEP2:

finally:

2.1>

1st UI

OPEN index.html 

rasa cUSTOM ui BY NAVIGATING TO FOLDER (RASA UI/RASA-CUSTOM-UI-V2.0/INDEX.HTML) 

or 

2.2>

2nd ui

open index.html

BY NAVIGATING TO FOLDEr (RASA UI/RASA-WIDGET-MASTER/INDEX.HTML)

get response
