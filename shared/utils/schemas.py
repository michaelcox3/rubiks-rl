from typing import Literal
from pydantic import BaseModel, field_validator

VALID_MOVES = ["U","U'","D","D'","L","L'","R","R'","F","F'","B","B'"]  # 0..11 per env order

class CubeStateRequest(BaseModel):
    # 54-length vector of ints in [0,5] from your env's _get_obs()
    state: list[int]

    @field_validator("state")
    @classmethod
    def _validate_obs(cls, v: list[int]) -> list[int]:
        if len(v) != 54:
            raise ValueError("state must be length 54")
        if any((x < 0 or x > 5) for x in v):
            raise ValueError("state entries must be integers in [0,5]")
        return v

class CubeStateResponse(BaseModel):
    state: list[int]

class CubePredictResponse(BaseModel):
    move: str
    confidence: float | None = None

class CubeRotateRequest(CubeStateRequest):
    move: Literal["U","U'","D","D'","L","L'","R","R'","F","F'","B","B'"]

