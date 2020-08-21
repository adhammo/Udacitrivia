import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from sqlalchemy import func
from schema import Schema, And, Use, Optional, SchemaError
import random
import re

from .models import db, setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    #----------------------------------------------------------------------------#
    # Setup App.
    #----------------------------------------------------------------------------#

    # Create flask app and setup CORS
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Setup sqlalchemy database
    setup_db(app)

    # CORS allowed headers and methods
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    #----------------------------------------------------------------------------#
    # Questions.
    #----------------------------------------------------------------------------#

    @app.route('/questions', methods=['GET'])
    def get_questions():
        questions = []
        total_questions = 0
        page = request.args.get('page', None, type=int)

        questions_query = Question.query
        if page:
            # paginated questions
            if page < 1:
                abort(400, 'pages are one indexed')

            questions = questions_query.order_by(Question.id).offset((page - 1) * QUESTIONS_PER_PAGE).limit(QUESTIONS_PER_PAGE).all()
            total_questions = questions_query.count()
        else:
            # all questions
            questions = questions_query.order_by(Question.id).all()
            total_questions = len(questions)

        if len(questions) == 0:
            abort(404, 'no questions found')

        return jsonify({
            'success': True,
            'questions': [question.format() for question in questions],
            'total_questions': total_questions
        })

    @app.route('/questions/<int:question_id>', methods=['GET'])
    def get_question(question_id):
        question = Question.query.get(question_id)

        if not question:
            abort(404, f'no question found with id {question_id}')

        return jsonify({
            'success': True,
            'question': question.format()
        })

    #  Create, search, and play questions
    #  ----------------------------------------------------------------

    @app.route('/questions', methods=['POST'])
    def post_questions():
        body = request.get_json()

        if not body:
            abort(400, 'no json body was found')

        if 'search_term' in body:
            return search_questions(body)
        else:
            return create_question(body)

    def search_questions(body):
        search_term = body['search_term']

        questions = []
        total_questions = 0
        page = request.args.get('page', None, type=int)

        questions_query = Question.query.filter(Question.question.ilike(f'%{search_term}%'))
        if page:
            # paginated questions
            if page < 1:
                abort(400, 'pages are one indexed')

            questions = questions_query.order_by(Question.id).offset((page - 1) * QUESTIONS_PER_PAGE).limit(QUESTIONS_PER_PAGE).all()
            total_questions = questions_query.count()
        else:
            # all questions
            questions = questions_query.order_by(Question.id).all()
            total_questions = len(questions)

        if len(questions) == 0:
            abort(404, f"no questions with search term '{search_term}' found")

        return jsonify({
            'success': True,
            'search_term': search_term,
            'questions': [question.format() for question in questions],
            'total_questions': total_questions
        })

    def create_question(body):
        schema = Schema({
            'question': str,
            'answer': str,
            'difficulty': And(Use(int), lambda difficulty: 1 <= difficulty <= 5),
            'category': And(Use(int), lambda category: Category.query.get(category) is not None)
        })

        # validate question input
        question_data = {}
        try:
            question_data = schema.validate(body)
        except:
            abort(400, 'input question was bad or not formatted correctly')

        # create question
        question = Question(question_data['question'], question_data['answer'], question_data['difficulty'], question_data['category'])

        # add question to database
        error = False
        try:
            db.session.add(question)
            db.session.commit()
            question_data = question.format()
        except:
            db.session.rollback()
            error = True
        finally:
            db.session.close()

        if error:
            abort(500, "couldn't create question")
        else:
            return jsonify({
                'success': True,
                'question': question_data
            })

    @app.route('/quizzes', methods=['POST'])
    def play_quizzes():
        body = request.get_json()

        if not body:
            abort(400, 'no json body was found')

        schema = Schema({
            'previous_questions': [And(Use(int), lambda question: Question.query.get(question) is not None)],
            Optional('quiz_category'): And(Use(int), lambda category: Category.query.get(category) is not None)
        })

        # validate quiz input
        quiz_data = {}
        try:
            quiz_data = schema.validate(body)
        except:
            abort(400, 'quiz input was bad or not formatted correctly')

        prev_questions = [Question.query.get(question) for question in quiz_data['previous_questions']]
        if 'quiz_category' in quiz_data:
            category = Category.query.get(quiz_data['quiz_category'])

            for question in prev_questions:
                if question.category_id != category.id:
                    abort(400, 'a question does not belong to category')

            total_questions = len(category.questions) - len(prev_questions)

            if total_questions == 0:
                return jsonify({
                    'success': True,
                    'total_questions': total_questions,
                    'categoy': category.id
                })

            question = list(filter(lambda question: question not in prev_questions, category.questions))[random.randint(0, total_questions - 1)]

            return jsonify({
                'success': True,
                'question': question.format(),
                'total_questions': total_questions,
                'categoy': category.id
            })
        else:
            questions = Question.query.all()
            total_questions = len(questions) - len(prev_questions)

            if total_questions == 0:
                return jsonify({
                    'success': True,
                    'total_questions': total_questions,
                })

            question = list(filter(lambda question: question not in prev_questions, questions))[random.randint(0, total_questions - 1)]

            return jsonify({
                'success': True,
                'question': question.format(),
                'total_questions': total_questions,
            })

    #  Edit and delete questions
    #  ----------------------------------------------------------------

    @app.route('/questions/<int:question_id>', methods=['PUT'])
    def edit_question(question_id):
        question = Question.query.get(question_id)

        if not question:
            abort(422, f'no question found with id {question_id}')

        body = request.get_json()
        if not body:
            abort(400, 'no json body was found')

        schema = Schema({
            'question': str,
            'answer': str,
            'difficulty': And(Use(int), lambda difficulty: 1 <= difficulty <= 5),
            'category': And(Use(int), lambda category: Category.query.get(category) is not None)
        })

        # validate question input
        question_data = {}
        try:
            question_data = schema.validate(body)
        except:
            abort(400, 'input question was bad or not formatted correctly')

        # edit question
        question.question = question_data['question']
        question.answer = question_data['answer']
        question.difficulty = question_data['difficulty']
        question.category_id = question_data['category']

        # edit question in database
        error = False
        try:
            db.session.commit()
            question_data = question.format()
        except:
            db.session.rollback()
            error = True
        finally:
            db.session.close()

        if error:
            abort(500, "couldn't edit question")
        else:
            return jsonify({
                'success': True,
                'question': question_data
            })

    @app.route('/questions/<int:question_id>', methods=['PATCH'])
    def edit_question_partially(question_id):
        question = Question.query.get(question_id)

        if not question:
            abort(422, f'no question found with id {question_id}')

        body = request.get_json()
        if not body:
            abort(400, 'no json body was found')

        schema = Schema({
            Optional('question'):  str,
            Optional('answer'): str,
            Optional('difficulty'): And(Use(int), lambda difficulty: 1 <= difficulty <= 5),
            Optional('category'): And(Use(int), lambda category: Category.query.get(category) is not None)
        })

        # validate question input
        question_data = {}
        try:
            question_data = schema.validate(body)
        except:
            abort(400, 'input question was bad or not formatted correctly')

        # edit question
        if 'question' in question_data:
            question.question = question_data['question']
        if 'answer' in question_data:
            question.answer = question_data['answer']
        if 'difficulty' in question_data:
            question.difficulty = question_data['difficulty']
        if 'category' in question_data:
            question.category_id = question_data['category']

        # edit question in database
        error = False
        try:
            db.session.commit()
            question_data = question.format()
        except:
            db.session.rollback()
            error = True
        finally:
            db.session.close()

        if error:
            abort(500, "")
        else:
            return jsonify({
                'success': True,
                'question': question_data
            })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)

        if not question:
            abort(422, f'no question found with id {question_id}')

        # delete question from database
        error = False
        try:
            question_data = question.format()
            db.session.delete(question)
            db.session.commit()
        except:
            db.session.rollback()
            error = True
        finally:
            db.session.close()

        if error:
            abort(500, "couldn't delete question")
        else:
            return jsonify({
                'success': True,
                'question': question_data
            })

    #----------------------------------------------------------------------------#
    # Categories.
    #----------------------------------------------------------------------------#

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.order_by(Category.id).all()

        if len(categories) == 0:
            abort(404, 'no categories found')

        return jsonify({
            'success': True,
            'categories': [category.format() for category in categories],
        })

    @app.route('/categories/<int:category_id>', methods=['GET'])
    def get_category(category_id):
        category = Category.query.get(category_id)

        if not category:
            abort(404, f'no category found with id {category_id}')

        return jsonify({
            'success': True,
            'category': category.format()
        })

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_category_questions(category_id):
        category = Category.query.get(category_id)

        if not category:
            abort(404, f'no category found with id {category_id}')

        questions = []
        total_questions = 0
        page = request.args.get('page', None, type=int)

        if page:
            # paginated questions
            if page < 1:
                abort(400, 'pages are one indexed')

            start = (page - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE - 1
            questions = category.questions[start:end]
            total_questions = len(category.questions)
        else:
            # all questions
            questions = category.questions
            total_questions = len(questions)

        if len(questions) == 0:
            abort(404, f"no questions found in category {category_id}")

        return jsonify({
            'success': True,
            'category': category.format(),
            'questions': [question.format() for question in questions],
            'total_questions': total_questions
        })

    @app.route('/categories/<int:category_id>/questions', methods=['POST'])
    def search_category_questions(category_id):
        category = Category.query.get(category_id)

        if not category:
            abort(404, f'no category found with id {category_id}')

        body = request.get_json()

        if not body:
            abort(400, 'no json body was found')

        if 'search_term' not in body:
            abort(400, 'no search term found')

        search_term = body['search_term']

        questions = []
        total_questions = 0
        page = request.args.get('page', None, type=int)

        questions_data = list(filter(lambda question: re.search(r"{}".format(search_term), question.question, re.IGNORECASE) is not None, category.questions))

        if page:
            # paginated questions
            if page < 1:
                abort(400, 'pages are one indexed')

            start = (page - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE - 1
            questions = questions_data[start:end]
            total_questions = len(questions_data)
        else:
            # all questions
            questions = questions_data
            total_questions = len(questions)

        if len(questions) == 0:
            abort(404, f"no questions with search term '{search_term}' found in category {category_id}")

        return jsonify({
            'success': True,
            'category': category.format(),
            'questions': [question.format() for question in questions],
            'total_questions': total_questions,
            'search_term': search_term
        })

    #----------------------------------------------------------------------------#
    # Error Handling.
    #----------------------------------------------------------------------------#

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request',
            'description': error.description
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'not found',
            'description': error.description
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method is not allowed',
            'description': error.description
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable entity',
            'description': error.description
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error',
            'description': error.description
        }), 500

    return app


if __name__ == "__main__":
    create_app()
