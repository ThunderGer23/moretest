import os
from os import remove
import pickle 
import pathlib
import shutil
import tempfile
import pandas as pd 
import tensorflow as tf
from IPython import display
from tensorflow import tensorflow_hub as hub
from tensorflow import tensorflow_text as text
from tensorflow.python.keras import layers
from tensorflow.python.keras import regularizers
from urllib.request import urlopen

"""
    DATASET PARA CITAS
"""

#from google.colab import drive
#from google.colab import files

#drive.mount('/content/drive') 
os.chdir('/content/drive/MyDrive/APA_entrenamientos')

df = pd.DataFrame({'Categoria':[], 'Cita':[]})
df.to_csv('citas_dataset2.csv')
#files.download('citas_dataset2.csv')

df=pd.read_csv('citas_dataset.csv', encoding='latin-1')
df.head()

"""
    CODIFICANDO BERT PARA CITAS
"""
df_ieee=df[df['Categoria']=='ieee']
df_apa = df[df['Categoria']=='apa']

df_apa_submuestra = df_ieee.sample(df_ieee.shape[0])
df_apa_submuestra.shape

df_balanceado = pd.concat([df_ieee, df_apa])
df_balanceado.shape

df_balanceado['Categoria'].value_counts()
df_balanceado['ieee'] = df_balanceado['Categoria'].apply(lambda x : 1 if x == 'ieee' else 0)
df_balanceado.sample(5)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(df_balanceado['Cita'], df_balanceado['ieee'], stratify=df_balanceado['ieee'])

X_train.head(4)

bert_preprocess = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3")
bert_encoder = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4")

logdir = pathlib.Path(tempfile.mkdtemp())/"tensorboard_logs"
shutil.rmtree(logdir, ignore_errors=True)

"""
"""

# Bert capas
text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name='text')
preprocessed_text = bert_preprocess(text_input)
outputs = bert_encoder(preprocessed_text)

# capas red neuronal
l = tf.keras.layers.Dropout(0.1, name='dropout')(outputs['pooled_output'])
l = tf.keras.layers.Dense(1, activation='sigmoid', name="output")(l)

model = tf.keras.Model(inputs=[text_input], outputs =[l])
model.summary()

"""
"""

METRICS = [
      tf.keras.metrics.BinaryAccuracy(name='accuracy'),
      tf.keras.metrics.Precision(name='precision'),
      tf.keras.metrics.Recall(name='recall')
]

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])
model.fit(X_train, y_train, epochs=10)

"""
"""

nameRN='Citas_RN.h5'
model.save(nameRN)
model.evaluate(X_test,y_test)

citas = [ 
    'González, R. (2013). Costos Paramétricos - México, D.F. Instituto Mexicano de Ingeniería de Costos. D.F, México. Editorial Trillas',
    '1.  SEP, 2011. “Programa de Estudio 2011, Guía para la Educadora, Educación  Básica Prescolar”. México, SEP.',
    '9.  Moltó  ,  E.  Fundamentos  de  la  Educación  en  Física.  Ministerio  de  Educación, La Habana, 2003.',
    'Bloot, S. J., & Pye, K. (2001). “Gradistat: A gran size distribution and statics package for the analysis of unconsolidated sediments”. Earth Surface Processes and Landforms, 261.',
]

def interpretacion_cita ( ref ):
  interprete = []
  for cita in ref:
    if cita >=0.5 : 
      interprete.append('cita ieee')
    if cita<0.5 : 
      interprete.append('cita apa')
  return interprete