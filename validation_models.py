from pydantic import BaseModel

class CatalogueModel(BaseModel):
    name: str
    description: str
    image: str
    chef: str
    category: int

