// frontend/src/components/QuestionMarkPopup.js
import React from 'react';
import { FaQuestionCircle, FaTimes } from 'react-icons/fa';

function QuestionMarkPopup({ isOpen, onToggle, onModeSelect }) {
  return (
    <>
      {!isOpen && (
        <div className="chatbot-bubble" onClick={onToggle}>
          <FaQuestionCircle className="w-8 h-8 text-blue-500" />
        </div>
      )}
      {isOpen && (
        <div className="chatbot-mode-select">
          <div className="mode-select-header">
            <h2>Select Mode</h2>
            <button className="mode-select-close" onClick={onToggle}>
              <FaTimes />
            </button>
          </div>
          <button className="mode-button" onClick={() => onModeSelect('chat')}>
            Chat Interface
          </button>
          <button className="mode-button" onClick={() => onModeSelect('3d')}>
            3D Interactive Mode
          </button>
        </div>
      )}
    </>
  );
}

export default QuestionMarkPopup;