import React from 'react';
import Listing from "./Listing";

// A function that returns a listing feed
function ListingFeed({ listings }) {
  if (!Array.isArray(listings) || listings.length === 0) {
    console.error("listings is not an array:", listings);
    listings = [];
    // TODO: Add loading circle or something instead of "no listings available"
    return <div>No listings available</div>;
  }
  return (
    <div className="listing-feed">
      {listings.map((listing, index) => (
        <Listing key={index} listing={listing} />
      ))}
    </div>
  );
}

export default ListingFeed;