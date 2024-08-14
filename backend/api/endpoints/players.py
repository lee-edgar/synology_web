from fastapi import APIRouter, HTTPException
from typing import Optional
from sqlalchemy import select, insert
from sqlalchemy.exc import SQLAlchemyError
from db.session import engine
from models.player import Player
from schemas.player import PlayerInput
import logging

router = APIRouter()

@router.get("/players/{player_id}")
async def get_player_name(player_id: int) -> Optional[dict]:
    try:
        with engine.connect() as connection:
            query = select(Player.c.name).where(Player.c.player_id == player_id)
            result = connection.execute(query).first()
            if result:
                return {"name": result[0]}
            else:
                raise HTTPException(status_code=404, detail="Player not found")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/players/")
async def add_player(player: PlayerInput):
    try:
        with engine.connect() as connection:
            transaction = connection.begin()
            try:
                query = insert(Player).values(
                    player_id=player.player_id,
                    name=player.name,
                    position=player.position,
                    nationality=player.nationality,
                    club=player.club
                )
                connection.execute(query)
                transaction.commit()
                return {"message": "Player added successfully"}
            except SQLAlchemyError as e:
                transaction.rollback()
                logging.error(f"Error occurred: {str(e)}")
                raise HTTPException(status_code=500, detail="Database error")
    except SQLAlchemyError as e:
        logging.error(f"Connection error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
