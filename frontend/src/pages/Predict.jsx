import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, RefreshCw, CheckCircle, AlertCircle, Fuel, Settings, Activity } from 'lucide-react';
import { fetchYears, fetchMakes, fetchModels, fetchVariants, predictMileage } from '../services/api';

export default function Predict() {
  // Cascading Selection States
  const [years, setYears] = useState([]);
  const [makes, setMakes] = useState([]);
  const [models, setModels] = useState([]);
  const [variants, setVariants] = useState([]);

  const [selectedYear, setSelectedYear] = useState('');
  const [selectedMake, setSelectedMake] = useState('');
  const [selectedModel, setSelectedModel] = useState('');
  const [selectedVariantId, setSelectedVariantId] = useState('');

  // Status & Prediction Results
  const [loadingDropdowns, setLoadingDropdowns] = useState({
    years: false,
    makes: false,
    models: false,
    variants: false,
  });
  const [isPredicting, setIsPredicting] = useState(false);
  const [predictionResult, setPredictionResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  // 1. Initial Load: Fetch Years
  useEffect(() => {
    async function loadYears() {
      try {
        setLoadingDropdowns((prev) => ({ ...prev, years: true }));
        setErrorMessage(null);
        const data = await fetchYears();
        setYears(data);
      } catch (err) {
        setErrorMessage('Failed to connect to backend server. Please verify backend is running on port 8000.');
      } finally {
        setLoadingDropdowns((prev) => ({ ...prev, years: false }));
      }
    }
    loadYears();
  }, []);

  // 2. Year Changed -> Fetch Makes
  const handleYearChange = async (e) => {
    const year = e.target.value;
    setSelectedYear(year);
    setSelectedMake('');
    setSelectedModel('');
    setSelectedVariantId('');
    setMakes([]);
    setModels([]);
    setVariants([]);
    setPredictionResult(null);
    setErrorMessage(null);

    if (!year) return;

    try {
      setLoadingDropdowns((prev) => ({ ...prev, makes: true }));
      const data = await fetchMakes(year);
      setMakes(data);
    } catch (err) {
      setErrorMessage(`Failed to load brands for year ${year}: ${err.message}`);
    } finally {
      setLoadingDropdowns((prev) => ({ ...prev, makes: false }));
    }
  };

  // 3. Make Changed -> Fetch Models
  const handleMakeChange = async (e) => {
    const make = e.target.value;
    setSelectedMake(make);
    setSelectedModel('');
    setSelectedVariantId('');
    setModels([]);
    setVariants([]);
    setPredictionResult(null);
    setErrorMessage(null);

    if (!make) return;

    try {
      setLoadingDropdowns((prev) => ({ ...prev, models: true }));
      const data = await fetchModels(selectedYear, make);
      setModels(data);
    } catch (err) {
      setErrorMessage(`Failed to load models for ${make}: ${err.message}`);
    } finally {
      setLoadingDropdowns((prev) => ({ ...prev, models: false }));
    }
  };

  // 4. Model Changed -> Fetch Variants
  const handleModelChange = async (e) => {
    const model = e.target.value;
    setSelectedModel(model);
    setSelectedVariantId('');
    setVariants([]);
    setPredictionResult(null);
    setErrorMessage(null);

    if (!model) return;

    try {
      setLoadingDropdowns((prev) => ({ ...prev, variants: true }));
      const data = await fetchVariants(selectedYear, selectedMake, model);
      setVariants(data);
      // Auto-select if only 1 configuration exists
      if (data.length === 1) {
        setSelectedVariantId(data[0].id.toString());
      }
    } catch (err) {
      setErrorMessage(`Failed to load configurations for ${model}: ${err.message}`);
    } finally {
      setLoadingDropdowns((prev) => ({ ...prev, variants: false }));
    }
  };

  // 5. Variant Changed
  const handleVariantChange = (e) => {
    setSelectedVariantId(e.target.value);
    setErrorMessage(null);
  };

  // 6. Execute ML Prediction
  const handlePredict = async () => {
    if (!selectedVariantId) return;

    setIsPredicting(true);
    setErrorMessage(null);

    try {
      const selectedVariantObj = variants.find(
        (v) => v.id.toString() === selectedVariantId.toString()
      );

      const payload = {
        vehicleId: parseInt(selectedVariantId, 10),
        year: parseInt(selectedYear, 10),
        make: selectedMake,
        model: selectedModel,
        variant: selectedVariantObj ? selectedVariantObj.variant : undefined,
      };

      const result = await predictMileage(payload);
      setPredictionResult(result);
    } catch (err) {
      setErrorMessage(`Prediction failed: ${err.message}`);
    } finally {
      setIsPredicting(false);
    }
  };

  // Reset for another vehicle
  const handleReset = () => {
    setPredictionResult(null);
    setSelectedVariantId('');
  };

  const isFormComplete = Boolean(
    selectedYear && selectedMake && selectedModel && selectedVariantId
  );

  return (
    <div className="section-spacing">
      <div className="container">
        <div className="predict-page-header">
          <h1>Predict Your Mileage</h1>
          <p>Select your vehicle and we'll estimate its fuel mileage.</p>
        </div>

        {errorMessage && (
          <div
            style={{
              maxWidth: '640px',
              margin: '0 auto 1.5rem',
              padding: '1rem',
              backgroundColor: 'var(--error-bg)',
              border: '1px solid var(--error-border)',
              borderRadius: 'var(--radius-sm)',
              color: 'var(--error-text)',
              display: 'flex',
              alignItems: 'center',
              gap: '0.6rem',
            }}
          >
            <AlertCircle size={20} />
            <span>{errorMessage}</span>
          </div>
        )}

        {/* Dynamic Form Card (Only shown if no result, or user can toggle) */}
        {!predictionResult ? (
          <div className="prediction-card">
            {/* Step 1 - Model Year */}
            <div className="form-group">
              <label htmlFor="year-select" className="form-label">
                <span className="step-num">Step 1 —</span> Model Year
              </label>
              <select
                id="year-select"
                className="select-control"
                value={selectedYear}
                onChange={handleYearChange}
                disabled={loadingDropdowns.years}
              >
                <option value="">
                  {loadingDropdowns.years ? 'Loading years...' : 'Select Year ▼'}
                </option>
                {years.map((yr) => (
                  <option key={yr} value={yr}>
                    {yr}
                  </option>
                ))}
              </select>
            </div>

            {/* Step 2 - Brand */}
            <div className="form-group">
              <label htmlFor="make-select" className="form-label">
                <span className="step-num">Step 2 —</span> Brand
              </label>
              <select
                id="make-select"
                className="select-control"
                value={selectedMake}
                onChange={handleMakeChange}
                disabled={!selectedYear || loadingDropdowns.makes}
              >
                <option value="">
                  {!selectedYear
                    ? 'Select year first'
                    : loadingDropdowns.makes
                    ? 'Loading brands...'
                    : 'Select Brand ▼'}
                </option>
                {makes.map((mk) => (
                  <option key={mk} value={mk}>
                    {mk}
                  </option>
                ))}
              </select>
            </div>

            {/* Step 3 - Model */}
            <div className="form-group">
              <label htmlFor="model-select" className="form-label">
                <span className="step-num">Step 3 —</span> Model
              </label>
              <select
                id="model-select"
                className="select-control"
                value={selectedModel}
                onChange={handleModelChange}
                disabled={!selectedMake || loadingDropdowns.models}
              >
                <option value="">
                  {!selectedMake
                    ? 'Select brand first'
                    : loadingDropdowns.models
                    ? 'Loading models...'
                    : 'Select Model ▼'}
                </option>
                {models.map((mdl) => (
                  <option key={mdl} value={mdl}>
                    {mdl}
                  </option>
                ))}
              </select>
            </div>

            {/* Step 4 - Variant */}
            <div className="form-group">
              <label htmlFor="variant-select" className="form-label">
                <span className="step-num">Step 4 —</span> Variant
              </label>
              <select
                id="variant-select"
                className="select-control"
                value={selectedVariantId}
                onChange={handleVariantChange}
                disabled={!selectedModel || loadingDropdowns.variants}
              >
                <option value="">
                  {!selectedModel
                    ? 'Select model first'
                    : loadingDropdowns.variants
                    ? 'Loading configurations...'
                    : 'Select Variant ▼'}
                </option>
                {variants.map((v) => (
                  <option key={v.id} value={v.id}>
                    {v.variant}
                  </option>
                ))}
              </select>
            </div>

            {/* Predict Button */}
            <div style={{ marginTop: '2rem' }}>
              <button
                className="btn btn-primary btn-large"
                onClick={handlePredict}
                disabled={!isFormComplete || isPredicting}
              >
                {isPredicting ? (
                  <>
                    <RefreshCw className="spin" size={20} />
                    Calculating your estimated mileage...
                  </>
                ) : (
                  '🚗 Predict My Mileage'
                )}
              </button>
            </div>
          </div>
        ) : (
          /* RESULT CARD */
          <div className="result-card">
            <div className="result-header-tag">YOUR ESTIMATED MILEAGE</div>

            {/* Large Mileage Highlight */}
            <div className="result-mileage-number">
              {predictionResult.predicted_kmpl} <span style={{ fontSize: '2rem', fontWeight: 600 }}>km/L</span>
            </div>

            <div className="result-mileage-mpg">
              ≈ {predictionResult.predicted_mpg} MPG
            </div>

            {/* Efficiency Badge */}
            <div className="result-badge-container">
              <span className="badge badge-success">
                <CheckCircle size={14} />
                {predictionResult.efficiency_rating}
              </span>
            </div>

            {/* Vehicle Title & Variant */}
            <div className="result-vehicle-name">
              {predictionResult.vehicle}
            </div>
            <div className="result-vehicle-variant">
              {predictionResult.variant}
            </div>

            {/* Vehicle Details Section */}
            <div className="result-specs-section">
              <div className="result-specs-title">
                <Settings size={18} />
                <span>Vehicle Specifications (Retrieved from EPA Dataset)</span>
              </div>

              <div className="specs-grid">
                {predictionResult.specs.engine && (
                  <div className="spec-item">
                    <span className="spec-key">Engine</span>
                    <span className="spec-val">{predictionResult.specs.engine}</span>
                  </div>
                )}
                {predictionResult.specs.cylinders && (
                  <div className="spec-item">
                    <span className="spec-key">Cylinders</span>
                    <span className="spec-val">{predictionResult.specs.cylinders}</span>
                  </div>
                )}
                {predictionResult.specs.transmission && (
                  <div className="spec-item">
                    <span className="spec-key">Transmission</span>
                    <span className="spec-val">{predictionResult.specs.transmission}</span>
                  </div>
                )}
                {predictionResult.specs.fuel_type && (
                  <div className="spec-item">
                    <span className="spec-key">Fuel Type</span>
                    <span className="spec-val">{predictionResult.specs.fuel_type}</span>
                  </div>
                )}
                {predictionResult.specs.drive_type && (
                  <div className="spec-item">
                    <span className="spec-key">Drive Type</span>
                    <span className="spec-val">{predictionResult.specs.drive_type}</span>
                  </div>
                )}
                {predictionResult.specs.vehicle_class && (
                  <div className="spec-item">
                    <span className="spec-key">Vehicle Class</span>
                    <span className="spec-val">{predictionResult.specs.vehicle_class}</span>
                  </div>
                )}
              </div>
            </div>

            {/* Action Buttons */}
            <div className="result-actions">
              <button className="btn btn-primary" onClick={handleReset}>
                <RefreshCw size={18} />
                Predict Another Vehicle
              </button>
              <Link to="/" className="btn btn-secondary">
                <ArrowLeft size={18} />
                Back to Home
              </Link>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
