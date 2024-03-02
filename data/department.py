import datetime
import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy import orm


class Departments(SqlAlchemyBase):
    __tablename__ = 'departments'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    chief = sqlalchemy.Column(sqlalchemy.Integer)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)

    members = orm.relationship('User', back_populates="departments")



