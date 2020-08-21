import React, { Component } from 'react';
import $ from 'jquery';
import '../stylesheets/App.css';

import Question from './Question';
import Search from './Search';

class QuestionView extends Component {
    state = {
        page: 1,
        questions: [],
        totalQuestions: 0,
        categories: {},
        currentCategory: null,
        searchTerm: null,
        view: 'questions',
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

    getQuestions = () => {
        $.ajax({
            url: `http://localhost:5000/questions?page=${this.state.page}`,
            type: 'GET',
            success: (result) => {
                this.setState({
                    questions: result.questions,
                    totalQuestions: result.total_questions,
                    currentCategory: null,
                    view: 'questions',
                });
            },
            error: (error) => {
                if (error.responseJSON['error'] === 404) {
                    this.setState({
                        questions: [],
                        totalQuestions: 0,
                        currentCategory: null,
                        view: 'questions',
                    });
                } else {
                    alert(`Unable to load questions. Error: ${error.responseText}`);
                }
            },
        });
    };

    getCategoryQuestions = (id) => {
        $.ajax({
            url: `http://localhost:5000/categories/${id}/questions?page=${this.state.page}`,
            type: 'GET',
            success: (result) => {
                this.setState({
                    questions: result.questions,
                    totalQuestions: result.total_questions,
                    currentCategory: id,
                    view: 'categoryQuestions',
                });
            },
            error: (error) => {
                if (error.responseJSON['error'] === 404) {
                    this.setState({
                        questions: [],
                        totalQuestions: 0,
                        currentCategory: id,
                        view: 'categoryQuestions',
                    });
                } else {
                    alert(`Unable to load category questions. Error: ${error.responseText}`);
                }
            },
        });
    };

    searchQuestions = (searchTerm) => {
        $.ajax({
            url: `http://localhost:5000/questions?page=${this.state.page}`,
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({ search_term: searchTerm }),
            crossDomain: true,
            success: (result) => {
                this.setState({
                    questions: result.questions,
                    totalQuestions: result.total_questions,
                    currentCategory: null,
                    searchTerm: searchTerm,
                    view: 'searchQuestions',
                });
            },
            error: (error) => {
                if (error.responseJSON['error'] === 404) {
                    this.setState({
                        questions: [],
                        totalQuestions: 0,
                        currentCategory: null,
                        searchTerm: searchTerm,
                        view: 'searchQuestions',
                    });
                } else {
                    alert(`Unable to search questions. Error: ${error.responseText}`);
                }
            },
        });
    };

    searchCategoryQuestions = (id, searchTerm) => {
        $.ajax({
            url: `http://localhost:5000/categories/${id}/questions?page=${this.state.page}`,
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({ search_term: searchTerm }),
            crossDomain: true,
            success: (result) => {
                this.setState({
                    questions: result.questions,
                    totalQuestions: result.total_questions,
                    currentCategory: id,
                    searchTerm: searchTerm,
                    view: 'searchCategoryQuestions',
                });
            },
            error: (error) => {
                if (error.responseJSON['error'] === 404) {
                    this.setState({
                        questions: [],
                        totalQuestions: 0,
                        currentCategory: id,
                        searchTerm: searchTerm,
                        view: 'searchCategoryQuestions',
                    });
                } else {
                    alert(`Unable to search category questions. Error: ${error.responseText}`);
                }
            },
        });
    };

    questionAction = (id) => (action) => {
        if (action === 'DELETE') {
            if (window.confirm('Are you sure you want to delete the question?')) {
                $.ajax({
                    url: `http://localhost:5000/questions/${id}`,
                    type: 'DELETE',
                    success: (result) => {
                        if (this.state.view === 'questions') this.getQuestions();
                        else if (this.state.view === 'categoryQuestions') this.getCategoryQuestions(this.state.currentCategory);
                        else if (this.state.view === 'searchQuestions') this.searchQuestions(this.state.searchTerm);
                        else if (this.state.view === 'searchCategoryQuestions') this.searchCategoryQuestions(this.state.currentCategory, this.state.searchTerm);
                    },
                    error: (error) => {
                        alert(`Unable to delete question. Error: ${error.responseText}`);
                    },
                });
            }
        }
    };

    selectPage(num) {
        this.setState({ page: num }, () => {
            if (this.state.view === 'questions') this.getQuestions();
            else if (this.state.view === 'categoryQuestions') this.getCategoryQuestions(this.state.currentCategory);
            else if (this.state.view === 'searchQuestions') this.searchQuestions(this.state.searchTerm);
            else if (this.state.view === 'searchCategoryQuestions') this.searchCategoryQuestions(this.state.currentCategory, this.state.searchTerm);
        });
    }

    createPagination() {
        let pageNumbers = [];
        let maxPage = Math.ceil(this.state.totalQuestions / 10);
        for (let i = 1; i <= maxPage; i++) {
            pageNumbers.push(
                <span
                    key={i}
                    className={`page-num ${i === this.state.page ? 'active' : ''}`}
                    style={{
                        cursor: i === this.state.page ? 'default' : 'pointer',
                    }}
                    onClick={() => {
                        this.selectPage(i);
                    }}
                >
                    {i}
                </span>
            );
        }
        return pageNumbers;
    }

    render() {
        return (
            <div className="question-view">
                <div className="categories-list" style={{ backgroundColor: '#dddddd', paddingBottom: '15px' }}>
                    <h2
                        style={{
                            cursor: 'pointer',
                            marginLeft: 'auto',
                            marginRight: 'auto',
                            width: '200px',
                            padding: '20px',
                            color: this.state.currentCategory === null ? 'white' : 'black',
                            backgroundColor: this.state.currentCategory === null ? '#222222' : '#f4f4f4',
                        }}
                        onClick={() => {
                            this.setState({ page: 1 }, this.getQuestions);
                        }}
                    >
                        All Categories
                    </h2>
                    <ul
                        style={{
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                        }}
                    >
                        {Object.keys(this.state.categories).map((id) => {
                            return (
                                <li
                                    key={id}
                                    style={{
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        width: '200px',
                                        padding: '20px',
                                        color: this.state.currentCategory === id ? 'white' : 'black',
                                        backgroundColor: this.state.currentCategory === id ? '#222222' : '#f4f4f4',
                                        cursor: 'pointer',
                                    }}
                                    onClick={() => {
                                        this.setState({ page: 1 }, () => {
                                            this.getCategoryQuestions(id);
                                        });
                                    }}
                                >
                                    <img className="category" style={{ width: '24px', marginRight: '10px', filter: this.state.currentCategory === id ? 'invert(.5) sepia(1) saturate(5) hue-rotate(175deg)' : 'none' }} src={`${this.state.categories[id]}.svg`} alt={`${this.state.categories[id]} icon`} />
                                    {this.state.categories[id]}
                                </li>
                            );
                        })}
                    </ul>
                    <Search
                        submitSearch={(searchTerm) => {
                            this.setState({ page: 1 }, () => {
                                if (this.state.view === 'questions' || this.state.view === 'searchQuestions') this.searchQuestions(searchTerm);
                                else if (this.state.view === 'categoryQuestions' || this.state.view === 'searchCategoryQuestions') this.searchCategoryQuestions(this.state.currentCategory, searchTerm);
                            });
                        }}
                    />
                </div>
                <div className="questions-list" style={{ paddingBottom: '15px' }}>
                    <h2>Questions</h2>
                    <p style={{ display: this.state.totalQuestions === 0 ? 'block' : 'none' }}>No questions found.</p>
                    {this.state.questions.map((q) => (
                        <Question key={q.id} question={q.question} answer={q.answer} category={this.state.categories[q.category]} difficulty={q.difficulty} questionAction={this.questionAction(q.id)} />
                    ))}
                    <div className="pagination-menu">{this.createPagination()}</div>
                </div>
            </div>
        );
    }
}

export default QuestionView;
