from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine 
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()
