from fastapi import FastAPI
#from routes.user import user
from docs import tags_metadata


# Creating a FastAPI object.
app = FastAPI(
    title= "API para las citas",
    description= "This is a description for the API :v/",
    version = "1.0",
    contact={
        "name": "ThunderGer",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    openapi_tags= tags_metadata
)