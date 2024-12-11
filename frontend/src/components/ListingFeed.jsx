// ListingFeed.jsx
import React from 'react';
import Listing from "./Listing";
import "./styles/ListingFeed.css";

// A function that returns a listing feed
function ListingFeed({ listings, actionType, onAction }) {
  if (!Array.isArray(listings)) {
    console.error("listings is not an array:", listings);
    listings = [];
    return <div>No listings available</div>; // TODO: Add loading circle or placeholder
  }

  return (
    <div className="listing-feed">
      {listings.map((listing, index) => (

        <Listing key={index}
          listing={listing}
          additionalAction={
            actionType === "save" ? (
              <button
                className="save-button"
                onClick={(e) => {
                  e.preventDefault();
                  onAction(listing.id);
                }}
              >
                Save
              </button>
            ) : actionType === "remove" ? (
              <button
                className="remove-favorite-button"
                onClick={(e) => {
                  e.preventDefault();
                  onAction(listing.id);
                }}
              >
                &times;
              </button>
            ) : null
          }
        />
      ))}
    </div>
  );
}

export default ListingFeed;