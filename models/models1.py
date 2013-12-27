
# SQLAlchemy, SQLElixir

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relation, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AttackType:
    UNDEFINED = 0
    
    # Melee attacks
    HIT     = 1
    CRUSH   = 2
    SLASH   = 3
    PIERCE  = 4
    CLEAVE  = 5
    CLAW    = 6
    KICK    = 7
    
    # Elemental attacks
    AIR     = 10
    FIRE    = 11
    WATER   = 12
    EARTH   = 13
    
    # Magical attacks
    GOOD_MAGIC    = 20
    EVIL_MAGIC    = 21
    NEUTRAL_MAGIC = 22
    
    # Other attacks
    DISEASE = 31
    POISON  = 32
    
    
class MobFlags:
    UNDEFINED  = 0
    
    AGGRESSIVE = 1
    SENTINAL   = 2
    
    ISNPC      = 4
    WIMPY      = 8
    
    
    
class AffectFlags:
    UNDEFINED     = 0
    
    SENSE_LIFE    = 1
    SENSE_HIDDEN  = 2
    
    SEE_INVISIBLE = 4
    NIGHT_VISION  = 8
    
    FLYING        = 16
    

class User(Base):
    __tablename__ = 'users'
    
    id        = Column(Integer, primary_key=True)
    username  = Column(String)
    password  = Column(String)
    email     = Column(String, nullable=False)
    firstname = Column(String)
    lastname  = Column(String)
    
    def __init__(self, username, password, firstname, lastname):
        self.username  = username
        self.password  = password
        self.firstname = firstname
        self.lastname  = lastname
        
    def __repr__(self):
        return "<User('%s', '%s', '%s', '%s')>" % (self.username, self.password, self.firstname, self.lastname)


class Attribute(Base):
    __tablename__ = 'attributes'
    
    id    = Column(Integer, primary_key=True)
    name  = Column(String)

class AttributeEffects(Base):
    __tablename__ = 'attributeeffects'
    
    id    = Column(Integer, primary_key=True)
    name  = Column(String)
    attribute = relation(Attribute, backref('attributeeffects', order_by=id))
    modifier = Column(Integer)

class Attack(Base):
    __tablename__ = 'attack'
    
    id         = Column(Integer, primary_key=True)
    name       = Column(String)
    attacktype = Column(Integer)  # this will be one of AttackType class attacks
    
    dice       = Column(Integer)  # d&d styke number of die
    sides      = Column(Integer)  # d&d style die sides
    bonus      = Column(Integer)  # attack bonus over dice roll
    use        = Column(Integer)  # Percent chance to use this attack 0-100

class Skill(Base):
    __tablename__ = 'skills'
    
    id    = Column(Integer, primary_key=True)
    name  = Column(String)
    attributeeffects = relation(AttributeEffects, backref('skills'), order_by=id))

class ToonClass(Base):
    __tablename__ = 'classes'
    
    id    = Column(Integer, primary_key=True)
    name  = Column(String)
    attributeeffects = relation(AttributeEffects, backref('classes'), order_by=id))

class ToonLevel(Base):
    __tablename__ = 'levels'
    
    id         = Column
    toonclass  = relation(ToonClass, backref=backref('levels', order_by=id))
    level      = Column(Integer)

class Toon(Base):
    __tablename__ = 'toons'
    
    id     = Column(Integer, primary_key=True)
    name   = Column(String)
    levels = relation(ToonLevel, backref=backref('toons', order_by=id))
    affectflags = Column(Integer)
    
