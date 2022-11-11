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