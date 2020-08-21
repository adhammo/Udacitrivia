import os
import unittest
import json

from flask_sqlalchemy import SQLAlchemy
from schema import Schema, And, Use, Optional, SchemaError

from flaskr import create_app
from flaskr.models import setup_db, db, Question, Category


class TriviaTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, 'trivia_test')

        db.drop_all()
        db.create_all()

        self.temp_categories = [
            Category('Science'),
            Category('Art'),
            Category('Geography'),
            Category('History'),
            Category('Entertainment'),
            Category('Sports')
        ]

        self.temp_questions = [
            Question('Whose autobiography is entitled \'I Know Why the Caged Bird Sings\'?', 'Maya Angelou', 2, 4),
            Question('What boxer\'s original name is Cassius Clay?', 'Muhammad Ali', 1, 4),
            Question('The Taj Mahal is located in which Indian city?', 'Agra', 2, 3),
            Question('Which Dutch graphic artist–initials M C was a creator of optical illusions?', 'Escher', 1, 2),
            Question('What is the heaviest organ in the human body?', 'The Liver', 4, 1)
        ]

        db.session.add_all(self.temp_categories)
        db.session.add_all(self.temp_questions)
        db.session.commit()

    def tearDown(self):
        db.drop_all()

    #----------------------------------------------------------------------------#
    # Questions.
    #----------------------------------------------------------------------------#

    #  Create questions
    #  ----------------------------------------------------------------

    def test_create_question_success(self):
        schema = Schema({
            'id': int,
            'question': str,
            'answer': str,
            'difficulty': int,
            'category': int
        })

        res = self.client().post('/questions', json={
            'question': 'Who are you?',
            'answer': 'Someone',
            'difficulty': 5,
            'category': 1
        })

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 200)
        self.assertTrue('success' in data)
        self.assertTrue('question' in data)

        (success, question) = (data['success'], data['question'])

        # check success
        self.assertEqual(success, True)

        # check question
        self.assertTrue(schema.is_valid(question))
        self.assertEqual(question['id'], 6)
        self.assertEqual(question['question'], 'Who are you?')
        self.assertEqual(question['answer'], 'Someone')
        self.assertEqual(question['difficulty'], 5)
        self.assertEqual(question['category'], 1)

        # check added question
        self.assertEqual(json.loads(self.client().get('/questions/6').data)['question'], question)

    def test_create_question_fail_bad_input(self):
        res = self.client().post('/questions', json={
            'question': 'Who are you?',
            'category': 'sad'
        })

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 400)
        self.assertTrue('success' in data)
        self.assertTrue('error' in data)
        self.assertTrue('description' in data)
        self.assertTrue('message' in data)

        (success, error, description, message) = (data['success'], data['error'], data['description'], data['message'])

        # check success
        self.assertFalse(success)
        self.assertEqual(error, 400)
        self.assertEqual(description, 'input question was bad or not formatted correctly')
        self.assertEqual(message, 'bad request')

    #  Get questions
    #  ----------------------------------------------------------------

    def test_get_questions_success(self):
        schema = Schema({
            'id': int,
            'question': str,
            'answer': str,
            'difficulty': int,
            'category': int
        })

        res = self.client().get('/questions')

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 200)
        self.assertTrue('success' in data)
        self.assertTrue('questions' in data)

        (success, questions) = (data['success'], data['questions'])

        # check success
        self.assertEqual(success, True)

        # check questions
        for i in range(len(questions)):
            question = questions[i]
            self.assertTrue(schema.is_valid(question))
            self.assertEqual(question, self.temp_questions[i].format())

    def test_get_questions_fail_no_questions(self):
        db.drop_all()
        db.create_all()

        res = self.client().get('/questions')

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 404)
        self.assertTrue('success' in data)
        self.assertTrue('error' in data)
        self.assertTrue('description' in data)
        self.assertTrue('message' in data)

        # check success
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['description'], 'no questions found')
        self.assertEqual(data['message'], 'not found')

    def test_get_question_success(self):
        schema = Schema({
            'id': int,
            'question': str,
            'answer': str,
            'difficulty': int,
            'category': int
        })

        res = self.client().get('/questions/1')

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 200)
        self.assertTrue('success' in data)
        self.assertTrue('question' in data)

        # check success
        self.assertEqual(data['success'], True)

        # check question
        question = data['question']
        self.assertTrue(schema.is_valid(question))
        self.assertEqual(question, self.temp_questions[0].format())

    def test_get_question_fail_no_question(self):
        res = self.client().get('/questions/6')

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 404)
        self.assertTrue('success' in data)
        self.assertTrue('error' in data)
        self.assertTrue('description' in data)
        self.assertTrue('message' in data)

        # check success
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['description'], 'no question found with id 6')
        self.assertEqual(data['message'], 'not found')

    #  Search questions
    #  ----------------------------------------------------------------

    def test_search_question_success(self):
        schema = Schema({
            'id': int,
            'question': str,
            'answer': str,
            'difficulty': int,
            'category': int
        })

        res = self.client().post('/questions', json={
            'search_term': 'what'
        })

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 200)
        self.assertTrue('success' in data)
        self.assertTrue('questions' in data)
        self.assertTrue('total_questions' in data)
        self.assertTrue('search_term' in data)

        # check success
        self.assertEqual(data['success'], True)

        # check question
        questions = data['questions']
        total_questions = data['total_questions']
        search_term = data['search_term']
        self.assertEqual(search_term, 'what')
        self.assertEqual(total_questions, 2)
        self.assertTrue(schema.is_valid(questions[0]))
        self.assertEqual(questions[0], self.temp_questions[1].format())
        self.assertTrue(schema.is_valid(questions[1]))
        self.assertEqual(questions[1], self.temp_questions[4].format())

    def test_search_question_fail_no_questions(self):
        res = self.client().post('/questions', json={
            'search_term': 'sadsadsad'
        })

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 404)
        self.assertTrue('success' in data)
        self.assertTrue('error' in data)
        self.assertTrue('description' in data)
        self.assertTrue('message' in data)

        # check success
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['description'], "no questions with search term 'sadsadsad' found")
        self.assertEqual(data['message'], 'not found')

    #  Edit questions
    #  ----------------------------------------------------------------

    def test_edit_question_fully_success(self):
        schema = Schema({
            'id': int,
            'question': str,
            'answer': str,
            'difficulty': int,
            'category': int
        })

        res = self.client().put('/questions/1', json={
            'question': 'Who are you?',
            'answer': 'Someone',
            'difficulty': 5,
            'category': 1
        })

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 200)
        self.assertTrue('success' in data)
        self.assertTrue('question' in data)

        (success, question) = (data['success'], data['question'])

        # check success
        self.assertEqual(success, True)

        # check question
        self.assertTrue(schema.is_valid(question))
        self.assertEqual(question['id'], 1)
        self.assertEqual(question['question'], 'Who are you?')
        self.assertEqual(question['answer'], 'Someone')
        self.assertEqual(question['difficulty'], 5)
        self.assertEqual(question['category'], 1)

        # check edited question
        self.assertEqual(json.loads(self.client().get('/questions/1').data)['question'], question)

    def test_edit_question_fully_fail_bad_input(self):
        res = self.client().put('/questions/1', json={
            'question': 'Who are you?',
            'category': 'sad'
        })

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 400)
        self.assertTrue('success' in data)
        self.assertTrue('error' in data)
        self.assertTrue('description' in data)
        self.assertTrue('message' in data)

        # check success
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['description'], 'input question was bad or not formatted correctly')
        self.assertEqual(data['message'], 'bad request')

    def test_edit_question_fully_fail_no_question(self):
        res = self.client().put('/questions/6', json={
            'question': 'Who are you?',
            'answer': 'Someone',
            'difficulty': 5,
            'category': 1
        })

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 422)
        self.assertTrue('success' in data)
        self.assertTrue('error' in data)
        self.assertTrue('description' in data)
        self.assertTrue('message' in data)

        # check success
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['description'], 'no question found with id 6')
        self.assertEqual(data['message'], 'unprocessable entity')

    def test_edit_question_partially_success(self):
        schema = Schema({
            'id': int,
            'question': str,
            'answer': str,
            'difficulty': int,
            'category': int
        })

        res = self.client().patch('/questions/1', json={
            'question': 'Who are you?',
            'category': 1
        })

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 200)
        self.assertTrue('success' in data)
        self.assertTrue('question' in data)

        (success, question) = (data['success'], data['question'])

        # check success
        self.assertEqual(success, True)

        # check question
        self.assertTrue(schema.is_valid(question))
        self.assertEqual(question['id'], 1)
        self.assertEqual(question['question'], 'Who are you?')
        self.assertEqual(question['answer'], self.temp_questions[0].answer)
        self.assertEqual(question['difficulty'], self.temp_questions[0].difficulty)
        self.assertEqual(question['category'], 1)

        # check edited question
        self.assertEqual(json.loads(self.client().get('/questions/1').data)['question'], question)

    def test_edit_question_partially_fail_bad_input(self):
        res = self.client().patch('/questions/1', json={
            'category': 'sad'
        })

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 400)
        self.assertTrue('success' in data)
        self.assertTrue('error' in data)
        self.assertTrue('description' in data)
        self.assertTrue('message' in data)

        # check success
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['description'], 'input question was bad or not formatted correctly')
        self.assertEqual(data['message'], 'bad request')

    def test_edit_question_partially_fail_no_question(self):
        res = self.client().patch('/questions/6', json={
            'question': 'Who are you?',
            'answer': 'Someone',
            'difficulty': 5,
            'category': 1
        })

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 422)
        self.assertTrue('success' in data)
        self.assertTrue('error' in data)
        self.assertTrue('description' in data)
        self.assertTrue('message' in data)

        # check success
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['description'], 'no question found with id 6')
        self.assertEqual(data['message'], 'unprocessable entity')

    #  Delete questions
    #  ----------------------------------------------------------------

    def test_delete_question_success(self):
        schema = Schema({
            'id': int,
            'question': str,
            'answer': str,
            'difficulty': int,
            'category': int
        })

        res = self.client().delete('/questions/1')

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 200)
        self.assertTrue('success' in data)
        self.assertTrue('question' in data)

        # check success
        self.assertEqual(data['success'], True)

        # check question
        question = data['question']
        self.assertTrue(schema.is_valid(question))
        self.assertEqual(question, self.temp_questions[0].format())

    def test_delete_question_fail_no_question(self):
        res = self.client().delete('/questions/6')

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 422)
        self.assertTrue('success' in data)
        self.assertTrue('error' in data)
        self.assertTrue('description' in data)
        self.assertTrue('message' in data)

        # check success
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['description'], 'no question found with id 6')
        self.assertEqual(data['message'], 'unprocessable entity')

    #  No body
    #  ----------------------------------------------------------------

    def test_post_questions_fail_no_body(self):
        res = self.client().post('/questions')

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 400)
        self.assertTrue('success' in data)
        self.assertTrue('error' in data)
        self.assertTrue('description' in data)
        self.assertTrue('message' in data)

        (success, error, description, message) = (data['success'], data['error'], data['description'], data['message'])

        # check success
        self.assertFalse(success)
        self.assertEqual(error, 400)
        self.assertEqual(description, 'no json body was found')
        self.assertEqual(message, 'bad request')

    def test_put_questions_fail_no_body(self):
        res = self.client().put('/questions/1')

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 400)
        self.assertTrue('success' in data)
        self.assertTrue('error' in data)
        self.assertTrue('description' in data)
        self.assertTrue('message' in data)

        (success, error, description, message) = (data['success'], data['error'], data['description'], data['message'])

        # check success
        self.assertFalse(success)
        self.assertEqual(error, 400)
        self.assertEqual(description, 'no json body was found')
        self.assertEqual(message, 'bad request')

    def test_patch_questions_fail_no_body(self):
        res = self.client().patch('/questions/1')

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 400)
        self.assertTrue('success' in data)
        self.assertTrue('error' in data)
        self.assertTrue('description' in data)
        self.assertTrue('message' in data)

        (success, error, description, message) = (
            data['success'], data['error'], data['description'], data['message'])

        # check success
        self.assertFalse(success)
        self.assertEqual(error, 400)
        self.assertEqual(description, 'no json body was found')
        self.assertEqual(message, 'bad request')

    #----------------------------------------------------------------------------#
    # Categories.
    #----------------------------------------------------------------------------#

    #  Get categories
    #  ----------------------------------------------------------------

    def test_get_categories_success(self):
        schema = Schema({
            'id': int,
            'type': str,
            'questions': [int],
        })

        res = self.client().get('/categories')

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 200)
        self.assertTrue('success' in data)
        self.assertTrue('categories' in data)

        (success, categories) = (data['success'], data['categories'])

        # check success
        self.assertEqual(success, True)

        # check categories
        for i in range(len(categories)):
            category = categories[i]
            self.assertTrue(schema.is_valid(category))
            self.assertEqual(category, self.temp_categories[i].format())

    def test_get_categories_fail_no_categories(self):
        db.drop_all()
        db.create_all()

        res = self.client().get('/categories')

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 404)
        self.assertTrue('success' in data)
        self.assertTrue('error' in data)
        self.assertTrue('description' in data)
        self.assertTrue('message' in data)

        # check success
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['description'], 'no categories found')
        self.assertEqual(data['message'], 'not found')

    def test_get_category_success(self):
        schema = Schema({
            'id': int,
            'type': str,
            'questions': [int],
        })

        res = self.client().get('/categories/1')

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 200)
        self.assertTrue('success' in data)
        self.assertTrue('category' in data)

        # check success
        self.assertEqual(data['success'], True)

        # check category
        category = data['category']
        self.assertTrue(schema.is_valid(category))
        self.assertEqual(category, self.temp_categories[0].format())

    def test_get_category_fail_no_category(self):
        res = self.client().get('/categories/8')

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 404)
        self.assertTrue('success' in data)
        self.assertTrue('error' in data)
        self.assertTrue('description' in data)
        self.assertTrue('message' in data)

        # check success
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['description'], 'no category found with id 8')
        self.assertEqual(data['message'], 'not found')

    #  Get category questions
    #  ----------------------------------------------------------------

    def test_get_category_questions_success(self):
        category_schema = Schema({
            'id': int,
            'type': str,
            'questions': [int],
        })

        question_schema = Schema({
            'id': int,
            'question': str,
            'answer': str,
            'difficulty': int,
            'category': int
        })

        res = self.client().get('/categories/1/questions')

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 200)
        self.assertTrue('success' in data)
        self.assertTrue('category' in data)
        self.assertTrue('questions' in data)

        (success, category, questions) = (data['success'], data['category'], data['questions'])

        # check success
        self.assertEqual(success, True)

        # check category
        category = data['category']
        self.assertTrue(category_schema.is_valid(category))
        self.assertEqual(category, self.temp_categories[0].format())

        # check questions
        for i in range(len(questions)):
            question = questions[i]
            self.assertTrue(question_schema.is_valid(question))
            self.assertEqual(question, self.temp_categories[0].questions[i].format())

    def test_get_category_questions_fail_wrong_category(self):
        res = self.client().get('/categories/8/questions')

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 404)
        self.assertTrue('success' in data)
        self.assertTrue('error' in data)
        self.assertTrue('description' in data)
        self.assertTrue('message' in data)

        # check success
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['description'], 'no category found with id 8')
        self.assertEqual(data['message'], 'not found')

    def test_get_category_questions_fail_no_questions(self):
        db.session.add(Category('Physics'))
        db.session.commit()

        res = self.client().get('/categories/7/questions')

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 404)
        self.assertTrue('success' in data)
        self.assertTrue('error' in data)
        self.assertTrue('description' in data)
        self.assertTrue('message' in data)

        # check success
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['description'], 'no questions found in category 7')
        self.assertEqual(data['message'], 'not found')

    #  Search questions
    #  ----------------------------------------------------------------

    def test_search_question_success(self):
        schema = Schema({
            'id': int,
            'question': str,
            'answer': str,
            'difficulty': int,
            'category': int
        })

        res = self.client().post('/questions', json={
            'search_term': 'what'
        })

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 200)
        self.assertTrue('success' in data)
        self.assertTrue('questions' in data)
        self.assertTrue('total_questions' in data)
        self.assertTrue('search_term' in data)

        # check success
        self.assertEqual(data['success'], True)

        # check question
        questions = data['questions']
        total_questions = data['total_questions']
        search_term = data['search_term']
        self.assertEqual(search_term, 'what')
        self.assertEqual(total_questions, 2)
        self.assertTrue(schema.is_valid(questions[0]))
        self.assertEqual(questions[0], self.temp_questions[1].format())
        self.assertTrue(schema.is_valid(questions[1]))
        self.assertEqual(questions[1], self.temp_questions[4].format())

    #  Search category questions
    #  ----------------------------------------------------------------

    def test_search_category_question_success(self):
        schema = Schema({
            'id': int,
            'question': str,
            'answer': str,
            'difficulty': int,
            'category': int
        })

        res = self.client().post('/categories/4/questions', json={
            'search_term': 'what'
        })

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 200)
        self.assertTrue('success' in data)
        self.assertTrue('questions' in data)
        self.assertTrue('total_questions' in data)
        self.assertTrue('search_term' in data)

        # check success
        self.assertEqual(data['success'], True)

        # check question
        questions = data['questions']
        total_questions = data['total_questions']
        search_term = data['search_term']
        self.assertEqual(search_term, 'what')
        self.assertEqual(total_questions, 1)
        self.assertTrue(schema.is_valid(questions[0]))
        self.assertEqual(questions[0], self.temp_questions[1].format())

    def test_search_category_question_fail_bad_input(self):
        res = self.client().post('/categories/1/questions', json={
            'silk': 'what'
        })

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 400)
        self.assertTrue('success' in data)
        self.assertTrue('error' in data)
        self.assertTrue('description' in data)
        self.assertTrue('message' in data)

        # check success
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['description'], 'no search term found')
        self.assertEqual(data['message'], 'bad request')

    def test_search_category_question_fail_no_category(self):
        res = self.client().post('/categories/8/questions', json={
            'search_term': 'what'
        })

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 404)
        self.assertTrue('success' in data)
        self.assertTrue('error' in data)
        self.assertTrue('description' in data)
        self.assertTrue('message' in data)

        # check success
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['description'], 'no category found with id 8')
        self.assertEqual(data['message'], 'not found')

    def test_search_category_question_fail_no_questions(self):
        res = self.client().post('/categories/1/questions', json={
            'search_term': 'sadsadsad'
        })

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 404)
        self.assertTrue('success' in data)
        self.assertTrue('error' in data)
        self.assertTrue('description' in data)
        self.assertTrue('message' in data)

        # check success
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['description'], "no questions with search term 'sadsadsad' found in category 1")
        self.assertEqual(data['message'], 'not found')

    #----------------------------------------------------------------------------#
    # Quizzes.
    #----------------------------------------------------------------------------#

    #  Post quizzes
    #  ----------------------------------------------------------------

    def test_quizzes_all_success(self):
        schema = Schema({
            'id': int,
            'question': str,
            'answer': str,
            'difficulty': int,
            'category': int
        })

        res = self.client().post('/quizzes', json={
            'previous_questions': [2, 3, 4, 5]
        })

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 200)
        self.assertTrue('success' in data)
        self.assertTrue('question' in data)
        self.assertTrue('total_questions' in data)

        # check success
        self.assertEqual(data['success'], True)

        # check question
        question = data['question']
        total_questions = data['total_questions']
        self.assertTrue(schema.is_valid(question))
        self.assertEqual(question, self.temp_questions[0].format())
        self.assertEqual(total_questions, 1)

    def test_quizzes_category_success(self):
        schema = Schema({
            'id': int,
            'question': str,
            'answer': str,
            'difficulty': int,
            'category': int
        })

        res = self.client().post('/quizzes', json={
            'previous_questions': [2],
            'quiz_category': 4
        })

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 200)
        self.assertTrue('success' in data)
        self.assertTrue('question' in data)
        self.assertTrue('total_questions' in data)

        # check success
        self.assertEqual(data['success'], True)

        # check question
        question = data['question']
        total_questions = data['total_questions']
        self.assertTrue(schema.is_valid(question))
        self.assertEqual(question, self.temp_questions[0].format())
        self.assertEqual(total_questions, 1)

    def test_quizzes_fail_bad_input(self):
        res = self.client().post('/quizzes', json={
            'quiz_category': 'dsad'
        })

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 400)
        self.assertTrue('success' in data)
        self.assertTrue('error' in data)
        self.assertTrue('description' in data)
        self.assertTrue('message' in data)

        (success, error, description, message) = (data['success'], data['error'], data['description'], data['message'])

        # check success
        self.assertFalse(success)
        self.assertEqual(error, 400)
        self.assertEqual(description, 'quiz input was bad or not formatted correctly')
        self.assertEqual(message, 'bad request')

    def test_quizzes_fail_no_body(self):
        res = self.client().post('/quizzes')

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 400)
        self.assertTrue('success' in data)
        self.assertTrue('error' in data)
        self.assertTrue('description' in data)
        self.assertTrue('message' in data)

        (success, error, description, message) = (data['success'], data['error'], data['description'], data['message'])

        # check success
        self.assertFalse(success)
        self.assertEqual(error, 400)
        self.assertEqual(description, 'no json body was found')
        self.assertEqual(message, 'bad request')

    #----------------------------------------------------------------------------#
    # Error Handling.
    #----------------------------------------------------------------------------#
    def test_method_not_allowed(self):
        res = self.client().post('/categories')

        status = res.status_code
        data = json.loads(res.data)

        # check status and data
        self.assertEqual(status, 405)
        self.assertTrue('success' in data)
        self.assertTrue('error' in data)
        self.assertTrue('description' in data)
        self.assertTrue('message' in data)

        (success, error, description, message) = (data['success'], data['error'], data['description'], data['message'])

        # check success
        self.assertFalse(success)
        self.assertEqual(error, 405)
        self.assertEqual(description, 'The method is not allowed for the requested URL.')
        self.assertEqual(message, 'method is not allowed')


if __name__ == "__main__":
    unittest.main()
