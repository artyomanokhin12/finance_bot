from pydantic import BaseModel, ConfigDict


class SUserAuth(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
