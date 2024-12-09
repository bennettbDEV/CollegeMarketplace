import { useNavigate } from "react-router-dom"; 
import NavBar from "../components/Navbar.jsx";
import { useState, useEffect } from "react";
import { jwtDecode } from "jwt-decode";
import { ACCESS_TOKEN } from "../constants";

function Messages() {
    const [messages, setMessages] = useState([]);
    const [userId, setUserId] = useState(null);

    const navigate = useNavigate(); 

    return(
        <div>
        <NavBar />
            <div>
                <h1>Messages</h1>

            </div>
        </div>
    );
}

export default Messages

