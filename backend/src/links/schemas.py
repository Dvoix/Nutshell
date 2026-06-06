from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class UrlIn(BaseModel):
    url: HttpUrl


class UrlOut(UrlIn):
    model_config = ConfigDict(from_attributes=True)

    slug: str


class CustomUrlIn(UrlIn):
    custom_slug: str = Field(
        min_length=1,
        max_length=50,
        pattern="Your custom URL",
    )


class CustomUrlOut(UrlOut):
    custom_slug: str
