import React from "react";

function Listing({listing}) {
    const formattedDate = new Date(listing.created_at).toLocaleDateString("en-US")

    return (
        <div className="listing-container">
            <h2 className="listing-title">{listing.title}</h2>
            <p className="listing-condition">Condition: {listing.condition}</p>
            <p className="listing-description">Desc: {listing.description}</p>
            <p className="listing-price">Price: ${listing.price}</p>
            <p className="listing-image">TempImageTxt: {listing.image}</p>
            <p className="listing-date">Posted on: {formattedDate}</p>
            <div className="listing-tags">
                <strong>Tags: </strong>
                {listing.tags.map((tag, index) => (
                    <span key={index} className="listing-tag">{tag} </span>
                ))}
            </div>
            <p className="listing-author">Author ID: {listing.author_id}</p>
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
