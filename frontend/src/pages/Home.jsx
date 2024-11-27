import { useState, useEffect } from "react";
import api from "../api";
import ListingFeed from "../components/ListingFeed";

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
            <div>
                <h1>Listings</h1>
                <ListingFeed listings={listings} />
            </div>
        </div>
    );
}

export default Home;
