##SCREEN

##To run any number of command 24*7 in any cloud server :

##using screen

sudo apt install screen

open terminal1:

run command: 

screen

then type command: 

rasa run --enable-api --log-file out.log --cors "*" --debug

again open another terminal type command :

screen

rasa run actions --debug


finally:

then run url on postman

http://ip_address:5005/webhooks/rest/webhook/

#json content":

{"message": "how are you?"}
