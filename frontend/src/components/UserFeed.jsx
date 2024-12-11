// UserFeed.jsx
import React from "react";
import User from "./User";
import "./styles/UserFeed.css";

function UserFeed({ users, onUnblock }) {
    if (!Array.isArray(users) || users.length === 0) {
        return <div>No blocked users available.</div>;
    }

    return (
        <div className="user-feed">
            {users.map((user, index) => (
                <div key={index} className="user-item">
                    <User user={user} onUnblock={onUnblock} />
                </div>
            ))}
        </div>
    );
}

export default UserFeed;
