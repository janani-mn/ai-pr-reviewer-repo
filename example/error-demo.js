// Sample JS file with various errors for PR review testing

function buggyFunction(a, b) {
  // Error: Unused variable
  let unusedVar = 42;

  // Error: Undefined variable
  let result = a + b + notDefined;

  // Error: Shadowed variable
  let a = 10;

  // Error: Direct mutation of function parameter
  b++;

  // Error: Console statement in production code
  console.log('Debug info:', a, b);

  // Error: Missing semicolon
  return result
}

// Error: Incorrect import/export syntax
require('fs');

// Error: Function declared but never used
function neverUsed() {
  return 'I am never called';
}
