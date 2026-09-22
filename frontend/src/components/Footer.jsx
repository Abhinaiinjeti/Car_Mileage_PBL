import React from 'react';
import { Link } from 'react-router-dom';

export default function Footer() {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-inner">
          <div className="footer-brand">
            <h4>AutoMileage AI</h4>
            <p>
              An intelligent vehicle fuel mileage prediction platform using machine learning on official U.S. EPA data.
            </p>
            <div className="footer-academic-badge">
              B.Tech Project-Based Learning (PBL)
            </div>
          </div>

          <div className="footer-links">
            <h5>Navigation</h5>
            <ul>
              <li><Link to="/">Home</Link></li>
              <li><Link to="/predict">Predict Mileage</Link></li>
              <li><Link to="/how-it-works">How It Works</Link></li>
              <li><Link to="/about">About & Insights</Link></li>
            </ul>
          </div>

          <div className="footer-links">
            <h5>Data & Source</h5>
            <ul>
              <li><a href="https://www.fueleconomy.gov" target="_blank" rel="noopener noreferrer">U.S. EPA FuelEconomy</a></li>
              <li><Link to="/about#metrics">Model Performance</Link></li>
              <li><Link to="/how-it-works#random-forest">Random Forest Docs</Link></li>
            </ul>
          </div>
        </div>

        <div className="footer-bottom">
          <p>
            Disclaimer: Estimated mileage is based on vehicle specifications and the machine-learning model used by this application. 
            Actual fuel economy may vary depending on driving style, traffic, road conditions, weather, vehicle condition and other factors.
          </p>
          <p>
            © 2026 AutoMileage AI. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}
