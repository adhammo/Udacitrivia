from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

database_path = lambda database_name: f'postgresql://postgres:admin@localhost:5432/{database_name}'

db = SQLAlchemy()
migrate = Migrate(db=db)


def setup_db(app, database_name='trivia'):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path(database_name)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    migrate.app = app
    migrate.init_app(app)


class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    difficulty = Column(Integer, nullable=False)
    category_id = Column(ForeignKey('categories.id'), nullable=False)

    def __init__(self, question, answer, difficulty, category_id):
        self.question = question
        self.answer = answer
        self.difficulty = difficulty
        self.category_id = category_id

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'difficulty': self.difficulty,
            'category': self.category_id
        }


class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    questions = relationship(
        'Question', backref='category', lazy=True, cascade='delete')

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type,
            'questions': [question.id for question in self.questions]
        }
