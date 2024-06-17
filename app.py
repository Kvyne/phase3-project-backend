from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.category import Category
from models.catalogues import Catalogue
from validation_models import CatalogueModel

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins = ["*"], allow_credentials = True, 
allow_methods = ["*"], allow_headers = ["*"])


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get('/categories')
def categories():
    categories = Category.find_all()

    return categories

@app.get('/catalogue')
def get_catalogue():
    catalogues = Catalogue.find_all()

    return catalogues

@app.post('/catalogue')
def save_catalogue(data: CatalogueModel):
    catalogue = Catalogue(data.name, data.description, data.image, data.category, data.chef)
    catalogue.save()

    return catalogue.to_dict() 