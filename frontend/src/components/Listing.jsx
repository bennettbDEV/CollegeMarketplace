import React, { useState } from "react";
import api from "../api";
import "./styles/Listing.css";


function Listing({ listing }) {
    const [imageError, setImageError] = useState(false);  // Track if the image fails to load
    const formattedDate = new Date(listing.created_at).toLocaleDateString("en-US");

    // Image URL
    const imageUrl = listing.image ? `${api.defaults.baseURL}${listing.image}` : null;
    const fallbackImage = "/default-image.jpg";  // Fallback image URL

    const handleImageError = () => {
        setImageError(true);
    };

    return (
        <div className="listing-container">
            <h2 className="listing-title">{listing.title}</h2>
            <p className="listing-condition">Condition: {listing.condition}</p>
            <p className="listing-description">Desc: {listing.description}</p>
            <p className="listing-price">Price: ${listing.price}</p>

            <div className="listing-image">
                {imageUrl && !imageError ? (
                    <img
                        src={imageUrl}
                        alt={listing.title}
                        className="listing-image-file"
                        style={{ width: "200px", height: "auto" }}
                        onError={handleImageError}  // Trigger fallback on error
                    />
                ) : (
                    <img
                        src={fallbackImage}  // Fallback image
                        alt="Fallback"
                        className="listing-image-file"
                        style={{ width: "200px", height: "auto" }}
                    />
                )}
            </div>
            <p className="listing-date">Posted on: {formattedDate}</p>
            <div className="listing-tags">
                <strong>Tags: </strong>
                {listing.tags.map((tag, index) => (
                    <span key={index} className="listing-tag">{tag} </span>
                ))}
            </div>
        </div>
    );
    //For image: {listing.image && <img src={listing.image} alt={listing.title} className="listing-image" />}
}
/*
<button className="delete-button" onClick={() => onDelete(listing.id)}>
                Delete
            </button>
*/
export default Listing
