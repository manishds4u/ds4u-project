# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 16:17:20 2019

@author: Manish
"""


#for dataset and notebook on kaggle
#https://www.kaggle.com/abhishek/approaching-almost-any-nlp-problem-on-kaggle/notebook






import pandas as pd
import numpy as np
import xgboost as xgb
from tqdm import tqdm
from sklearn.svm import SVC
from keras.models import Sequential
from keras.layers.recurrent import LSTM, GRU
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.embeddings import Embedding
from keras.layers.normalization import BatchNormalization
from keras.utils import np_utils
from sklearn import preprocessing, decomposition, model_selection, metrics, pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from keras.layers import GlobalMaxPooling1D, Conv1D, MaxPooling1D, Flatten, Bidirectional, SpatialDropout1D
from keras.preprocessing import sequence, text
from keras.callbacks import EarlyStopping
from nltk import word_tokenize
from nltk.corpus import stopwords
#stop_words = stopwords.words('english')

from sklearn import preprocessing, decomposition, model_selection, metrics, pipeline
from sklearn.linear_model import LogisticRegression

import pandas as pd
import numpy as np


#1

train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')
sample = pd.read_csv('sample_submission.csv')


train.head()
test.head()
sample.head()


from sklearn import preprocessing, decomposition, model_selection, metrics, pipeline
lbl_enc = preprocessing.LabelEncoder()
y = lbl_enc.fit_transform(train.author.values)


from sklearn.model_selection import train_test_split
xtrain, xvalid, ytrain, yvalid = train_test_split(train.text.values, y, 
                                                  stratify=y, 
                                                  random_state=42, 
                                                  test_size=0.1, shuffle=True)

print (xtrain.shape)
print (xvalid.shape)



# Always start with these features. They work (almost) everytime!
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
tfv = TfidfVectorizer(min_df=3,  max_features=None, 
            strip_accents='unicode', analyzer='word',token_pattern=r'\w{1,}',
            ngram_range=(1, 3), use_idf=1,smooth_idf=1,sublinear_tf=1,
            stop_words = 'english')

# Fitting TF-IDF to both training and test sets (semi-supervised learning)
tfv.fit(list(xtrain) + list(xvalid))
xtrain_tfv =  tfv.transform(xtrain) 
xvalid_tfv = tfv.transform(xvalid)


# Fitting a simple Logistic Regression on TFIDF
from sklearn.linear_model import LogisticRegression
clf = LogisticRegression(C=1.0)
clf.fit(xtrain_tfv, ytrain)
predictions = clf.predict_proba(xvalid_tfv)
predict1= clf.predict(xvalid_tfv)

# Fitting a simple Naive Bayes on TFIDF
from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB()
clf.fit(xtrain_tfv, ytrain)
prediction2 = clf.predict_proba(xvalid_tfv)
predict2= clf.predict(xvalid_tfv)

#accuracy score
from sklearn.metrics import accuracy_score

acs2=accuracy_score(predict2, yvalid)

inverse=tfv.inverse_transform(predict2)
inv=np.array(inverse)
df=pd.DataFrame(inv.reshape(-1,1))



from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

print(confusion_matrix(yvalid,predict2))
print(classification_report(yvalid,predict2))
print(accuracy_score(yvalid, predict2))



#Instead of using TF-IDF, we can also use word counts as features.
#This can be done easily using CountVectorizer from scikit-learn.
ctv = CountVectorizer(analyzer='word',token_pattern=r'\w{1,}',
            ngram_range=(1, 3), stop_words = 'english')

# Fitting Count Vectorizer to both training and test sets (semi-supervised learning)
ctv.fit(list(xtrain) + list(xvalid))
xtrain_ctv =  ctv.transform(xtrain) 
xvalid_ctv = ctv.transform(xvalid)


from sklearn.linear_model import LogisticRegression

# Fitting a simple Logistic Regression on TFIDF
clf = LogisticRegression(C=1.0)
clf.fit(xtrain_tfv, ytrain)
predictions3 = clf.predict_proba(xvalid_tfv)
predict3 = clf.predict(xvalid_tfv)
#accuracy score
from sklearn.metrics import accuracy_score

acs3=accuracy_score(predict3, yvalid)


from sklearn.naive_bayes import MultinomialNB
# Fitting a simple Naive Bayes on Counts
clf = MultinomialNB()
clf.fit(xtrain_ctv, ytrain)
predictions = clf.predict_proba(xvalid_ctv)


predict4 = clf.predict(xvalid_tfv)
#accuracy score
from sklearn.metrics import accuracy_score

acs4=accuracy_score(predict4, yvalid)



#Since SVMs take a lot of time, we will reduce the number of features from the TF-IDF 
#using Singular Value Decomposition before applying SVM.

#Also, note that before applying SVMs, we must standardize the data.

# Apply SVD, I chose 120 components. 120-200 components are good enough for SVM model.
svd = decomposition.TruncatedSVD(n_components=120)
svd.fit(xtrain_tfv)
xtrain_svd = svd.transform(xtrain_tfv)
xvalid_svd = svd.transform(xvalid_tfv)

# Scale the data obtained from SVD. Renaming variable to reuse without scaling.
scl = preprocessing.StandardScaler()
scl.fit(xtrain_svd)
xtrain_svd_scl = scl.transform(xtrain_svd)
xvalid_svd_scl = scl.transform(xvalid_svd)
#Now it's time to apply SVM. After running the following cell, feel free to go for a walk or 
#talk to your girlfriend/boyfriend. :P

# Fitting a simple SVM
clf = SVC(C=1.0, probability=True) # since we need probabilities
clf.fit(xtrain_svd_scl, ytrain)
prediction1 = clf.predict_proba(xvalid_svd_scl)

predict1 = clf.predict(xvalid_svd_scl)


from sklearn.metrics import accuracy_score

acs4=accuracy_score(predict1, yvalid)









#2
#other method

from nltk.corpus import stopwords
#stop_words = stopwords.words('english')

from sklearn import preprocessing, decomposition, model_selection, metrics, pipeline
from sklearn.linear_model import LogisticRegression

import pandas as pd
import numpy as np


train = pd.read_csv('train.csv')


train.head()
x=train.text

lbl_enc = preprocessing.LabelEncoder()
y = lbl_enc.fit_transform(train.author.values)

xtrain, xvalid, ytrain, yvalid = train_test_split(train.text.values, y, 
                                                  stratify=y, 
                                                  random_state=42, 
                                                  test_size=0.1, shuffle=True)



# Always start with these features. They work (almost) everytime!
tfv = TfidfVectorizer(min_df=3,  max_features=None, 
            strip_accents='unicode', analyzer='word',token_pattern=r'\w{1,}',
            ngram_range=(1, 3), use_idf=1,smooth_idf=1,sublinear_tf=1,
            stop_words = 'english')

# Fitting TF-IDF to both training and test sets (semi-supervised learning)
tfv.fit(list(xtrain) + list(xvalid))
xtrain_tfv =  tfv.transform(xtrain) 
xvalid_tfv = tfv.transform(xvalid)
# Fitting a simple Logistic Regression on TFIDF
clf = LogisticRegression(C=1.0)
clf.fit(xtrain_tfv, ytrain)
predictions = clf.predict_proba(xvalid_tfv)

prediction = clf.predict(xvalid_tfv)

inverse=tfv.inverse_transform(prediction)
inv=np.array(inverse)
df=pd.DataFrame(inv.reshape(-1,1))

from sklearn.metrics import accuracy_score

acs=accuracy_score(prediction, yvalid)









#3
#other method



from sklearn import preprocessing, decomposition, model_selection, metrics, pipeline
from sklearn.linear_model import LogisticRegression

import pandas as pd
import numpy as np
train = pd.read_csv('train.csv')


train.head()
#features
x=train.text


#label_encoding
lbl_enc = preprocessing.LabelEncoder()
y = lbl_enc.fit_transform(train.author.values)


#Text Preprocessing

import re
documents = []

from nltk.stem import WordNetLemmatizer

stemmer = WordNetLemmatizer()

for sen in range(0, len(x)):
    # Remove all the special characters
    document = re.sub(r'\W', ' ', str(x[sen]))
    
    # remove all single characters
    document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)
    
    # Remove single characters from the start
    document = re.sub(r'\^[a-zA-Z]\s+', ' ', document) 
    
    # Substituting multiple spaces with single space
    document = re.sub(r'\s+', ' ', document, flags=re.I)
    
    # Removing prefixed 'b'
    document = re.sub(r'^b\s+', '', document)
    
    # Converting to Lowercase
    document = document.lower()
    
    # Lemmatization
    document = document.split()

    document = [stemmer.lemmatize(word) for word in document]
    document = ' '.join(document)
    
    documents.append(document)
    
#Converting Text to Numbers
    
    
"""   
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
X = vectorizer.fit_transform(documents).toarray()

