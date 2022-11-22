from fastapi import APIRouter
from models.red import Red
import tensorflow_hub as hub 
import tensorflow_text as text
#import keras
from tensorflow import keras

red = APIRouter()

def interpretacion_cita ( ref ):
  interprete = []
  for cita in ref:
    if cita >=0.5 : 
      interprete.append('CITA IEEE')
    if cita<0.5 : 
      interprete.append('CITA APA')
  return interprete

with open('CitasRN.json') as json_file:
      json_config = json_file.read()
json_file.close()

new_model = keras.models.model_from_json(
json_config,
custom_objects={'KerasLayer':hub.KerasLayer}
)

new_model.load_weights('CitasRN_weights.h5')

# new_model = keras.models.load_model(
#        ('Citas_RN.h5'),
#        custom_objects={'KerasLayer':hub.KerasLayer}
# )

new_model.load_weights('CitasRN_weights.h5')
new_model.compile(loss='mean_squared_error', optimizer='adam', metrics=['binary_accuracy'])

@red.post('/red')
def testDeRed(red: Red):
    analisis = new_model.predict(red.citas)
    return interpretacion_cita(analisis)