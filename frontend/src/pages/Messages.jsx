import NavBar from "../components/Navbar.jsx";
import RegistrationForm from "../components/RegistrationForm";
//import "./styles/Register.css";
import MessagesFeed from "../components/MessagesFeed.jsx";
import api from "../api";
import React, { useState, useEffect } from "react";

function Messages() {

    const [loading, setLoading] = useState(false);
    const [messages, setMessages] = useState([]);

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

    const getMessages = (url) => {
        setLoading(true);
        api
            .get(url)
            .then((response) => response.data)
            .then((data) => {
                console.log("API Response:", data);
                setMessages(data.results);
            })
            .catch((err) => {
                console.error("Error fetching listings:", err);
            })
            .finally(() => {
                setLoading(false);
            });
    };

    return (
        <>
            <NavBar />
            <div className="container">
                <h1>Messages</h1>
               <h2>Inbox:</h2>
               {loading ? (
                    <p>Loading...</p>
                ) : (
                    <>
                        <MessagesFeed messages={messages} />

                       
                    </>
                )}
            </div>
            
        </>
    );
}

export default Messages;
