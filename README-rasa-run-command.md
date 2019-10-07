follow link:
https://towardsdatascience.com/a-beginners-guide-to-rasa-nlu-for-intent-classification-and-named-entity-recognition-a4f0f76b2a96

possible rasa commad:

usage: rasa [-h] [--version]
            {init,run,shell,train,interactive,test,visualize,data,x} ...
            
            
            
            rasa init    -----for creating file
            rasa shell ------for cmd chat
            rasa train  ------ to train rasa model
            rasa test-----to tetst rasa model
            
1:

after activating virtualenvironment myenv
and installing rasa
pip install -u rasa
2:
then run command

command1:
rasa init  

 The following files will be created:
__init__.py: An empty file that helps python find your actions.
actions.py: Code for your custom actions
config.yml: Configuration of your NLU and Core models
credentials.yml: Details for connecting to other services
data/nlu.md: Your NLU training data
data/stories.md: Your stories
domain.yml: Your assistant’s domain
endpoints.yml: Details for connecting to endpoint channels
models/<timestamp>.tar.gz: Your initial model. Timestamp is in the format of YYYYMMDD-hhmmss. NLU-only models will have nlu prefix at the front.
  3:
for converting nlu.md file nlu.json:
command2:
rasa data convert nlu --data data/nlu.md --out data/nlu.json -f json
4:
 for training only rasa nlu for intent and entity recognition
 run:
 command 3:
 rasa train nlu
 5:
 for traing compltete rasa nlu and rasa core file:
 
 command4:
 
 rasa train
 
 
 6:
Testing model
You can test the model by running an interactive shell mode via the following command:

rasa shell nlu
If you have multiple nlu models and would like to test a specific model, use the following command instead.

rasa shell -m models/nlu-20190515-144445.tar.gz

7:
 after training it will create models folder:
 after extracting model folder:
 it has two file:
 nlu file  -----> models/default
 core file ----> models/dialogue
 
 8:
 for running rasa server 
 command5:
 
 rasa run
