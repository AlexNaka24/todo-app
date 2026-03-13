from pydantic import BaseModel, Field

class TodoRequest(BaseModel):
    title: str = Field(min_length=10, max_length=50)
    description: str = Field(min_length=10, max_length=200)
    priority: int = Field(ge=0, le=6)
    complete: bool = Field(default=False)