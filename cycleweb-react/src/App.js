import React, { Component } from 'react';
import {Button,FormControl, FormGroup,
       ControlLabel} from 'react-bootstrap';
import logo from './logo.svg';
import './App.css';
import request from 'request';
import url from  'url';
import 'whatwg-fetch';

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
	this.handleFileSubmit = this.handleFileSubmit.bind(this);
	this.handleTextAreaChange = this.handleTextAreaChange.bind(this);
	this.handleFileChange = this.handleFileChange.bind(this);
	this.state = {
	    description: '',
	    file_upload: '',
	    result: ''}
    }
    handleFormSubmit(e) {
	console.log("hello!!!");
	e.preventDefault();
	var me = this;
	fetch('/cycle', {
	    method: 'POST',
	    headers: {
		'Content-Type': 'application/json'
	    },
	    body: JSON.stringify({
		data : this.state.description
	    })
	}).then(function(response) {
	    return response.json();
	}).then(function(json) {
	    console.log("return!!!", json);
	    me.setState({result: json.result});
	}).catch(function(ex) {
	    console.log('parsing failed', ex);
	    me.setState({result: "Error"});
	});
    }
    handleFileSubmit(e) {
	console.log("hello!!!");
	e.preventDefault();
	var data = new FormData();
	data.append('file', this.state.file_upload[0]);
	var me = this;
	fetch('/cycle', {
	    method: 'POST',
	    body: data
	}).then(function(response) {
	    return response.json();
	}).then(function(json) {
	    console.log("return!!!", json);
	    me.setState({result: json.result});
	}).catch(function(ex) {
	    console.log('parsing failed', ex);
	    me.setState({result: "Error"});
	});
    }
    handleTextAreaChange(e) {
	console.log("hello!!!");
	this.setState({description: e.target.value});
    }
    handleFileChange(e) {
	console.log("hello!!!", e.target.files);
	this.setState({file_upload: e.target.files});
    }

    formatResults() {
	return JSON.stringify(this.state.result);
    }

    render() {
	return (
		<div className="App">
		<div className="App-header">
		<h2>Welcome to the cycle detector</h2>
		</div>
		<form onSubmit={this.handleFileSubmit}>
		<FormGroup controlId="formControlsFile">
		<ControlLabel>File upload</ControlLabel>
		<FormControl type="file"
	    onChange={this.handleFileChange} />
	        </FormGroup>
		<Button type="submit">Calculate</Button>
		</form>

		<hr/>
		<form onSubmit={this.handleFormSubmit}>
		<FormGroup controlId="formControlsTextarea">
		<ControlLabel>Textarea</ControlLabel>
		<FormControl componentClass="textarea"
	    placeholder="textarea"
	    value={this.state.description}
	    onChange={this.handleTextAreaChange} />
	        </FormGroup>
		<Button type="submit">Calculate</Button>
		</form>
		<p className="App-intro">
		{this.formatResults()}
		</p>
		</div>
    );
  }
}

export default App;
