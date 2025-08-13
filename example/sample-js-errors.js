// sample-js-errors.js
// This file contains intentional errors for testing ESLint and your PR workflow

function buggyFunction(a, b) {
  // Unused variable
  let unusedVar = 42;

  // Undefined variable
  let result = a + b + notDefined;

  // Shadowed variable
  let a = 10;

  // Direct mutation of function parameter
  b++;

  // Console statement in production code
  console.log('Debug info:', a, b);

  // Missing semicolon
  return result
}

// Incorrect import/export syntax
require('fs');

// Function declared but never used
function neverUsed() {
  return 'I am never called';
}
