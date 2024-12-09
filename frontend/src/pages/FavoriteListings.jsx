import React, { useState, useEffect } from "react";
import NavBar from "../components/Navbar";
import api from "../api";
import ListingFeed from "../components/ListingFeed";
import "./styles/FavoriteListings.css";

function SavedListings() {
    const [listings, setListings] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        fetchFavoriteListings();
    }, []);

    const fetchFavoriteListings = async () => {
        setLoading(true);
        try {
            const response = await api.get("/api/listings/list_favorite_listings/");
            setListings(response.data.favorites || []);
        } catch (err) {
            console.error("Error fetching favorite listings:", err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="saved-listings-container">
            <NavBar />
            <h1>Your Saved Listings</h1>
            {loading ? (
                <p>Loading...</p>
            ) : listings.length === 0 ? (
                <div className="empty-listings-message">
                    <p>You don't have any saved listings yet.</p>
                    <p>Browse the marketplace to save your favorite items!</p>
                </div>
            ) : (
                <ListingFeed listings={listings} />
            )}
        </div>
    );
}

export default SavedListings;
