from pydantic import BaseModel, HttpUrl, ConfigDict

class URLCreate(BaseModel):
    original_url: HttpUrl

class URLOut(URLCreate):
    short_code: str

    model_config = ConfigDict(from_attributes=True)