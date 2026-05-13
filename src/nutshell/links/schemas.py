from pydantic import BaseModel, ConfigDict, HttpUrl


class UrlIn(BaseModel):
    url: HttpUrl


class UrlOut(UrlIn):
    model_config = ConfigDict(from_attributes=True)

    slug: str
