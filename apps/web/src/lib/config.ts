const DEFAULT_API_BASE_URL = "http://localhost:8000";

function getConfiguredApiBaseUrl() {
  return import.meta.env.VITE_API_BASE_URL?.trim() ?? "";
}

export function getApiBaseUrl() {
  return getConfiguredApiBaseUrl() || DEFAULT_API_BASE_URL;
}

export function shouldUseStaticJobData() {
  return import.meta.env.PROD && !getConfiguredApiBaseUrl();
}
