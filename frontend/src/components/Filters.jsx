import React, { useState } from "react";
import "./styles/Filters.css";

const Filters = ({ onFilterChange }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [condition, setCondition] = useState("");

  const handleFilterChange = () => {
    // Send the filter data back to the parent component
    onFilterChange({
      searchTerm,
      minPrice,
      maxPrice,
      condition,
    });
  };

  return (
    <div className="filters-container">
      <h3>Filter Listings</h3>
      <div className="filter-group">
        <label htmlFor="searchTerm">Search:</label>
        <input
          type="text"
          id="searchTerm"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Search by title or description"
        />
      </div>

      <div className="filter-group">
        <label htmlFor="minPrice">Min Price:</label>
        <input
          type="number"
          id="minPrice"
          value={minPrice}
          onChange={(e) => setMinPrice(e.target.value)}
          placeholder="0"
        />
      </div>

      <div className="filter-group">
        <label htmlFor="maxPrice">Max Price:</label>
        <input
          type="number"
          id="maxPrice"
          value={maxPrice}
          onChange={(e) => setMaxPrice(e.target.value)}
          placeholder="1000"
        />
      </div>

      <div className="filter-group">
        <label htmlFor="condition">Condition:</label>
        <select
          id="condition"
          value={condition}
          onChange={(e) => setCondition(e.target.value)}
        >
          <option value="">All</option>
          <option value="Factory New">Factory New</option>
          <option value="Minimal Wear">Minimal Wear</option>
          <option value="Fair">Fair</option>
          <option value="Well Worn">Well Worn</option>
          <option value="Refurbished">Refurbished</option>
        </select>
      </div>

      <button className="apply-filters" onClick={handleFilterChange}>
        Apply Filters
      </button>
    </div>
  );
};

export default Filters;