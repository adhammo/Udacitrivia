# Trivia API

## About

**Trivia API** is used as the back-end for **Udacitrivia** full-stack web application.

**Udacitrivia** front-end uses **Trivia API** to retrieve, store, and manipulate questions and categories in order to play a game of trivia.

## Getting Started

### Create Trivia Database

Create a database called **"trivia"** which will be used by the API to store questions and categories data.

Open up a new shell terminal and type in the following commands:

1. Follow this guide to [Install PostgreSQL ](https://www.postgresqltutorial.com/install-postgresql/) on your machine
2. Follow this guide to [Start PostgreSQL service](https://tableplus.com/blog/2018/10/how-to-start-stop-restart-postgresql-server.html) on your machine
3. Create a new database called **"trivia"**
    ```bash
    dropdb trivia && createdb trivia
    ```
4. Create a new database called **"trivia_test"** which is used for testing (optional)
    ```bash
    dropdb trivia_test && createdb trivia_test
    ```

### Setup Virtual Environment (Optional)

Follow this guide to [Setup a Virtual Environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) and **activate** it then continue following the next steps using virtual env.

```bash
pip install virtualenv
virtualenv env
```

##### Activation:

```bash
# Windows
	env\Scripts\activate
# Mac OS / Linux:
	source env/bin/activate
```

### Install Dependencies

Install all required packages:

```bash
cd backend
pip install -r requirements.txt
```

# Test API

Run the following command to test **Trivia API**:

```bash
cd backend
py test_flaskr.py
```

# Set Flask App

Set flask app to flaskr and environment to development (debug).

```bash
# Windows
cd backend
set FLASK_APP=flaskr
set FLASK_ENV=development

# Mac OS / Linux
cd backend
export FLASK_APP=flaskr
export FLASK_ENV=development
```

### Migrate Database Schema

Initialize and upgrade a migration for **trivia** database to create the tables necessary for the API to function correctly:

```bash
cd backend
flask db init
flask db migrate
flask db upgrade
```

### Add Template Data

Here are some data to insert into your questions and categories tables to simulate real data.

**Categories:**

```sql
INSERT INTO categories(type)
VALUES 	('Science'),
		('Art'),
		('Geography'),
		('History'),
		('Entertainment'),
		('Sports');
```

**Questions:**

```sql
INSERT INTO questions(question, answer, difficulty, category_id)
VALUES 	('Whose autobiography is entitled ''I Know Why the Caged Bird Sings''?', 'Maya Angelou', 2, 4),
		('What boxer''s original name is Cassius Clay?', 'Muhammad Ali', 1, 4),
		('What movie earned Tom Hanks his third straight Oscar nomination, in 1996?', 'Apollo 13', 4, 5),
		('What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?', 'Tom Cruise', 4, 5),
		('What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?', 'Edward Scissorhands', 3, 5),
		('Which is the only team to play in every soccer World Cup tournament?', 'Brazil', 3, 6),
		('Which country won the first ever soccer World Cup in 1930?', 'Uruguay', 4, 6),
		('Who invented Peanut Butter?', 'George Washington Carver', 2, 4),
		('What is the largest lake in Africa?', 'Lake Victoria', 2, 3),
		('In which royal palace would you find the Hall of Mirrors?', 'The Palace of Versailles', 3, 3),
		('The Taj Mahal is located in which Indian city?', 'Agra', 2, 3),
		('Which Dutch graphic artist–initials M C was a creator of optical illusions?', 'Escher', 1, 2),
		('La Giaconda is better known as what?', 'Mona Lisa', 3, 2),
		('How many paintings did Van Gogh sell in his lifetime?', 'One', 4, 2),
		('Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?', 'Jackson Pollock', 2, 2),
		('What is the heaviest organ in the human body?', 'The Liver', 4, 1),
		('Who discovered penicillin?', 'Alexander Fleming', 3, 1),
		('Hematology is a branch of medicine involving the study of what?', 'Blood', 4, 1),
		('Which dung beetle was worshipped by the ancient Egyptians?', 'Scarab', 4, 4);
```

### Run Flask Application

Follow this guide [Flask Quickstart](https://flask.palletsprojects.com/en/1.1.x/quickstart/) to know more ways to run a flask app.

```bash
flask run
```

## Introduction

**Trivia API** is designed to run locally on your machine.

Invoke the following endpoint to interact with **Trivia API**:

```http
Endpoint: http://localhost:5000/
```

### Schema

**Trivia API** has two main objects; a Question and a Category.

**Question Schema:**

```
{
    "id": number,
    "question": string,
    "answer": string,
    "difficulty": number, 	// a natural number from 1 to 5 inclusive
    "category": number 		// category id (must exist before question)
}
```

**Category Schema:**

```
{
	"id": number,
	"type": string,				// category name
	"questions": [
		(Question Schema),
		(Question Schema),
		...
	]
}
```

### Error Handling

If **Trivia API** couldn't fulfill the request because an error has occurred for any reason it will respond with an error status and with the next standardized message:

```
{
    "error": number, 		// status code
    "message": string, 		// breif error message
    "description": string, 	// detailed error message
    "success": false
}
```

## Questions

### Get All Questions

Retrieves all questions from **trivia** database.

**Request**

```http
GET /questions[?page=<int:page_id>]
Host: localhost:5000
```

**Response**

```
{
	"questions": [
		(Question Schema),
		(Question Schema),
		...
	],
	"total_questions": number,
	"success": true
}
```

### Get a Question

Retrieves a question from **trivia** database.

**Request**

```http
GET /questions/<int:question_id>
Host: localhost:5000
```

**Response**

```
{
	"question": (Question Schema),
	"success": true
}
```

### Search Questions

Retrieves all questions in **trivia** database that include a **search term** as a sub-string.

**Request**

```http
POST /questions[?page=<int:page_id>]
Host: localhost:5000
```

with body:

```
{
    "search_term": string
}
```

**Response**

```
{
	"questions": [					// all or paginated questions
		(Question Schema),
		(Question Schema),
		...
	],
	"total_questions": number,			// count of all questions
	"search_term": string,
	"success": true
}
```

### Create a Question

Creates a new question in **trivia** database.

**Request**

```http
POST /questions
Host: localhost:5000
```

with body:

```
{
    "question": string,
    "answer": string,
    "difficulty": number, 	// a natural number from 1 to 5 inclusive
    "category": number 		// category id (must exist before question)
}
```

> Note: all fields are required.

**Response**
Returns the question that was just created.

```
{
	"question": (Question Schema),
	"success": true
}
```

### Edit a Question

Edits **all** values of a question in **trivia** database.

**Request**

```http
PUT /questions/<int:question_id>
Host: localhost:5000
```

with body:

```
{
    "question": string,
    "answer": string,
    "difficulty": number, 	// a natural number from 1 to 5 inclusive
    "category": number 		// category id (must exist before question)
}
```

> Note: all fields are required.

**Response**
Returns the question that was just edited.

```
{
	"question": (Question Schema),
	"success": true
}
```

### Edit a Question Partially

Edits **some** values of a question in **trivia** database.

**Request**

```http
PATCH /questions/<int:question_id>
Host: localhost:5000
```

with body:

```
{
    "question": string,
    "answer": string,
    "difficulty": number, 	// a natural number from 1 to 5 inclusive
    "category": number 		// category id (must exist before question)
}
```

> Note: none of the fields are required.

**Response**
Returns the question that was just edited.

```
{
	"question": (Question Schema),
	"success": true
}
```

### Delete a Question

Delete a question from **trivia** database.

**Request**

```http
DELETE /questions/<int:question_id>
Host: localhost:5000
```

**Response**
Returns the question that was just deleted.

```
{
	"question": (Question Schema),
	"success": true
}
```

## Categories

### Get All Categories

Retrieves all categories from **trivia** database.

**Request**

```http
GET /categories
Host: localhost:5000
```

**Response**

```
{
	"categories": [
		(Category Schema),
		(Category Schema),
		...
	],
	"success": true
}
```

### Get a Category

Retrieves a category from **trivia** database.

**Request**

```http
GET /categories/<int:category_id>
Host: localhost:5000
```

**Response**

```
{
	"category": (Category Schema),
	"success": true
}
```

### Get Category Questions

Retrieves questions of a category from **trivia** database.

**Request**

```http
GET /categories/<int:category_id>/questions[?page=<int:page_id>]
Host: localhost:5000
```

**Response**

```
{
	"category": (Category Schema),
	"questions" [					// all or paginated questions
		(Question Schema),
		(Question Schema),
		...
	],
	"total_questions": number, 			// count of all questions
	"success": true
}
```

### Search Category Questions

Retrieves all questions of a category in **trivia** database that include a **search term** as a sub-string.

**Request**

```http
POST /questions[?page=<int:page_id>]
Host: localhost:5000
```

with body:

```
{
    "search_term": string
}
```

**Response**

```
{
	"category": (Category Schema),
	"questions": [				// all or paginated questions
		(Question Schema),
		(Question Schema),
		...
	],
	"total_questions": number,		// count of all questions
	"search_term": string,
	"success": true
}
```

## Quizzes

### Play a Quiz

Retrieves a unique random question (optionally in a category) from **trivia** database.

**Request**

```http
POST /quizzes
Host: localhost:5000
```

with body:

```
{
	"quiz_category": (Category Schema),
	"previous_questions": [
		(Question Schema),
		(Question Schema),
		...
	]
}
```

> Note: quiz_category is optional.

**Response**

```
{
	"category": (Category Schema),		// only if provided a quiz_category
	"questions": [				// all or paginated questions
		(Question Schema),
		(Question Schema),
		...
	],
	"total_questions": number,		// count of all questions
	"search_term": string,
	"success": true
}
```
