import React, { Component } from 'react';
import $ from 'jquery';

import '../stylesheets/FormView.css';

class FormView extends Component {
    state = {
        question: '',
        answer: '',
        difficulty: 1,
        category: 1,
        categories: {},
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

    submitQuestion = (event) => {
        event.preventDefault();
        $.ajax({
            url: 'http://localhost:5000/questions', //TODO: update request URL
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                question: this.state.question,
                answer: this.state.answer,
                difficulty: this.state.difficulty,
                category: this.state.category,
            }),
            crossDomain: true,
            success: (result) => {
                document.getElementById('add-question-form').reset();
            },
            error: (error) => {
                alert(`Unable to add question. Error: ${error.responseText}`);
            },
        });
    };

    handleChange = (event) => {
        this.setState({ [event.target.name]: event.target.value });
    };

    render() {
        return (
            <div id="add-form">
                <h2>Add a New Trivia Question</h2>
                <form className="form-view" id="add-question-form" style={{ width: '300px', margin: 'auto' }} onSubmit={this.submitQuestion}>
                    <div style={{ width: '300px', margin: 'auto', display: 'flex', justifyContent: 'space-between' }}>
                        <label htmlFor="question">Question</label>
                        <input type="text" id="question" name="question" onChange={this.handleChange} />
                    </div>
                    <div style={{ width: '300px', margin: 'auto', display: 'flex', justifyContent: 'space-between' }}>
                        <label htmlFor="answer">Answer</label>
                        <input type="text" id="answer" name="answer" onChange={this.handleChange} />
                    </div>
                    <div style={{ width: '300px', margin: 'auto', display: 'flex', justifyContent: 'space-between' }}>
                        <label htmlFor="difficulty">Difficulty</label>
                        <select id="difficulty" name="difficulty" onChange={this.handleChange}>
                            <option value="1">1</option>
                            <option value="2">2</option>
                            <option value="3">3</option>
                            <option value="4">4</option>
                            <option value="5">5</option>
                        </select>
                    </div>
                    <div style={{ width: '300px', margin: 'auto', display: 'flex', justifyContent: 'space-between' }}>
                        <label htmlFor="category">Category</label>
                        <select id="category" name="category" onChange={this.handleChange}>
                            {Object.keys(this.state.categories).map((id) => {
                                return (
                                    <option key={id} value={id}>
                                        {this.state.categories[id]}
                                    </option>
                                );
                            })}
                        </select>
                    </div>
                    <input type="submit" className="button" value="Submit" />
                </form>
            </div>
        );
    }
}

export default FormView;
