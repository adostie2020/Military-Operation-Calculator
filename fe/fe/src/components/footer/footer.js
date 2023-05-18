import React from 'react';
import './footer.css';

function Footer() {
  return (
    <footer>
      <p>&copy; {new Date().getFullYear()}</p>
    </footer>
  );
}

export default Footer;