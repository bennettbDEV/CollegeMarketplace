import React from 'react';
import Message from "./Message";
import { Link } from "react-router-dom";
import "./styles/ListingFeed.css"; 

function MessagesFeed({ messages }) {
  if (!Array.isArray(messages)) {
    console.error("messages is not an array:", messages);
    messages = [];
    return <div>No messages available</div>;
  }

  return (
    <div className="messages-feed">
      {messages.map((message, index) => ( 
          <Message key={index} message={message} /> 
      ))}
    </div>
  );
}

export default MessagesFeed;
