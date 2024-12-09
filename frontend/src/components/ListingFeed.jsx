// ListingFeed.jsx
import React from 'react';
import Listing from "./Listing";
import { Link } from "react-router-dom";
import "./styles/ListingFeed.css";

// A function that returns a listing feed
function ListingFeed({ listings, onSaveListing }) {
  if (!Array.isArray(listings)) {
    console.error("listings is not an array:", listings);
    listings = [];
    return <div>No listings available</div>; // TODO: Add loading circle or placeholder
  }

  return (
    <div className="listing-feed">
      {listings.map((listing, index) => (
        <div key={index} className="listing-wrapper">
          <Link to={`/listings/${listing.id}`}>
            <Listing listing={listing} />
          </Link>
          <button
            className="save-button"
            onClick={(e) => {
              e.preventDefault(); // Prevent navigation when clicking the Save button
              onSaveListing(listing.id);
            }}
          >
            Save
          </button>
        </div>
      ))}
    </div>
  );
}

export default ListingFeed;

