from sqlalchemy.orm import relationship
from App import db

class User(db.Model):
    user_id=db.Column(db.Integer, primary_key=True,autoincrement=True,unique=True)
    user_ci=db.Column(db.String(10),unique=True)
    user_name=db.Column(db.String(100),nullable=False)
    user_type=db.Column(db.String(1))
    password_hash = db.Column(db.String(200))
    def __init__(self,user_ci,user_name,password_hash,user_type ):
        self.user_ci=user_ci
        self.user_name=user_name
        self.password_hash=password_hash
        self.user_type=user_type

class Area(db.Model):
    __tablename__ = 'area'
    area_id=db.Column(db.Integer, primary_key=True,autoincrement=True,unique=True)
    area_name=db.Column(db.String(100),nullable=False)
    gestor=relationship("Manager",back_populates="manager_area")

class Manager(db.Model):
    __tablename__ = 'manager'
    manager_id=db.Column(db.Integer, primary_key=True,autoincrement=True,unique=True)
    manager_ci=db.Column(db.String(10),unique=True)
    manager_name=db.Column(db.String(100),nullable=False)
    manager_email = db.Column(db.String(100),nullable=False)
    manager_phone=db.Column(db.String(10),nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey(Area.area_id))
    manager_area = relationship("Area", back_populates="gestor")
    contract=relationship("Contract",back_populates="manager")

class Contract(db.Model):
    __tablename__ = 'contract'
    contract_id=db.Column(db.Integer, primary_key=True,autoincrement=True,unique=True)
    contract_provider=db.Column(db.String(200),nullable=False)
    contract_providerID=db.Column(db.String(10),nullable=False)
    contract_name=db.Column(db.String(200),nullable=False)
    contract_start= db.Column(db.Date,nullable=False)
    contract_end=db.Column(db.Date,nullable=False)
    contract_close=db.Column(db.Date)
    contract_state=db.Column(db.String(10),nullable=False)
    contract_instate=db.Column(db.String(10))
    manager_id = db.Column(db.Integer, db.ForeignKey(Manager.manager_id))
    manager= relationship("Manager", back_populates="contract")
    level=relationship("Level",back_populates="contract")

class Level(db.Model):
    __tablename__ = 'level'
    level_id=db.Column(db.Integer, primary_key=True,autoincrement=True,unique=True)
    level_name=db.Column(db.String(200),nullable=False)
    level_goal=db.Column(db.Float,nullable=False)
    contract_id = db.Column(db.Integer, db.ForeignKey(Contract.contract_id))
    contract= relationship("Contract", back_populates="level")
    score=relationship("Score",back_populates="level")

class Score(db.Model):
    __tablename__ = 'score'
    score_id=db.Column(db.Integer, primary_key=True,autoincrement=True,unique=True)
    score_month=db.Column(db.Integer,nullable=False)
    score_year=db.Column(db.Integer,nullable=False)
    score_value=db.Column(db.Float,nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey(Level.level_id))
    level= relationship("Level", back_populates="score")


db.create_all()