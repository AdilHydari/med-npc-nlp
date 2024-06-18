// frontend/src/components/SimpleChatbot.js
import React, { useState } from 'react';
import QuestionMarkPopup from './QuestionMarkPopup';
import ChatInterface from './ChatInterface';
import InteractiveMode from './InteractiveMode';
import '../assets/css/SimpleChatbot.css';

function SimpleChatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedMode, setSelectedMode] = useState(null);

  const handleToggleChatbot = () => {
    setIsOpen(!isOpen);
    setSelectedMode(null);
  };

  const handleModeSelect = (mode) => {
    setSelectedMode(mode);
    setIsOpen(false);
  };

  return (
    <div className={`chatbot-container ${isOpen ? 'open' : ''}`}>
      {!selectedMode && (
        <QuestionMarkPopup
          isOpen={isOpen}
          onToggle={handleToggleChatbot}
          onModeSelect={handleModeSelect}
        />
      )}
      {selectedMode === 'chat' && (
        <ChatInterface onToggle={() => setSelectedMode(null)} />
      )}
      {selectedMode === '3d' && (
        <InteractiveMode onToggle={() => setSelectedMode(null)} />
      )}
    </div>
  );
}

export default SimpleChatbot;