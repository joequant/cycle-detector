import React, { Component } from 'react';
import {Button,FormControl, FormGroup,
       ControlLabel} from 'react-bootstrap';
import logo from './logo.svg';
import './App.css';
import request from 'request';
import url from  'url';

var requestParser = (function() {
    var href = document.location.href;
    var urlObj = url.parse(href, true);

    return {
	href,
	urlObj,
	getQueryStringValue: (key) => {
	    let value = ((urlObj && urlObj.query) && urlObj.query[key]) || null;
	    return value;
	},
	uriMinusPath: urlObj.protocol + '//' + urlObj.hostname + ':' + urlObj.port
    };
})();

class App extends Component {
    constructor(props) {
	super(props);
	this.handleFormSubmit = this.handleFormSubmit.bind(this);
	this.state = {
	    description: '',
	    result: ''}
    }
    handleFormSubmit(e) {
	console.log("hello!!!");
	e.preventDefault();
	var me = this;
	request.post(
	    requestParser.uriMinusPath + '/cycle',
	    { json: {data : this.state.description },
	      function (error, response, body) {
		  if (!error && response.statusCode == 200) {
		      me.setState({result: body});
		  }
	      }
	    }
	);
    }
    handleTextAreaChange(e) {
	this.setState({description: e.target.value});
    }
    render() {
	return (
		<div className="App">
		<div className="App-header">
		<h2>Welcome to the cycle detector</h2>
		</div>
		<form onSubmit={this.handleFormSubmit}>
		<FormGroup controlId="formControlsTextarea">
		<ControlLabel>Textarea</ControlLabel>
		<FormControl componentClass="textarea" placeholder="textarea" />
	        </FormGroup>
		<Button type="submit">Calculate</Button>
		</form>
		<p className="App-intro">
		{this.state.result}
		</p>
		</div>
    );
  }
}

export default App;