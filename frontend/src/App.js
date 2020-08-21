import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

import './stylesheets/App.css';
import Header from './components/Header';
import QuestionView from './components/QuestionView';
import FormView from './components/FormView';
import QuizView from './components/QuizView';

class App extends Component {
    render() {
        return (
            <div className="App">
                <Header path />
                <Router>
                    <Switch>
                        <Route path="/" exact component={QuestionView} />
                        <Route path="/add" component={FormView} />
                        <Route path="/play" component={QuizView} />
                        <Route component={QuestionView} />
                    </Switch>
                </Router>
            </div>
        );
    }
}

export default App;
