import React from 'react';

// This component intentionally contains several common React errors for testing PR review
function ErrorDemoComponent(props) {
  // Error: Unused variable
  const unused = 123;

  // Error: Typo in props (should be props.title)
  const heading = props.titel;

  // Error: JSX not wrapped in a single parent element
  <h1>{heading}</h1>
  <p>This is a demo component with errors.</p>

  // Error: Missing return statement
}

// Error: Missing propTypes validation

export default ErrorDemoComponent;
