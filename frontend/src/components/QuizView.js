import React, { Component } from 'react';
import $ from 'jquery';

import '../stylesheets/QuizView.css';

const questionsPerPlay = 5;

class QuizView extends Component {
    state = {
        quizCategory: null,
        previousQuestions: [],
        showAnswer: false,
        categories: {},
        numCorrect: 0,
        currentQuestion: {},
        guess: '',
        forceEnd: false,
    };

    componentDidMount() {
        this.getCategories();
    }

    getCategories = () => {
        $.ajax({
            url: 'http://localhost:5000/categories',
            type: 'GET',
            success: (result) => {
                let categoriesObject = {};
                for (const category of result.categories) {
                    categoriesObject[`${category.id}`] = category.type;
                }
                this.setState({ categories: categoriesObject }, this.getQuestions);
            },
            error: (error) => {
                alert(`Unable to load categories. Error: ${error.responseText}`);
            },
        });
    };

    getNextQuestion = () => {
        const previousQuestions = [...this.state.previousQuestions];
        if (this.state.currentQuestion.id) {
            previousQuestions.push(this.state.currentQuestion.id);
        }

        $.ajax({
            url: 'http://localhost:5000/quizzes',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                previous_questions: previousQuestions,
                quiz_category: this.state.quizCategory ? this.state.quizCategory.id : null,
            }),
            crossDomain: true,
            success: (result) => {
                this.setState({
                    showAnswer: false,
                    previousQuestions: previousQuestions,
                    currentQuestion: result.question,
                    guess: '',
                    forceEnd: result.question ? false : true,
                });
            },
            error: (error) => {
                alert(`Unable to load question. Error: ${error.responseText}`);
            },
        });
    };

    selectCategory = (category = null) => {
        this.setState({ quizCategory: category }, this.getNextQuestion);
    };

    handleChange = (event) => {
        this.setState({ [event.target.name]: event.target.value });
    };

    submitGuess = (event) => {
        event.preventDefault();
        let evaluate = this.evaluateAnswer();
        this.setState({
            numCorrect: !evaluate ? this.state.numCorrect : this.state.numCorrect + 1,
            showAnswer: true,
        });
    };

    restartGame = () => {
        this.setState({
            quizCategory: null,
            previousQuestions: [],
            showAnswer: false,
            numCorrect: 0,
            currentQuestion: {},
            guess: '',
            forceEnd: false,
        });
    };

    renderPrePlay() {
        return (
            <div className="quiz-play-holder">
                <div className="choose-header">Choose Category</div>
                <div className="category-holder">
                    <div className="play-category" onClick={this.selectCategory}>
                        ALL
                    </div>
                    {Object.keys(this.state.categories).map((id) => {
                        return (
                            <div key={id} value={id} className="play-category" onClick={() => this.selectCategory({ type: this.state.categories[id], id })}>
                                {this.state.categories[id]}
                            </div>
                        );
                    })}
                </div>
            </div>
        );
    }

    renderFinalScore() {
        return (
            <div className="quiz-play-holder">
                <div className="final-header">Your Final Score is {this.state.numCorrect}</div>
                <div className="play-again button" onClick={this.restartGame}>
                    {' '}
                    Play Again?{' '}
                </div>
            </div>
        );
    }

    evaluateAnswer = () => {
        const formatGuess = this.state.guess.replace(/[.,/#!$%^&*;:{}=\-_`~()]/g, '').toLowerCase();
        const answerArray = this.state.currentQuestion.answer.toLowerCase().split(' ');
        return answerArray.includes(formatGuess);
    };

    renderCorrectAnswer() {
        let evaluate = this.evaluateAnswer();
        return (
            <div className="quiz-play-holder">
                <div className="quiz-question">{this.state.currentQuestion.question}</div>
                <div className={`${evaluate ? 'correct' : 'wrong'}`}>{evaluate ? 'You were correct!' : 'You were incorrect'}</div>
                <div className="quiz-answer">{this.state.currentQuestion.answer}</div>
                <div className="next-question button" onClick={this.getNextQuestion}>
                    {' '}
                    Next Question{' '}
                </div>
            </div>
        );
    }

    renderPlay() {
        if (this.state.previousQuestions.length === questionsPerPlay || this.state.forceEnd) {
            return this.renderFinalScore();
        } else if (this.state.showAnswer) {
            return this.renderCorrectAnswer();
        } else {
            return (
                <div className="quiz-play-holder">
                    <div className="quiz-question">{this.state.currentQuestion.question}</div>
                    <form onSubmit={this.submitGuess}>
                        <input type="text" name="guess" onChange={this.handleChange} />
                        <input className="submit-guess button" type="submit" value="Submit Answer" />
                    </form>
                </div>
            );
        }
    }

    render() {
        return this.state.quizCategory ? this.renderPlay() : this.renderPrePlay();
    }
}

export default QuizView;
