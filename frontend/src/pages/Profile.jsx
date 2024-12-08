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

    const imageUrl = userData?.image ? `${api.defaults.baseURL}${userData.image}` : testImg;

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

    const fetchUserData = async (id, retries = 3, delay = 1000) => {
        for (let attempt = 1; attempt <= retries; attempt++) {
            try {
                const response = await api.get(`/api/users/${id}/`);
                const data = response.data;
                console.log("User Data:", data);
                setUserData(data);
                // Exit the function if the API call succeeds
                return; 
            } catch (err) {
                console.error(`Attempt ${attempt} failed:`, err);

                if (attempt < retries) {
                    console.log(`Retrying in ${delay}ms...`);
                    // Wait before retrying
                    await new Promise((resolve) => setTimeout(resolve, delay)); 
                } else {
                    console.error("All attempts to fetch user data failed.");
                }
            }
        }
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
                        <img src={imageUrl} width="150" alt="Profile" />
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
