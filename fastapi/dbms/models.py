from datetime import datetime
import sqlalchemy as sql
from dbms.database import Base


class GetRequests(Base):
    __tablename__ = "getrequests"

    index = sql.Column(sql.Integer, primary_key=True, index=True)
    date = sql.Column(sql.DateTime, index=True, default=datetime.utcnow)
    speal_width = sql.Column(sql.Float, index=True, nullable=True)
    speal_length = sql.Column(sql.Float, index=True, nullable=True)
    petal_width = sql.Column(sql.Float, index=True, nullable=True)
    petal_length = sql.Column(sql.Float, index=True, nullable=True)
    message = sql.Column(sql.String, index=True)
