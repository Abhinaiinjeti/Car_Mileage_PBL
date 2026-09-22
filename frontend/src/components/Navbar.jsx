import React, { useState } from 'react';
import { NavLink, Link } from 'react-router-dom';
import { Gauge, Menu, X } from 'lucide-react';

export default function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const toggleMobileMenu = () => {
    setMobileMenuOpen(!mobileMenuOpen);
  };

  const closeMobileMenu = () => {
    setMobileMenuOpen(false);
  };

  return (
    <header className="navbar">
      <div className="container navbar-inner">
        <Link to="/" className="brand-logo" onClick={closeMobileMenu}>
          <div className="brand-logo-icon">
            <Gauge size={22} strokeWidth={2.5} />
          </div>
          <span>AutoMileage AI</span>
        </Link>

        {/* Desktop Navigation */}
        <nav>
          <ul className="nav-links">
            <li>
              <NavLink to="/" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
                Home
              </NavLink>
            </li>
            <li>
              <NavLink to="/predict" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
                Predict Mileage
              </NavLink>
            </li>
            <li>
              <NavLink to="/how-it-works" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
                How It Works
              </NavLink>
            </li>
            <li>
              <NavLink to="/about" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
                About
              </NavLink>
            </li>
          </ul>
        </nav>

        {/* Mobile Hamburger Toggle Button */}
        <button 
          className="mobile-menu-btn" 
          onClick={toggleMobileMenu}
          aria-label="Toggle navigation menu"
        >
          {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {/* Mobile Dropdown Menu */}
      {mobileMenuOpen && (
        <div className="mobile-nav open">
          <NavLink to="/" className="nav-link" onClick={closeMobileMenu}>
            Home
          </NavLink>
          <NavLink to="/predict" className="nav-link" onClick={closeMobileMenu}>
            Predict Mileage
          </NavLink>
          <NavLink to="/how-it-works" className="nav-link" onClick={closeMobileMenu}>
            How It Works
          </NavLink>
          <NavLink to="/about" className="nav-link" onClick={closeMobileMenu}>
            About
          </NavLink>
        </div>
      )}
    </header>
  );
}
