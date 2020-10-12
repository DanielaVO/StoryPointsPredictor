import React from "react";
import "./App.css";
import "semantic-ui-css/semantic.min.css";
import { Form } from "react-bootstrap";
import Header from "./components/Header";
import Table from "./components/Table";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Header as="h1"></Header>
        <hr></hr>
      </header>
      <body>
        <Form>
          <Form.Group>
            <Form.File id="dataFile" label="Select a file " />
          </Form.Group>
        </Form>
        <Table className="Table"></Table>
      </body>
    </div>
  );
}

export default App;
