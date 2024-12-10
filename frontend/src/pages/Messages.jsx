import NavBar from "../components/Navbar.jsx";
import MessagesFeed from "../components/MessagesFeed.jsx";
import api from "../api";
import React, { useState, useEffect } from "react";

function Messages() {
    const [loading, setLoading] = useState(false);
    const [messages, setMessages] = useState([]);
    const [isInboxExpanded, setIsInboxExpanded] = useState(false); 

    useEffect(() => {
        fetchMessages();
    }, []);

    const fetchMessages = async () => {
        setLoading(true);
        try {
            const response = await api.get("/api/messages/");
            setMessages(response.data || []);
        } catch (err) {
            console.error("Error fetching messages:", err);
        } finally {
            setLoading(false);
        }
    };

    const toggleInbox = () => {
        setIsInboxExpanded((prev) => !prev);
    };

    return (
        <>
            <NavBar />
            <div className="container">
                <h1>Messages</h1>
                <h2>
                    Inbox:
                    <button 
                        onClick={toggleInbox} 
                        style={{
                            marginLeft: "10px",
                            padding: "5px 10px",
                            cursor: "pointer",
                        }}
                    >
                        {isInboxExpanded ? "Collapse" : "Expand"}
                    </button>
                </h2>
                {isInboxExpanded && (
                    loading ? (
                        <p>Loading...</p>
                    ) : (
                        <MessagesFeed messages={messages} />
                    )
                )}
            </div>
        </>
    );
}

export default Messages;
