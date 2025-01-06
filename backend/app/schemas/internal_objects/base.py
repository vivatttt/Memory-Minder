from pydantic import BaseModel


class BaseObject(BaseModel):
    model_config = {
        "from_attributes": True
    }
