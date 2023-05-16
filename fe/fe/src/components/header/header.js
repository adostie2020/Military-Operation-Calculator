import React from 'react';
import './header.css'; // Import the CSS file


const Header = () => {
  return (
    <header>
      <h1>PACAF</h1>
      <nav>
        <ul>
        <li><a href="/">Calculator</a></li>
          <li><a href="/">New Flight</a></li>
          <li><a href="/about">Aircraft Table</a></li>
          <li><a href="/contact">Exercise Table</a></li>
        </ul>
      </nav>
    </header>
  );
}

export default Header;