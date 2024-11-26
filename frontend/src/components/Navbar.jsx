import React from 'react';
import './styles/Navbar.css';

const Navbar = () => {
  return (

<nav className="navbar">
  <div className="navbar-left">
    <a href="/" className="logo">
      ISU Marketplace
    </a>
  </div>
  <div className="navbar-center">
    <ul className="nav-links">
      <li>
        <a href="/filter">Filter/Search</a>
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
        //Insert pic here
    </a>
    <a href="/settings" className="settings">
      //Insert setting gear here
    </a>
  </div>
</nav>
);
};

export default Navbar;