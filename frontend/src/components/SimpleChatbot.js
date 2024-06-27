// frontend/src/components/SimpleChatbot.js
import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { FaPaperPlane, FaTrash, FaQuestionCircle, FaTimes, FaFileUpload } from 'react-icons/fa';
import '../assets/css/SimpleChatbot.css';

const CHAT_HISTORY_KEY = 'chatHistory';

function useChatHistory() {
  const [chatHistory, setChatHistory] = useState(() => {
    const storedHistory = localStorage.getItem(CHAT_HISTORY_KEY);
    return storedHistory ? JSON.parse(storedHistory) : [];
  });

  useEffect(() => {
    const handleStorageChange = (e) => {
      if (e.key === CHAT_HISTORY_KEY && e.oldValue !== e.newValue) {
        setChatHistory(JSON.parse(e.newValue));
      }
    };
    window.addEventListener('storage', handleStorageChange);
    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);

  useEffect(() => {
    localStorage.setItem(CHAT_HISTORY_KEY, JSON.stringify(chatHistory));
  }, [chatHistory]);

  return [chatHistory, setChatHistory];
}

function ChatbotHeader({ onClearChat, onToggleChatbot }) {
  return (
    <div className="chatbot-header bg-blue-500 text-white px-4 py-2 flex items-center justify-between">
      <h2 className="text-xl font-semibold">Simple Chatbot</h2>
      <div className="flex items-center space-x-2">
        <button
          className="flex items-center space-x-2 bg-red-500 text-white py-1 px-2 rounded-lg shadow-md hover:bg-red-600 transition duration-300"
          onClick={onClearChat}
        >
          <FaTrash className="w-4 h-4" />
          <span>Clear Chat</span>
        </button>
        <button
          className="text-white hover:text-gray-200 transition duration-300"
          onClick={onToggleChatbot}
        >
          <FaTimes className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}

function ChatMessage({ message }) {
  return (
    <div className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`p-4 rounded-lg shadow ${
          message.isUser ? 'bg-blue-500 text-white' : 'bg-white text-gray-800'
        }`}
      >
        {message.content}
      </div>
    </div>
  );
}

function LoadingIndicator() {
  return (
    <div className="flex justify-start">
      <div className="p-4 rounded-lg shadow bg-white text-gray-800">
        <div className="flex items-center">
          <div className="w-2 h-2 bg-gray-400 rounded-full mr-1 animate-pulse"></div>
          <div className="w-2 h-2 bg-gray-400 rounded-full mr-1 animate-pulse animation-delay-75"></div>
          <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse animation-delay-150"></div>
        </div>
      </div>
    </div>
  );
}

function SimpleChatbot() {
  const [chatHistory, setChatHistory] = useChatHistory();
  const [userQuery, setUserQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showAlert, setShowAlert] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const chatHistoryRef = useRef(null);

  useEffect(() => {
    if (chatHistoryRef.current) {
      chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
    }
  }, [chatHistory]);

  const handleUserInput = async (e) => {
    e.preventDefault();
    if (userQuery.trim() === '') return;

    const newMessage = { content: userQuery, isUser: true };
    setChatHistory((prevHistory) => [...prevHistory, newMessage]);
    setUserQuery('');

    setTimeout(() => {
      if (chatHistoryRef.current) {
        chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
      }
    }, 0);

    setIsLoading(true);

    try {
      const response = await axios.post('http://localhost:5200/api/chatbot', { userInput: userQuery });
      const botResponse = { content: response.data.response, isUser: false };
      setChatHistory((prevHistory) => [...prevHistory, botResponse]);
    } catch (error) {
      console.error('Error sending user query:', error);
      const errorMessage = { content: 'Sorry, something went wrong. Please try again later.', isUser: false };
      setChatHistory((prevHistory) => [...prevHistory, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleUserInput(e);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setIsLoading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:5200/api/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      const botResponse = { content: response.data.response, isUser: false };
      setChatHistory((prevHistory) => [...prevHistory, botResponse]);
    } catch (error) {
      console.error('Error uploading file:', error);
      const errorMessage = { content: 'Sorry, something went wrong with the file upload. Please try again later.', isUser: false };
      setChatHistory((prevHistory) => [...prevHistory, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearChat = () => setShowAlert(true);
  const confirmClearChat = () => {
    setChatHistory([]);
    setShowAlert(false);
  };
  const cancelClearChat = () => setShowAlert(false);
  const handleToggleChatbot = () => setIsOpen(!isOpen);

  return (
    <div className={`chatbot-container ${isOpen ? 'open' : ''}`}>
      {!isOpen && (
        <div className="chatbot-bubble" onClick={handleToggleChatbot}>
          <FaQuestionCircle className="w-8 h-8 text-blue-500" />
        </div>
      )}
      {isOpen && (
        <div className="chatbot-content">
          <ChatbotHeader onClearChat={handleClearChat} onToggleChatbot={handleToggleChatbot} />
          <div className="chatbot-history flex-1 overflow-y-auto pb-4" ref={chatHistoryRef}>
            <div className="flex flex-col space-y-4 p-4">
              {chatHistory.map((message, index) => (
                <ChatMessage key={index} message={message} />
              ))}
              {isLoading && <LoadingIndicator />}
            </div>
          </div>
          <form onSubmit={handleUserInput} className="flex items-center bg-white rounded-lg shadow-md p-2 mt-4">
            <textarea
              value={userQuery}
              onChange={(e) => setUserQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              className="flex-1 px-4 py-3 rounded-lg focus:outline-none bg-transparent resize-none overflow-auto"
              rows={1}
            ></textarea>
            <button
              type="submit"
              disabled={isLoading}
              className={`ml-4 text-blue-500 px-4 py-3 rounded-lg transition duration-300 ${
                isLoading ? 'opacity-50 cursor-not-allowed' : 'hover:text-blue-600'
              }`}
            >
              <FaPaperPlane className="w-4 h-4" />
            </button>
            <input type="file" id="fileUpload" className="hidden" onChange={handleFileUpload} />
            <label htmlFor="fileUpload" className="ml-4 text-blue-500 px-4 py-3 rounded-lg cursor-pointer hover:text-blue-600 transition duration-300">
              <FaFileUpload className="w-4 h-4" />
            </label>
          </form>
          {showAlert && (
            <div className="clear-chat-popup fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
              <div className="bg-white p-8 rounded-lg shadow-lg">
                <h3 className="text-xl font-bold mb-4">Confirm Clear Chat</h3>
                <p className="mb-6">Are you sure you want to clear the chat history?</p>
                <div className="flex justify-end space-x-4">
                  <button className="bg-gray-500 text-white py-2 px-4 rounded-lg hover:bg-gray-600 transition duration-300" onClick={cancelClearChat}>
                    Cancel
                  </button>
                  <button className="bg-red-500 text-white py-2 px-4 rounded-lg hover:bg-red-600 transition duration-300" onClick={confirmClearChat}>
                    Clear
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default SimpleChatbot;

