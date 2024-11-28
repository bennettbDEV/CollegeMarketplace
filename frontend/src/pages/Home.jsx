import { useState, useEffect } from "react";
import api from "../api";
import ListingFeed from "../components/ListingFeed";
import NavBar from "../components/Navbar.jsx";
import Filters from "../components/Filters.jsx";
import LinkedButton from "../components/LinkedButton.jsx";
import "./styles/Home.css";

function Home() {
  const [listings, setListings] = useState([]);
  const [nextPage, setNextPage] = useState(null);
  const [previousPage, setPreviousPage] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getListings("/api/listings/");
  }, []);

  const getListings = (url) => {
    setLoading(true);
    api
      .get(url)
      .then((response) => response.data)
      .then((data) => {
        console.log("API Response:", data);
        setListings(data.results);
        setNextPage(data.links.next);
        setPreviousPage(data.links.previous);
      })
      .catch((err) => {
        console.error("Error fetching listings:", err);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <div>
      <NavBar />
      <div className="home-container">
        <div className="filters-section">
          <Filters />
        </div>

        <div className="listings-section">
          <h1>Listings</h1>

          {loading ? (
            <p>Loading...</p>
          ) : (
            <>
              <ListingFeed listings={listings} />

              <div className="pagination-controls">
                <LinkedButton
                  url={previousPage}
                  onClick={getListings}
                  label="Previous"
                />
                
                <LinkedButton
                  url={nextPage}
                  onClick={getListings}
                  label="Next"
                />
              </div>

            </>
          )}
        </div>

      </div>
    </div>
  );
}

export default Home;
