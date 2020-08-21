import React, { Component } from 'react';
import '../stylesheets/Header.css';

class Header extends Component {

  navTo(uri){
    window.location.href = window.location.origin + uri;
  }

  render() {
    return (
      <div className="App-header">
        <h1 style={{ cursor: 'pointer' }} onClick={() => {this.navTo('')}}>Udacitrivia</h1>
        <h2 style={{ cursor: 'pointer', color: window.location.pathname === '/'? '#55dd55' : 'white' }} onClick={() => {this.navTo('')}}>List</h2>
        <h2 style={{ cursor: 'pointer', color: window.location.pathname === '/add'? '#55dd55' : 'white' }} onClick={() => {this.navTo('/add')}}>Add</h2>
        <h2 style={{ cursor: 'pointer', color: window.location.pathname === '/play'? '#55dd55' : 'white' }} onClick={() => {this.navTo('/play')}}>Play</h2>
      </div>
    );
  }
}

export default Header;