from sklearn.feature_extraction.text import TfidfTransformer
tfidfconverter = TfidfTransformer()
X = tfidfconverter.fit_transform(X).toarray()
"""
#or

from sklearn.feature_extraction.text import TfidfVectorizer

tfv = TfidfVectorizer(min_df=3,  max_features=None, 
            strip_accents='unicode', analyzer='word',token_pattern=r'\w{1,}',
            ngram_range=(1, 3), use_idf=1,smooth_idf=1,sublinear_tf=1,
            stop_words = 'english')
#tfidfconverter = TfidfVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
tfv.fit(documents)
X=tfv.fit_transform(documents)


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)



classifier = LogisticRegression(C=1.0)
classifier.fit(X_train, y_train) 

"""
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators=1000, random_state=0)
classifier.fit(X_train, y_train) 
"""
y_pred = classifier.predict(X_test)


#accuracy score
from sklearn.metrics import accuracy_score

acs=accuracy_score(y_pred, y_test)

inverse=tfv.inverse_transform(y_pred)
inv=np.array(inverse)
df=pd.DataFrame(inv.reshape(-1,1))



from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

print(confusion_matrix(y_test,y_pred))
print(classification_report(y_test,y_pred))
print(accuracy_score(y_test, y_pred))


import pickle
with open('text_classifier', 'wb') as picklefile:
    pickle.dump(classifier,picklefile)
    
    
    
with open('text_classifier', 'rb') as training_model:
    model = pickle.load(training_model)
    
    
    
y_pred2 = model.predict(X_test)

print(confusion_matrix(y_test, y_pred2))
print(classification_report(y_test, y_pred2))
print(accuracy_score(y_test, y_pred2)) 






