import NavBar from "../components/Navbar.jsx";
import MessagesFeed from "../components/MessagesFeed.jsx";
import api from "../api";
import React, { useState, useEffect } from "react";

function Messages() {
    const [loading, setLoading] = useState(false);
    const [messages, setMessages] = useState([]);
    const [isInboxExpanded, setIsInboxExpanded] = useState(false); 
    const [formData, setFormData] = useState({ recipient: "", content: "" }); 

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

    const handleFormChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleFormSubmit = (e) => {
        e.preventDefault();
        console.log("Form submitted:", formData);
        
        setFormData({ recipient: "", content: "" }); 
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

                {/* Message Form */}
                <div className="message-form">
                    <h2>Send a Message</h2>
                    <form onSubmit={handleFormSubmit}>
                        <div style={{ marginBottom: "10px" }}>
                            <label htmlFor="recipient" style={{ display: "block", marginBottom: "5px" }}>
                                Recipient:
                            </label>
                            <input
                                type="text"
                                id="recipient"
                                name="recipient"
                                value={formData.recipient}
                                onChange={handleFormChange}
                                style={{ width: "100%", padding: "8px" }}
                                required
                            />
                        </div>
                        <div style={{ marginBottom: "10px" }}>
                            <label htmlFor="content" style={{ display: "block", marginBottom: "5px" }}>
                                Message Content:
                            </label>
                            <textarea
                                id="content"
                                name="content"
                                value={formData.content}
                                onChange={handleFormChange}
                                style={{ width: "100%", padding: "8px" }}
                                rows="5"
                                required
                            ></textarea>
                        </div>
                        <button
                            type="submit"
                        >
                            Send Message
                        </button>
                    </form>
                </div>
            </div>
        </>
    );
}

export default Messages;
