import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; 
import NavBar from "../components/Navbar.jsx";
import "./styles/Settings.css";

function Settings() {
    const navigate = useNavigate(); 
    const handleLogout = () => {
        localStorage.clear()
        navigate("/login", { replace: true });
    };

    return (
        <>
            <NavBar />
            <div className="container">
                <h2>Settings</h2>
                <button onClick={handleLogout}>Logout</button>
                        <br></br>
                <button >Reset Password</button>
                        <br></br>
                        <button className="delete-account-button">Delete Account</button>
            </div>
            
        </>
    );
}

export default Settings;
