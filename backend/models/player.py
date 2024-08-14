from sqlalchemy import Table, Column, Integer, String, MetaData

metadata = MetaData()

Player = Table(
    'players', metadata,
    Column('player_id', Integer, primary_key=True, index=True),
    Column('name', String(255)),
    Column('position', String(50)),
    Column('nationality', String(50)),
    Column('club', String(100))
)
