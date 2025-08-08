import React from 'react';

// This component is intentionally broken for error reporting demonstration
function BrokenSample(props) {
  // Error: Unused variable
  const unusedValue = 'not used';

  // Error: Typo in variable name
  let message = 'Hello, ' + props.nam;

  // Error: JSX not wrapped in a single parent element
  <h2>Welcome!</h2>
  <span>This is a broken sample component.</span>

  // Error: Missing return statement
}

export default BrokenSample;
