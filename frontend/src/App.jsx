import React from "react"
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import Login from "./pages/Login"
import Register from "./pages/Register"
import Home from "./pages/Home"
import NotFound from "./pages/NotFound"
import Profile from "./pages/Profile"
import SingleListing from "./pages/SingleListing";
import FavoriteListings from "./pages/FavoriteListings" // Import the SavedListings component
import ProtectedRoute from "./components/ProtectedRoute"
import CreateListing from "./pages/CreateListing"

function Logout() {
  localStorage.clear()
  return <Navigate to="/login" />
}

function RegisterAndLogout() {
  localStorage.clear()
  return <Register />
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="/register" element={<RegisterAndLogout />} />
        <Route path="/listings/:listingId" element={<SingleListing />} />

        <Route path="/profile" element={
          <ProtectedRoute>
            <Profile />
          </ProtectedRoute>
        } />
        <Route
          path="/saved" element={
            <ProtectedRoute>
              <FavoriteListings />
            </ProtectedRoute>
          }
        />
        <Route path="/createListing" element={
          <ProtectedRoute>
            <CreateListing />
          </ProtectedRoute>
        } />


        <Route path="*" element={<NotFound />}></Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
