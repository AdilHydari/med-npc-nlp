import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { FaPaperPlane, FaTrash } from 'react-icons/fa';

function SimpleChatbot() {
  const [chatHistory, setChatHistory] = useState(() => {
    const storedHistory = localStorage.getItem('chatHistory');
    return storedHistory ? JSON.parse(storedHistory) : [];
  });
  const [userQuery, setUserQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showAlert, setShowAlert] = useState(false);
  const chatHistoryRef = useRef(null);

  useEffect(() => {
    const handleStorageChange = (e) => {
      if (e.key === 'chatHistory' && e.oldValue !== e.newValue) {
        setChatHistory(JSON.parse(e.newValue));
      }
    };

    window.addEventListener('storage', handleStorageChange);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);

  useEffect(() => {
    localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
    if (chatHistoryRef.current) {
      chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
    }
  }, [chatHistory]);

  const handleUserInput = async (e) => {
    e.preventDefault();
    if (userQuery.trim() === '') return;

    const newMessage = {
      content: userQuery,
      isUser: true,
    };

    setChatHistory((prevHistory) => [...prevHistory, newMessage]);
    setUserQuery('');

    setTimeout(() => {
      if (chatHistoryRef.current) {
        chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
      }
    }, 0);

    setIsLoading(true);

    try {
      const response = await axios.post(
        'http://localhost:5000/api/chatbot',
        { userInput: userQuery }
      );

      const botResponse = {
        content: response.data.response,
        isUser: false,
      };

      setChatHistory((prevHistory) => [...prevHistory, botResponse]);
    } catch (error) {
      console.error('Error sending user query:', error);
      const errorMessage = {
        content: 'Sorry, something went wrong. Please try again later.',
        isUser: false,
      };
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

  const handleClearChat = () => {
    setShowAlert(true);
  };

  const confirmClearChat = () => {
    setChatHistory([]);
    setShowAlert(false);
  };

  const cancelClearChat = () => {
    setShowAlert(false);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100 p-4">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-semibold">Simple Chatbot</h2>
        <button
          className="flex items-center space-x-2 bg-red-500 text-white py-2 px-4 rounded-lg shadow-md hover:bg-red-600 transition duration-300"
          onClick={handleClearChat}
        >
          <FaTrash className="w-4 h-4" />
          <span>Clear Chat</span>
        </button>
      </div>
      <div className="flex-1 overflow-y-auto pb-4" ref={chatHistoryRef}>
        <div className="flex flex-col space-y-4">
          {chatHistory.map((message, index) => (
            <div key={index} className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}>
              <div
                className={`p-4 rounded-lg shadow ${
                  message.isUser ? 'bg-blue-500 text-white' : 'bg-white text-gray-800'
                }`}
              >
                {message.content}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="p-4 rounded-lg shadow bg-white text-gray-800">
                <div className="flex items-center">
                  <div className="w-2 h-2 bg-gray-400 rounded-full mr-1 animate-pulse"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full mr-1 animate-pulse animation-delay-75"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse animation-delay-150"></div>
                </div>
              </div>
            </div>
          )}
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
      </form>
      {showAlert && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
          <div className="bg-white p-8 rounded-lg shadow-lg">
            <h3 className="text-xl font-bold mb-4">Confirm Clear Chat</h3>
            <p className="mb-6">Are you sure you want to clear the chat history?</p>
            <div className="flex justify-end space-x-4">
              <button
                className="bg-gray-500 text-white py-2 px-4 rounded-lg hover:bg-gray-600 transition duration-300"
                onClick={cancelClearChat}
              >
                Cancel
              </button>
              <button
                className="bg-red-500 text-white py-2 px-4 rounded-lg hover:bg-red-600 transition duration-300"
                onClick={confirmClearChat}
              >
                Clear
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default SimpleChatbot;