// frontend/src/components/InteractiveMode.js
import React from 'react';
import { FaTimes } from 'react-icons/fa';

function InteractiveMode({ onToggle }) {
  return (
    <div className="chatbot-content">
      <div className="chatbot-header bg-blue-500 text-white px-4 py-2 flex items-center justify-between">
        <h2 className="text-xl font-semibold">3D Interactive Mode</h2>
        <button
          className="text-white hover:text-gray-200 transition duration-300"
          onClick={onToggle}
        >
          <FaTimes className="w-4 h-4" />
        </button>
      </div>
      <div className="flex-1 bg-white"></div>
    </div>
  );
}

export default InteractiveMode;