from pydantic import BaseModel, ConfigDict


class Base(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        populate_by_name=True,
        validate_assignment=True,
    )
