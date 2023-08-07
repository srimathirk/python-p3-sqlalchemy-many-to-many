from sqlalchemy import create_engine, func
from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

#builidng association table
game_user = Table(
    'game_users',
    Base.metadata,
    Column('game_id',ForeignKey('games.id'),primary_key=True),
    Column('user_id',ForeignKey('users.id'),primary_key=True),
    extend_existing=True,
)

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer(), primary_key=True)
    title = Column(String())
    genre = Column(String())
    platform = Column(String())
    price = Column(Integer())
    #created_at = Column(DateTime(),server_default=func.now())
    #updated_at = Column(DateTime(),onupdate=func.now())

    reviews = relationship('Review', backref=backref('game'))
    users=association_proxy('reviews', 'user', creator=lambda us:Review(user=us))
    #users = relationship('User',secondary=game_user, back_populates='games')
    def __repr__(self):
        return f'Game(id={self.id}, ' + \
            f'title={self.title}, ' + \
            f'platform={self.platform})'

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer(), primary_key=True)
    score = Column(Integer())
    comment = Column(String())
    #created_at=Column(DateTime(),server_default=func.now())
    #updated_at=Column(DateTime(),onupdate=func.now())

    game_id = Column(Integer(), ForeignKey('games.id'))
    #adding foreign key
    user_id=Column(Integer(),ForeignKey('users.id'))
    def __repr__(self):
        return f'Review(id={self.id}, ' + \
            f'score={self.score}, ' + \
            f'game_id={self.game_id})'

class User(Base):
    __tablename__ = 'users'
    id=Column(Integer(),primary_key=True)
    name= Column(String())
    created_at=Column(DateTime(),server_default=func.now())
    updated_at=Column(DateTime(),onupdate=func.now())
    
    #modify user table by adding relationship with backref in user table ;modify reviews table by add foreign key to refer to users table
    reviews = relationship('Review',backref=backref('user'))
    #games=relationship('Game',secondary=game_user,back_populates='users')
    games = association_proxy('reviews','game', 
        creator=lambda gm:Review(game=gm))
    def __repr__(self):
        return f'User(id{self.id},' +\
        f'name={self.name})'

