import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, CheckCircle2, GitFork, Cpu, Calculator, Award } from 'lucide-react';

export default function HowItWorks() {
  return (
    <div className="section-spacing">
      <div className="container">
        <div className="predict-page-header">
          <h1>How AutoMileage AI Works</h1>
          <p>From selecting your car to getting a mileage estimate.</p>
        </div>

        <div className="workflow-steps-list">
          {/* Step 1 */}
          <div className="workflow-step-card">
            <div className="step-indicator">1</div>
            <div className="step-details" style={{ width: '100%' }}>
              <h3>Choose Your Vehicle</h3>
              <p>
                Instead of requiring users to know complex technical specifications like cubic centimeters or curb weight, you simply pick your vehicle using cascading dropdowns:
              </p>
              <div className="process-steps-row" style={{ justifyContent: 'flex-start', margin: '0.75rem 0' }}>
                <span className="process-step-pill">Year</span>
                <span className="process-step-arrow">→</span>
                <span className="process-step-pill">Brand</span>
                <span className="process-step-arrow">→</span>
                <span className="process-step-pill">Model</span>
                <span className="process-step-arrow">→</span>
                <span className="process-step-pill">Variant</span>
              </div>
            </div>
          </div>

          {/* Step 2 */}
          <div className="workflow-step-card">
            <div className="step-indicator">2</div>
            <div className="step-details" style={{ width: '100%' }}>
              <h3>Get Vehicle Information</h3>
              <p>
                Once you select your specific car variant, the backend system automatically retrieves verified engineering specifications for that vehicle from the official EPA FuelEconomy dataset:
              </p>
              <ul style={{ listStyle: 'disc', paddingLeft: '1.25rem', color: 'var(--text-muted)' }}>
                <li>Engine displacement (e.g., 2.5 Liters)</li>
                <li>Cylinder count (e.g., 4 cylinders)</li>
                <li>Transmission type (e.g., Automatic 8-speed)</li>
                <li>Drive system (e.g., Front-Wheel Drive / All-Wheel Drive)</li>
                <li>Primary Fuel Type (e.g., Regular Gasoline, Diesel, Electricity)</li>
                <li>Vehicle Class category (e.g., Midsize Car, Small SUV)</li>
                <li>Model Year</li>
              </ul>
            </div>
          </div>

          {/* Step 3 */}
          <div className="workflow-step-card">
            <div className="step-indicator">3</div>
            <div className="step-details" style={{ width: '100%' }}>
              <h3>Machine Learning Analysis</h3>
              <p>
                The trained <strong>Random Forest Regression</strong> model analyzes these vehicle characteristics simultaneously. An ensemble of 100 individual decision trees votes on the expected fuel consumption.
              </p>

              {/* Ensemble Diagram */}
              <div className="tree-diagram-box">
{`Vehicle Information
        ↓
 Decision Tree 1 ──┐
 Decision Tree 2 ──┤
 Decision Tree 3 ──┤
 Decision Tree 4 ──┤
      ...          │
                   ↓
          Combined Prediction (Average)
                   ↓
             Estimated MPG`}
              </div>
            </div>
          </div>

          {/* Step 4 */}
          <div className="workflow-step-card">
            <div className="step-indicator">4</div>
            <div className="step-details" style={{ width: '100%' }}>
              <h3>Convert to km/L</h3>
              <p>
                The ML model evaluates fuel efficiency in standard EPA Miles Per Gallon (MPG). For global clarity and everyday consumer convenience, AutoMileage AI automatically converts the prediction into kilometers per liter (km/L):
              </p>
              <div className="conversion-box">
                1 MPG = 0.425144 km/L
              </div>
              <p style={{ fontSize: '0.9rem', color: 'var(--text-subtle)' }}>
                For example, an estimated 32.0 MPG is accurately converted to <strong>13.6 km/L</strong>.
              </p>
            </div>
          </div>

          {/* Step 5 */}
          <div className="workflow-step-card">
            <div className="step-indicator">5</div>
            <div className="step-details" style={{ width: '100%' }}>
              <h3>Show the Result</h3>
              <p>
                The final estimate is displayed in an intuitive, consumer-ready format along with the vehicle's efficiency rating category and complete specification breakdown:
              </p>
              <div style={{ display: 'inline-block', background: 'var(--bg-primary)', border: '1px solid var(--border-medium)', borderRadius: 'var(--radius-sm)', padding: '0.6rem 1.25rem', fontSize: '1.25rem', fontWeight: 800, color: 'var(--brand-primary)' }}>
                XX.X km/L
              </div>
            </div>
          </div>
        </div>

        {/* Why Random Forest Section */}
        <div className="why-rf-card" id="random-forest">
          <h2>Why Random Forest?</h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '1.05rem', lineHeight: '1.6' }}>
            Random Forest Regression uses multiple decision trees. Each tree makes an individual prediction based on random subsets of vehicle features, and the predictions are averaged to produce the final estimate.
          </p>

          <ul>
            <li>
              <span className="bullet-check">✔</span>
              <span><strong>Handles multiple vehicle characteristics:</strong> Easily learns interactions between engine displacement, cylinder count, transmission ratios, and vehicle weight classes.</span>
            </li>
            <li>
              <span className="bullet-check">✔</span>
              <span><strong>Captures non-linear relationships:</strong> Fuel consumption does not scale linearly with displacement or cylinders; tree ensembles model these curves naturally.</span>
            </li>
            <li>
              <span className="bullet-check">✔</span>
              <span><strong>Robust against overfitting:</strong> By aggregating 100 individual decision trees trained on bootstrap samples, variance and outliers are substantially reduced compared to a single decision tree.</span>
            </li>
            <li>
              <span className="bullet-check">✔</span>
              <span><strong>Tailored for tabular automotive data:</strong> Decision trees naturally handle mixed numeric (displacement, year) and categorical (transmission, drive type) specifications.</span>
            </li>
            <li>
              <span className="bullet-check">✔</span>
              <span><strong>Easy to explain for B.Tech PBL viva:</strong> The ensemble voting architecture offers clear interpretability and verifiable feature importance without black-box complexity.</span>
            </li>
          </ul>

          <div style={{ marginTop: '2rem' }}>
            <Link to="/predict" className="btn btn-primary">
              Try It Now with Your Car
              <ArrowRight size={18} />
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
