import nltk
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import gensim
import pickle
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
nltk.download('stopwords')
stopwords=stopwords.words('english')

def preprocess(texts):
  result=[]
  for word in gensim.utils.simple_preprocess(texts):
    if word not in stopwords and len(word)>3:
      result.append(word)
  return result

dataset=pd.read_csv('Emails.csv')
dataset['Tokenized_text']=dataset.Email_Text.apply(preprocess)
dataset['text_joined']=dataset['Tokenized_text'].apply(lambda x:' '.join(x))

maxlen=-1
nltk.download('punkt')
from nltk.tokenize import word_tokenize
for doc in dataset.text_joined:
  tokens=word_tokenize(doc)
  if(maxlen<len(tokens)):
    maxlen=len(tokens)

tokenizer=Tokenizer(num_words=1200)
tokenizer.fit_on_texts(dataset.text_joined)
sequences=tokenizer.texts_to_sequences(dataset.text_joined)
padded_train=pad_sequences(sequences,maxlen=240)

with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

label_tokenizer=Tokenizer()
label_tokenizer.fit_on_texts(dataset.Category)
label_word_index=label_tokenizer.word_index
label_seq=label_tokenizer.texts_to_sequences(dataset.Category)
label_seq=np.array(label_seq)

x_train,x_test,y_train,y_test=train_test_split(padded_train,label_seq,test_size=.2,random_state=101)

import tensorflow as tf
model=tf.keras.Sequential([
                           tf.keras.layers.Embedding(1200,16,input_length=240),
                           tf.keras.layers.GlobalAveragePooling1D(),
                           tf.keras.layers.Dense(50,activation='relu',kernel_regularizer=tf.keras.regularizers.l2(l=.2)),
                           tf.keras.layers.BatchNormalization(),
                           tf.keras.layers.Dropout(.5),
                           tf.keras.layers.Dense(5,activation='softmax')

])
opt=tf.keras.optimizers.Adam(lr=.0001)
model.compile(loss='sparse_categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
model.summary()

model.fit(x_train,y_train,validation_data=(x_test,y_test),epochs=100,batch_size=8)

model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
model.save_weights("model.h5")