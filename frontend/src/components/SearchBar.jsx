import React, { useState } from "react";
import "./styles/SearchBar.css";

const SearchBar = ({ onSearch }) => {
    const [searchTerm, setSearchTerm] = useState("");
    const [sortOption, setSortOption] = useState("");

    const handleSearch = () => {
        onSearch({ searchTerm, sortOption });
    };

    return (
        <div className="search-bar-container">
            <input
                type="text"
                className="search-input"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search by title or description..."
            />
            <button className="search-button" onClick={handleSearch}>
                🔍
            </button>
            <select
                className="sort-dropdown"
                value={sortOption}
                onChange={(e) => setSortOption(e.target.value)}
            >
                <option value="">Sort by...</option>
                <option value="price">Price: Low to High</option>
                <option value="-price">Price: High to Low</option>
                <option value="title">Title: A to Z</option>
                <option value="-title">Title: Z to A</option>
                <option value="-likes">Likes: High to Low</option>
                <option value="dislikes">Dislikes: Low to High</option>
                <option value="-created_at">Creation Date: Newest to Oldest</option>
                <option value="created_at">Creation Date: Oldest to Newest</option>
            </select>
        </div>
    );
};

export default SearchBar;
