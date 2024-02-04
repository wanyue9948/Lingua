// C:\Users\wanyu\translation-app;
import './App.css';
import React, { useState } from 'react';

function App() {
  const [text, setText] = useState(''); // State to hold input text
  const [translatedText, setTranslatedText] = useState(''); // State to hold translated text
  const [sourceLang, setSourceLang] = useState('en'); // State to hold source language
  const [targetLang, setTargetLang] = useState('cn'); // State to hold target language
  const [to_explain, setto_explain] = useState(''); // State to hold the explanation
  const [explanation, setExplanation] = useState(''); // State to hold the explanation


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
 
  const handleExplain = () => {
    // Define the data you'll send
    const dataToSend = {
      text: text, // text from state
      targetLang: targetLang // target language from state
    };
    
    // Send the data to your backend
    fetch('http://localhost:5000/explain', { // Use your backend's URL
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(dataToSend),
    })
    .then(response => response.json())
    .then(data => {
      setExplanation(
        data["explanation"]
      ); // Update state with the translated text
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  };

// Function to handle speech synthesis
const handleSpeak = () => {
  fetch('http://localhost:5000/speak', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      text: translatedText,
      language: targetLang // Use the target language code here
    }),
  })
  .then(response => response.json())
  .then(data => {
    // Handle the response for audio playback here
    // Depending on the backend implementation, this might involve playing an audio file or stream
  })
  .catch((error) => {
    console.error('Error during speech synthesis:', error);
  });
};
  return (
    <div className="App">
      <header className="App-header">
        <h1>Lingua Translation</h1>
        
        <div className="content">
          <div className="translation-section">
          <div className="language-selectors">
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
            className="input-box" 
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Type text to translate here..."
          />
          <button className="translate-button" onClick={handleTranslate}>Translate</button>
          <p>Translation:</p>
          <div className="result-box">{translatedText}</div>
          <button className="translate-button" onClick={handleSpeak}>Speak</button>
          </div>
          <div className="grammar-section">
            <div className="language-selectors">
              <select value={targetLang} onChange={(e) => setTargetLang(e.target.value)}>
                {/* Options should reflect available languages */}
                <option value="en">English</option>
                <option value="fr">French</option>
                <option value="es">Spanish</option>
                <option value="fi">Finnish</option>
                <option value="cn">Chinese</option>
                {/* Add more language options here */}
              </select>
              </div>
          <textarea
            className="input-box" 
            value={to_explain}
            onChange={(e) => setto_explain(e.target.value)}
            placeholder="Type text to explain here..."
          />
          <button className="translate-button" onClick={handleExplain}>Explain</button>
          <p>Grammar assistant:</p>
          <div className="result-box2">{explanation}</div>
          </div>
          </div>
        <div className="author">{"yue wan"}</div>
    
      </header>
    </div>
  );
}

export default App;
