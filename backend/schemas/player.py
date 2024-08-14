from pydantic import BaseModel

class PlayerInput(BaseModel):
    player_id: int
    name: str
    position: str
    nationality: str
    club: str
