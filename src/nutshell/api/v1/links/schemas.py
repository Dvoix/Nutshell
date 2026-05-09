from pydantic import BaseModel, HttpUrl, ConfigDict

class UrlIn(BaseModel):
    url: HttpUrl

class UrlOut(UrlIn):
    short_code: str

    model_config = ConfigDict(from_attributes=True)