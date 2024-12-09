import React, { useState } from "react";
import api from "../api";
import "./styles/Message.css";
import Messages from "../pages/Messages";


function Message({ message }) {

    return (

        <div className="message-container">
            <h3>From: </h3>
            <p>person</p>
            <h3>Content: </h3>
            <p>Sick, twisted and politically incorrect, the animated series features the adventures of the Griffin family. Endearingly ignorant Peter and stay-at-home wife Lois reside in Quahog, R.I., and have three kids.</p>
        </div>


        
    );
    //For image: {message.image && <img src={message.image} alt={message.title} className="message-image" />}
}
/*
<button className="delete-button" onClick={() => onDelete(message.id)}>
                Delete
            </button>
*/
export default Message
