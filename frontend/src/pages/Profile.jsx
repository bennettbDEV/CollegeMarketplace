import NavBar from "../components/Navbar.jsx";
import ListingFeed from "../components/ListingFeed";
import { jwtDecode } from "jwt-decode";
import { useState, useEffect } from "react";
import api from "../api";
import LinkedButton from "../components/LinkedButton.jsx";
import "./styles/Profile.css";
import { ACCESS_TOKEN } from "../constants";
import testImg from "../assets/usericon.png";

function Profile() {
    const [listings, setListings] = useState([]);
    const [nextPage, setNextPage] = useState(null);
    const [previousPage, setPreviousPage] = useState(null);
    const [loading, setLoading] = useState(false);
    const [userId, setUserId] = useState(null);
    const [userData, setUserData] = useState(null); 

    useEffect(() => {
        const token = localStorage.getItem(ACCESS_TOKEN);
        if (token) {
            try {
                const decodedToken = jwtDecode(token);
                setUserId(decodedToken.user_id);
            } catch (err) {
                console.error("Error decoding JWT:", err);
            }
        }
    }, []);

    useEffect(() => {
        if (userId) {
            fetchUserData(userId);
            getListings(`/api/listings/?author_id=${userId}`);
        }
    }, [userId]);

    const fetchUserData = (id) => {
        api
            .get(`/api/users/${id}/`)
            .then((response) => response.data)
            .then((data) => {
                console.log("User Data:", data);
                setUserData(data); 
            })
            .catch((err) => {
                console.error("Error fetching user data:", err);
            });
    };

    const getListings = (url) => {
        setLoading(true);
        api
            .get(url)
            .then((response) => response.data)
            .then((data) => {
                console.log("API Response:", data);
                setListings(data.results);
                setNextPage(data.links?.next || null);
                setPreviousPage(data.links?.previous || null);
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
            <div className="profile-container">
                <h1>Profile Page</h1>
                {userData ? (
                    <>
                        <p>Username: {userData.username}</p>
                        <p>Location: {userData.location}</p>
                        <img src={testImg} width="150" alt="Profile" />
                    </>
                ) : (
                    <p>Loading user data...</p>
                )}

                <h2>Your Listings:</h2>
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
    );
}

export default Profile;
