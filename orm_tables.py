import sqlalchemy as sa

wishlist = sa.Table("wishlist", sa.MetaData(),
                    sa.Column("note_id", sa.Integer, primary_key=True),
                    sa.Column("name", sa.String),
                    sa.Column("cost", sa.Integer),
                    sa.Column("url", sa.String),
                    sa.Column("description", sa.String),
                    sa.Column("tms_create", sa.DateTime),
                    sa.Column("tms_update", sa.DateTime),
                    sa.Column("status", sa.String))
