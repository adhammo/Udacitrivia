import React, { Component } from 'react';
import PropTypes from 'prop-types';

class Search extends Component {
    state = {
        query: '',
    };

    getInfo = (event) => {
        event.preventDefault();
        this.props.submitSearch(this.state.query);
    };

    handleInputChange = () => {
        this.setState({
            query: this.search.value,
        });
    };

    render() {
        return (
            <form
                onSubmit={this.getInfo}
                style={{
                    marginLeft: 'auto',
                    marginRight: 'auto',
                    width: '200px',
                    padding: '20px',
                    borderRadius: '4px',
                    backgroundColor: '#aaa',
                }}
            >
                <input placeholder="Search questions..." ref={(input) => (this.search = input)} style={{ width: '100%', boxSizing: 'border-box' }} onChange={this.handleInputChange} />
                <input type="submit" value="Submit" className="button" />
            </form>
        );
    }
}

Search.propTypes = {
    submitSearch: PropTypes.func.isRequired,
};

export default Search;
