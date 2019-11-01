#Rasa slot filling example either from entities and action slot. 

#run flask api response on html

#to run both rasa server i.e rasa nlu and rasa core

#error free

#step1:

rasa run --enable-api --log-file out.log --cors "*"

rasa run --enable-api --log-file out.log --cors "*" --debug

step2:

rasa run actions

finally:

then run url on postman

http://localhost:5005/webhooks/rest/webhook/

#json content":

{"message": "how are you?"}
