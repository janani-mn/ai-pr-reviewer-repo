import React, { useState, useEffect } from 'react';

// Sample React component with intentional issues for demo
const ProblematicComponent = () => {
  const [data, setData] = useState('');
  const [userInput, setUserInput] = useState('');
  
  // Issue: Missing dependency array
  useEffect(() => {
    console.log('Effect running');
  });

  // Issue: Potential XSS vulnerability
  const handleUnsafeRender = (input) => {
    document.getElementById('output').innerHTML = input;
  };

  // Issue: Hardcoded API key (security issue)
  const API_KEY = 'sk-1234567890abcdef';   

  // Issue: eval usage (dangerous)
  const handleDynamicCode = (code) => {
    eval(code);
  };

  return (
    <div>
      <h1>Demo Component</h1>
      <input 
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}   
        placeholder="Enter some text"
      />
      
      {/* Issue: dangerouslySetInnerHTML without sanitization */}
      <div dangerouslySetInnerHTML={{ __html: userInput }} />
      
      <div id="output"></div>
      
      <button onClick={() => handleUnsafeRender(userInput)}>
        Unsafe Render
      </button>
      
      <button onClick={() => handleDynamicCode(userInput)}>
        Execute Code
      </button>
    </div>
  );
};

export default ProblematicComponent;
