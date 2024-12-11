import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useUser } from '../contexts/UserContext.jsx';
import NavBar from "../components/Navbar.jsx";
import UserFeed from "../components/UserFeed";
import api from "../api";
import { retryWithExponentialBackoff } from "../utils/retryWithExponentialBackoff";
import "./styles/Settings.css";

function Settings() {
    const { userData, isLoading } = useUser();
    const navigate = useNavigate();
    const [blockedUsers, setBlocked] = useState([]);
    const [loading, setLoading] = useState(false);
    const userId = userData? userData.id : -1;

    useEffect(() => {
            fetchBlockedUsers();
        }, []);

    const handleLogout = () => {
        localStorage.clear()
        navigate("/login", { replace: true });
    };

    // Function: Fetch all blocked users
    const fetchBlockedUsers = async () => {
        setLoading(true);
        try {
            const response = await retryWithExponentialBackoff(() =>
                api.get("/api/users/list_blocked_users/"));
            setBlocked(response.data.blocked || []);
        } catch (err) {
            console.error("Error fetching blocked users:", err);
        } finally {
            setLoading(false);
        }
    };

    // Function: Remove a user from blockedUsers
    const handleUnblock = async (userId) => {
        try {
            // Send a DELETE request to the backend
            await api.delete(`/api/users/${userId}/unblock_user/`);
            // Update the UI by filtering out the unblocked user
            setBlocked((prevBlocked) =>
                prevBlocked.filter((user) => user.id !== userId)
            );
        } catch (err) {
            console.error("Error unblocking user:", err);
        }
    };

    const handleDeleteAccount = async () => {
        const confirmDelete = window.confirm(
            "Are you sure you want to delete your account? This action cannot be undone."
        );
        if (confirmDelete) {
            try {
                //await api.delete("/api/users/");
                localStorage.clear();
                navigate("/login", { replace: true });
            } catch (err) {
                console.error("Error deleting account:", err);
                alert("An error occurred while trying to delete your account. Please try again.");
            }
        }
    };


    return (
        <>
            <NavBar />
            <div className="container">
                <h2>Settings</h2>
                <button className="logout-button" onClick={handleLogout}>Logout</button>
                <br></br>
                <h3>Blocked users:</h3>
                <UserFeed users={blockedUsers} onUnblock={handleUnblock} />
                <button>Reset Password</button>
                <br></br>
                <br></br>
                <button className="delete-account-button"
                    onClick={handleDeleteAccount}>Delete Account</button>
            </div>

        </>
    );
}

export default Settings;
