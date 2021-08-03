import urllib
import os
import sqlalchemy
import databases
from datetime import datetime

host_server = os.environ.get('host_server', 'localhost')
db_server_port = urllib.parse.quote_plus(str(os.environ.get('db_server_port', '5432')))
database_name = os.environ.get('database_name', 'feedback_api')
db_username = urllib.parse.quote_plus(str(os.environ.get('db_username', 'postgres')))
db_password = urllib.parse.quote_plus(str(os.environ.get('db_password', 'Usd100000')))
ssl_mode = urllib.parse.quote_plus(str(os.environ.get('ssl_mode','prefer')))

DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(db_username, db_password, host_server, db_server_port, database_name, ssl_mode)

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

feedbacks = sqlalchemy.Table(
    "feedback",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("service_name", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("tag", sqlalchemy.String),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.now),
    sqlalchemy.Column("data", sqlalchemy.String, nullable=False)
)

engine = sqlalchemy.create_engine(DATABASE_URL, echo=True)
metadata.create_all(engine)
