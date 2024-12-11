import React from "react";
import "./styles/LinkedButton.css";

function PaginationButton({ url, onClick, label }) {
    const handleClick = () => {
        if (url) {
            onClick(url);
        }
    };

    return (
        <button
            className={`pagination-button ${url ? "enabled" : "disabled"}`}
            onClick={handleClick}
            disabled={!url}
        >
            {label}
        </button>
    );
}

export default PaginationButton;
