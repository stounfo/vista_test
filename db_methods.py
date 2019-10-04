import sqlalchemy as sa
from sqlalchemy import create_engine

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



if __name__ == "__main__":    
    a = Database(db_type="mysql+pymysql",
                name="root",
                password="asd",
                host="localhost",
                port="3306",
                database="wishlist")
    print(a.select_from_wishlist())
