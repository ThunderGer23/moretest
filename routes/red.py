from fastapi import APIRouter

red = APIRouter()

@red.get('/red')
def testDeRed():
    return 'Hola Mundo'