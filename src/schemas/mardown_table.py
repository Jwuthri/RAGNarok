from pydantic import BaseModel


class MarkdownTableSchema(BaseModel):
    model_name: str
    description: str
    context_length: str | int
