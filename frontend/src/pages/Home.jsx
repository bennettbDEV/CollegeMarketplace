import { useState, useEffect } from "react";
import api from "../api";
import ListingFeed from "../components/ListingFeed";
import NavBar from '../components/Navbar.jsx';
import Filters from '../components/Filters.jsx';
import './styles/Home.css';

function Home() {
    const [listings, setListings] = useState([]);

    useEffect(() => {
        getListings();
    }, []);

    const getListings = () => {
        api
            .get("/api/listings/")
            .then((response) => response.data)
            .then((data) => {
                console.log("API Response:", data);
                setListings(data);
            })
            .catch((err) => {
                console.error("Error fetching listings:", err);
                //alert("Error: " + (err.response ? err.response.data : err.message));
            });
    };
    /*
.then((data) => {
    setListings(data);
    console.log(data);
    })
    .catch((err) => alert(err));
  */
    return (
        <div>
      <NavBar />
      <div className="home-container">
        <div className="filters-section">
          <Filters />
        </div>
        <div className="listings-section">
          <h1>Listings</h1>
          <ListingFeed listings={listings} />
        </div>
      </div>
    </div>
    );
}

export default Home;
