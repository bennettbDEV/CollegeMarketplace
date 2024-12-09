//Navbar.jsx
import React from 'react';
import './styles/Navbar.css';
import userIcon from '../assets/usericon.png';
import settingsIcon from '../assets/settingsicon.png';
import homeIcon from '../assets/homeicon.png'; // Import the home icon

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-left">
        <a href="/" className="logo">
          <img src={homeIcon} alt="Home" className="home-icon" /> {/* Home Icon */}
          ISU Marketplace
        </a>
      </div>
      <div className="navbar-center">
        <ul className="nav-links">
          <li>
            <a href="/createlisting">Create Listing</a>
          </li>
          <li>
            <a href="/saved">Saved</a>
          </li>
          <li>
            <a href="/messages">Messages</a>
          </li>
        </ul>
      </div>
      <div className="navbar-right">
        <a href="/profile" className="profile-icon">
          <img src={userIcon} alt="Profile" />
        </a>
        <a href="/settings" className="settings">
          <img src={settingsIcon} alt="Settings" />
        </a>
      </div>
    </nav>
  );
};

export default Navbar;
