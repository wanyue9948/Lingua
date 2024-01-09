// import logo from './logo.svg';
import './App.css';
import React, { useState } from 'react';

function App() {
  const [text, setText] = useState(''); // State to hold input text
  const [translatedText, setTranslatedText] = useState(''); // State to hold translated text
  const [sourceLang, setSourceLang] = useState('en'); // State to hold source language
  const [targetLang, setTargetLang] = useState('cn'); // State to hold target language

  const handleTranslate = () => {
    // Define the data you'll send
    const dataToSend = {
      text: text, // text from state
      targetLang: targetLang // target language from state
    };
    
    // Send the data to your backend
    fetch('http://localhost:5000/translate', { // Use your backend's URL
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(dataToSend),
    })
    .then(response => response.json())
    .then(data => {
      setTranslatedText(
        data["translated_text"]
      ); // Update state with the translated text
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  };
  

  return (
    <div className="App">
      <header className="App-header">
        <h1>Lingua Translation</h1>
        <div>
          <select value={sourceLang} onChange={(e) => setSourceLang(e.target.value)}>
            {/* Options should reflect available languages */}
            <option value="en">English</option>
            <option value="fr">French</option>
            <option value="es">Spanish</option>
            <option value="fi">Finnish</option>
            <option value="cn">Chinese</option>
            {/* Add more language options here */}
          </select>
          <select value={targetLang} onChange={(e) => setTargetLang(e.target.value)}>
            <option value="en">English</option>
            <option value="fr">French</option>
            <option value="es">Spanish</option>
            <option value="fi">Finnish</option>
            <option value="cn">Chinese</option>
            {/* Add more language options here */}
          </select>
        </div>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Type text to translate here..."
        />
        <button onClick={handleTranslate}>Translate</button>
        <p>Translation:</p>
        <div>{translatedText}</div>
      </header>
    </div>
  );
}

export default App;
