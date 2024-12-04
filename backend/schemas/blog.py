from typing import Optional
from pydantic import BaseModel, root_validator, model_validator
from datetime import datetime


class CreateBlog(BaseModel):
    title: str
    slug: str
    content: Optional[str]

    @model_validator(mode='before')
    def generate_slug(cls, values):
        if "title" in values:
            values["slug"] = values.get("title").replace(" ", "-").lower()
        return values


class UpdateBlog(CreateBlog):
    pass


class ShowBlog(BaseModel):
    title: str
    content: Optional[str]
    created_at: datetime
    is_active: bool

    class Config():
        orm_mode = True


