// ListingFeed.jsx
import React from "react";
import Listing from "./Listing";
import { Link } from "react-router-dom";
import "./styles/ListingFeed.css";

// A component to display a feed of listings
function ListingFeed({ listings, onSaveListing }) {
  // Handle the case where listings are not an array
  if (!Array.isArray(listings)) {
    console.error("listings is not an array:", listings);
    listings = [];
    return <div>No listings available</div>; // Placeholder message
  }

  return (
    <div className="listing-feed">
      {listings.map((listing, index) => (
        <div key={index} className="listing-wrapper">
          {/* Wrap the listing with a link to its detail page */}
          <Link to={`/listings/${listing.id}`}>
            <Listing listing={listing} />
          </Link>

          {/* Add the Save button */}
          <button
            className="save-button"
            onClick={(e) => {
              e.preventDefault(); // Prevent the navigation when clicking the Save button
              onSaveListing(listing.id); // Call the save handler passed as a prop
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

