import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, ChevronRight, CheckCircle2 } from 'lucide-react';

export default function Home() {
  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="container">
          <span className="hero-brand-tag">AutoMileage AI</span>
          <h1 className="hero-title">Know Your Car's Mileage</h1>
          <p className="hero-subtitle">
            Select your car and get an estimated fuel mileage using Machine Learning.
          </p>

          <div className="hero-actions">
            <Link to="/predict" className="btn btn-primary">
              Predict Mileage
              <ArrowRight size={18} />
            </Link>
            <Link to="/how-it-works" className="btn btn-secondary">
              How It Works
            </Link>
          </div>

          {/* Clean Automotive Visual Illustration */}
          <div className="hero-vehicle-visual">
            <svg
              className="hero-car-svg"
              viewBox="0 0 720 220"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              aria-label="Clean automotive vehicle illustration"
            >
              {/* Road line */}
              <line x1="20" y1="190" x2="700" y2="190" stroke="#cbd5e1" strokeWidth="3" strokeDasharray="12 8" />
              
              {/* Vehicle Body Shadow */}
              <ellipse cx="360" cy="195" rx="270" ry="8" fill="#e2e8f0" />

              {/* Main Vehicle Silhouette */}
              <path
                d="M100 160 
                   C 100 145, 120 135, 170 130 
                   L 250 120 
                   C 285 90, 340 65, 410 65 
                   L 520 65 
                   C 570 65, 620 95, 640 125 
                   L 660 138 
                   C 675 145, 680 155, 680 165 
                   L 670 172 
                   C 660 172, 650 172, 640 172 
                   C 635 145, 595 145, 590 172 
                   L 260 172 
                   C 255 145, 215 145, 210 172 
                   L 105 172 
                   Z"
                fill="#1e3a8a"
              />

              {/* Cabin Windows */}
              <path
                d="M265 120 
                   L 335 80 
                   C 365 77, 440 77, 460 77 
                   L 460 120 
                   Z"
                fill="#e0f2fe"
              />
              <path
                d="M475 77 
                   L 525 77 
                   C 560 77, 595 98, 615 120 
                   L 475 120 
                   Z"
                fill="#e0f2fe"
              />

              {/* Headlight & Taillight accents */}
              <path d="M660 142 L 678 145 C 678 152, 672 155, 660 155 Z" fill="#38bdf8" />
              <path d="M105 140 L 98 145 C 98 153, 106 155, 114 155 Z" fill="#ef4444" />

              {/* Wheels */}
              {/* Front Wheel */}
              <circle cx="615" cy="172" r="34" fill="#0f172a" />
              <circle cx="615" cy="172" r="22" fill="#94a3b8" />
              <circle cx="615" cy="172" r="10" fill="#0f172a" />

              {/* Rear Wheel */}
              <circle cx="235" cy="172" r="34" fill="#0f172a" />
              <circle cx="235" cy="172" r="22" fill="#94a3b8" />
              <circle cx="235" cy="172" r="10" fill="#0f172a" />

              {/* Subtle Body Contour Line */}
              <path d="M165 140 Q 360 135 645 140" stroke="#3b82f6" strokeWidth="2.5" strokeLinecap="round" />
            </svg>
          </div>
        </div>
      </section>

      {/* Feature Cards Section */}
      <section className="section-spacing">
        <div className="container">
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon-wrapper">🚗</div>
              <h3>Simple</h3>
              <p>Select your car instead of entering technical specifications.</p>
            </div>

            <div className="feature-card">
              <div className="feature-icon-wrapper">🤖</div>
              <h3>Smart</h3>
              <p>Machine Learning analyzes your vehicle characteristics.</p>
            </div>

            <div className="feature-card">
              <div className="feature-icon-wrapper">⚡</div>
              <h3>Quick</h3>
              <p>Get an estimated mileage in seconds.</p>
            </div>
          </div>

          {/* Simple Process Flow */}
          <div className="process-section">
            <h2>How You Get Your Estimate</h2>
            <div className="process-steps-row">
              <div className="process-step-pill">Choose Your Car</div>
              <div className="process-step-arrow">↓</div>
              <div className="process-step-pill">Vehicle Specifications</div>
              <div className="process-step-arrow">↓</div>
              <div className="process-step-pill">Machine Learning</div>
              <div className="process-step-arrow">↓</div>
              <div className="process-step-pill">Mileage Estimate</div>
            </div>
          </div>

          {/* Disclaimer Box */}
          <div className="disclaimer-box">
            <strong>Disclaimer:</strong> Estimated mileage is based on the vehicle information and machine-learning model used by this application. Actual fuel economy may vary depending on driving style, traffic, road conditions, weather, vehicle condition and other factors.
          </div>
        </div>
      </section>
    </div>
  );
}
