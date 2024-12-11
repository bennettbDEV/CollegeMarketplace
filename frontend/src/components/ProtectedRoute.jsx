import { Navigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import { useState, useEffect, useCallback  } from "react";
import { REFRESH_TOKEN, ACCESS_TOKEN } from "../constants";
import api from "../api";

function ProtectedRoute({ children }) {
    const [isAuthorized, setIsAuthorized] = useState(null);

    const refreshToken = useCallback(async () => {
        const refreshToken = localStorage.getItem(REFRESH_TOKEN);
        try {
            const res = await api.post("/api/token/refresh/", { refresh: refreshToken });
            if (res.status === 200) {
                localStorage.setItem(ACCESS_TOKEN, res.data.access);
                setIsAuthorized(true);
            } else {
                setIsAuthorized(false);
            }
        } catch (error) {
            console.error("Error refreshing token:", error);
            setIsAuthorized(false);
        }
    }, []);

    const auth = useCallback(async () => {
        const token = localStorage.getItem(ACCESS_TOKEN);
        if (!token) {
            setIsAuthorized(false);
            return;
        }

        try {
            const decoded = jwtDecode(token);
            const tokenExpiration = decoded.exp;
            const now = Date.now() / 1000;

            if (tokenExpiration < now) {
                await refreshToken();
            } else {
                setIsAuthorized(true);
            }
        } catch (error) {
            console.error("Error decoding token:", error);
            setIsAuthorized(false);
        }
    }, [refreshToken]);

    useEffect(() => {
        const interval = setInterval(() => {
            const token = localStorage.getItem(ACCESS_TOKEN);
            if (token) {
                const decoded = jwtDecode(token);
                const tokenExpiration = decoded.exp;
                const now = Date.now() / 1000;

                // Refresh token proactively before it expires
                if (tokenExpiration - now < 60) {
                    refreshToken();
                }
            }
        }, 60000); // Check every 60 seconds

        auth(); // Initial authentication check
        return () => clearInterval(interval);
    }, [auth, refreshToken]);

    if (isAuthorized === null) {
        return <div>Loading...</div>;
    }

    return isAuthorized ? children : <Navigate to="/login" />;
}

export default ProtectedRoute;