import sqlalchemy as sa
from sqlalchemy import create_engine

from orm_tables import wishlist
from utils import datetime_now


class Database():
    def __init__(self, db_type: str, host: str, port: str, name: str, password: str, database: str):
        engine_settings = f"{db_type}://{name}:{password}@{host}:{port}/{database}"
        engine = create_engine(engine_settings, pool_recycle=3600)
        self._conn = engine.connect()
    
    def select_from_wishlist(self, status=["Active", "Done", "Delete"]):
        notes = list()
        query = sa.select([wishlist]).where(wishlist.c.status.in_(status)).order_by(sa.desc(wishlist.c.tms_update))
        for row in self._conn.execute(query):
            note = dict()
            for column, value in row.items():
                note[column] = value
            notes.append(note)
        return notes
    
    def change_note_status(self, note_id, status):
        query = wishlist.update().values(status=status).where(wishlist.c.note_id == note_id)
        self._conn.execute(query)

    def insert_into_wishlist(self, name, cost, url, description):
        query = wishlist.insert().values(name=name,
                                         cost=cost,
                                         url=url,
                                         description=description,
                                         tms_create=datetime_now(),
                                         tms_update=datetime_now(),
                                         status="Active")
        self._conn.execute(query)

    def get_note_data(self, note_id):
        note = dict()
        query = sa.select([wishlist]).where(wishlist.c.note_id == note_id)
        for row in self._conn.execute(query):
            for column, value in row.items():
                note[column] = value
        return note

    def update_wishlist(self, note_id, name, cost, url, description):
        query = wishlist.update().values(name=name,
                                         cost=cost,
                                         url=url,
                                         description=description,
                                         tms_update=datetime_now()).where(
                                             wishlist.c.note_id == note_id
                                         )
        self._conn.execute(query)
