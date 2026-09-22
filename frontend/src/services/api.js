/**
 * AutoMileage AI - API Service
 * Handles communication with the FastAPI backend.
 * Automatically handles CORS or Vite proxy.
 */

// If running in development on port 5173 or other dev port, connect directly to backend on 8000 or via proxy
const getApiBase = () => {
  if (typeof window !== 'undefined') {
    if (window.location.port === '5173') {
      return 'http://127.0.0.1:8000/api';
    }
  }
  return '/api';
};

const API_BASE_URL = getApiBase();

async function handleResponse(response) {
  if (!response.ok) {
    let errorMessage = `HTTP ${response.status} ${response.statusText}`;
    try {
      const errorJson = await response.json();
      if (errorJson.detail) {
        errorMessage = typeof errorJson.detail === 'string' 
          ? errorJson.detail 
          : JSON.stringify(errorJson.detail);
      }
    } catch {
      // Use generic error if response is not json
    }
    throw new Error(errorMessage);
  }
  return response.json();
}

export async function fetchYears() {
  const response = await fetch(`${API_BASE_URL}/years`);
  return handleResponse(response);
}

export async function fetchMakes(year) {
  const response = await fetch(`${API_BASE_URL}/makes?year=${encodeURIComponent(year)}`);
  return handleResponse(response);
}

export async function fetchModels(year, make) {
  const response = await fetch(
    `${API_BASE_URL}/models?year=${encodeURIComponent(year)}&make=${encodeURIComponent(make)}`
  );
  return handleResponse(response);
}

export async function fetchVariants(year, make, model) {
  const response = await fetch(
    `${API_BASE_URL}/variants?year=${encodeURIComponent(year)}&make=${encodeURIComponent(make)}&model=${encodeURIComponent(model)}`
  );
  return handleResponse(response);
}

export async function predictMileage({ vehicleId, year, make, model, variant }) {
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      vehicle_id: vehicleId,
      year: year ? parseInt(year, 10) : undefined,
      make: make,
      model: model,
      variant: variant,
    }),
  });
  return handleResponse(response);
}

export async function fetchModelInsights() {
  const response = await fetch(`${API_BASE_URL}/model-insights`);
  return handleResponse(response);
}
