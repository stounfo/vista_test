import sqlalchemy as sa
from sqlalchemy import create_engine
from utils import datetime_now
from orm_tables import wishlist



class Database():
    def __init__(self, db_type: str, host: str, port: str, name: str, password: str, database: str):
        engine_settings = f"{db_type}://{name}:{password}@{host}:{port}/{database}"
        engine = create_engine(engine_settings, pool_recycle=3600)
        self._conn = engine.connect()
    
    def select_from_wishlist(self, status: list = ["Active", "Done", "Delete"]):
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



if __name__ == "__main__":    
    a = Database(db_type="mysql+pymysql",
                name="root",
                password="asd",
                host="localhost",
                port="3306",
                database="wishlist")

    print(a.insert_into_wishlist("a", 44, "localhost", "spas"))
