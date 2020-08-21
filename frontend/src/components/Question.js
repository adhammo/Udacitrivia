import React, { Component } from 'react';
import PropTypes from 'prop-types';

import '../stylesheets/Question.css';

class Question extends Component {
    state = {
        visibleAnswer: false,
    };

    flipVisibility = () => {
        this.setState({ visibleAnswer: !this.state.visibleAnswer });
    };

    render() {
        const { question, answer, category, difficulty } = this.props;
        return (
            <div className="Question-holder">
                <div className="Question">{question}</div>
                <div className="Question-status">
                    <img className="category" src={`${category}.svg`} alt={`${category} icon`} />
                    <div className="difficulty">Difficulty: {difficulty}</div>
                    <img src="delete.png" className="delete" style={{ cursor: 'pointer' }} onClick={() => this.props.questionAction('DELETE')} alt="delete question" />
                </div>
                <div className="show-answer button" style={{ cursor: 'pointer', width: 'fit-content' }} onClick={this.flipVisibility}>
                    {this.state.visibleAnswer ? 'Hide' : 'Show'} Answer
                </div>
                <div className="answer-holder">
                    <span style={{ visibility: this.state.visibleAnswer ? 'visible' : 'hidden' }}>Answer: {answer}</span>
                </div>
            </div>
        );
    }
}

Question.propTypes = {
    question: PropTypes.string.isRequired,
    answer: PropTypes.string.isRequired,
    category: PropTypes.string.isRequired,
    difficulty: PropTypes.number.isRequired,
    questionAction: PropTypes.func.isRequired,
};

export default Question;
