step0:
FOLLOW BELOW LINK TO RESOLVE RASA DEPENDENCY ISSUE
https://stackoverflow.com/questions/46713653/installing-rasa-on-windows

step1:
INSTALLATION FILE:
GOOGLE DRIVE OF EMAIL ID:
manishkr.ds4u@gmail.com
folder:rasa
https://drive.google.com/drive/folders/1CFIsVv5xMhG2jGN_jjl3a9dZF-foQPXG?usp=sharing

step3:
creating virtual environment:
pip install virtualenv
virtualenv myenv
myenv\Scripts\acrtivate


step3:install python library for rasa dependency

Spacy – pip install -U spacy
Spacy Large English language model - python -m spacy download en_core_web_lg
Link the model now: python -m spacy link en_core_web_lg en

Fallback if the above fails: If your network is blocking it, or is too slow to download the above model, fallback by downloading it directly from its GitHub repo link:https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-2.0.0/en_core_web_lg-2.0.0.tar.gz extract the tar.gz using 7z and do python setup.py install by navigating into the directory.
or above linking command not work:
python -m spacy link en_core_web_md lg --force
Scikit – pip install -U scikit-learn

Numpy – pip install -U numpy
Scipy Package – pip install -U scipy
Sklearn – pip install -U sklearn-crfsuite
Duckling – pip install -U duckling
Tensorflow as a component - pip install -U tensorflow
Latest version of RASA NLU – pip install -U rasa_nlu
rasa: pip install -U rasa


Check if RASA installed or not by pasting the following command in Anaconda command prompt:

python -c "import rasa_nlu; print(rasa_nlu.__version__);"

step4: for running "rasa init" command and creating rasa folder follow:
rasa intent and entity classification using command line:
link1:
https://idk.dev/a-beginners-guide-to-rasa-nlu-for-intent-classification-and-named-entity-recognition/
link2:
https://towardsdatascience.com/a-beginners-guide-to-rasa-nlu-for-intent-classification-and-named-entity-recognition-a4f0f76b2a96
