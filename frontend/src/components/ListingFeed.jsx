import React from 'react';
import Listing from "./Listing";
import { Link } from "react-router-dom";
import "./styles/ListingFeed.css";

// A function that returns a listing feed
function ListingFeed({ listings }) {
  if (!Array.isArray(listings)) {
    console.error("listings is not an array:", listings);
    listings = [];
    // TODO: Add loading circle or something instead of "no listings available"
    return <div>No listings available</div>;
  }
  return (
    <div className="listing-feed">
      {listings.map((listing, index) => (
        <Link to={`/listings/${listing.id}`}>
          <Listing key={index} listing={listing} />
        </Link>
      ))}
    </div>
  );
}

export default ListingFeed;