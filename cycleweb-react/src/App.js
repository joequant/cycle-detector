import React, { Component } from 'react';
import {Button, FormControl, FormGroup,
	ControlLabel, Form} from 'react-bootstrap';
import logo from './logo.svg';
import blank from './blank.png';
import './App.css';
import request from 'request';
import url from  'url';
import 'whatwg-fetch';

function CycleLine(props) {
    var data = props.data;
    var header = props.header;
    if (data != null) {
	console.log('cycle-line', data);
	return (<li>{header}{data}</li>);
    } else {
	return null;
    }
}

function CycleDisplay(props) {
    var i = props.element;
    console.log('cycle-display', i);
    return (<ul><li>{i[0].join("->")}</li>
	    <CycleLine header='Arb: ' data={i[1]}/>
	    <CycleLine header='Delay: ' data={i[2]}/>
	    <CycleLine header='Limit: ' data={i[3]}/></ul>);
}

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
	    file_upload: [],
	    result: '',
	    image_src: blank }
    }
    handleFormSubmit(e) {
	this.handleSubmit(e, {
	    method: 'POST',
	    headers: {
		'Content-Type': 'application/json'
	    },
	    body: JSON.stringify({
		data : this.state.description
	    })
	});
    }
    handleFileSubmit(e) {
	var data = new FormData();
	for(var file of this.state.file_upload) {
	    data.append('file[]', file);
	};
	this.handleSubmit(e, {
	    method: 'POST',
	    body: data
	});
    }
    handleSubmit(e, data) {
	console.log("hello!!!");
	e.preventDefault();
	var me = this;
	fetch('/cycle', data).then(function(response) {
	    return response.json();
	}).then(function(json) {
	    console.log("return!!!", json);
	    me.setState({result: json.result});
	}).catch(function(ex) {
	    console.log('parsing failed', ex);
	    me.setState({result: "Error"});
	});
	fetch('/cycle-viz', data).then(function(response) {
	    return response.blob();
	}).then(function(blob) {
	    var objectURL = URL.createObjectURL(blob);
	    me.setState({image_src: objectURL});
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
	var result = this.state.result;

	if( Object.prototype.toString.call( result ) === '[object Array]' ) {
	    result.sort((a,b) => {return b[1] - a[1]});
	    var elems = result.map((i) => {
		console.log('proto', i);
		return (<CycleDisplay element={i} />);
	    });
	    console.log(elems);
	    return (<div>{elems}</div>);
	}
	return "";
    }

    render() {
	return (
		<div className="App">
		<div className="App-header">
		<h2>Welcome to the cycle detector</h2>
		</div>
		<Form inline onSubmit={this.handleFileSubmit}>
		<FormGroup controlId="formControlsFile">
		<ControlLabel>File upload (multiple files allowed)</ControlLabel>
		<FormControl type="file" multiple
	    onChange={this.handleFileChange} />
	        </FormGroup>
		<Button type="submit">Calculate</Button>
		</Form>
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
		<p>
		{this.formatResults()}
	    </p>
		<img src={this.state.image_src}/>
		</div>
    );
  }
}

export default App;
