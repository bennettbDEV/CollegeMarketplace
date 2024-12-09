import React, { useState } from "react";
import NavBar from "../components/Navbar.jsx";
import RegistrationForm from "../components/RegistrationForm";
import "./styles/Settings.css";

function Settings() {

    const handleLogout = () => {
        localStorage.clear()
        //navigate("/login", { replace: true });
        window.location.reload();
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
