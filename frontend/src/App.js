// frontend/src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SimpleChatbot from './components/SimpleChatbot';

function App() {
  return (
    <Router>
      <Routes>
      <Route exact path="/" element={<SimpleChatbot />} />
        {/* ... define other routes */}
      </Routes>
    </Router>
  );
}

export default App;