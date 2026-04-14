// Define environments
export const ENV = {
  MANGU_API: 'http://127.0.0.1:5000',
  GLOBAL_API: 'https://global-processes.onrender.com'
};

export const URLS = {
  // Mangu Local Endpoints
  leadership: `${ENV.MANGU_API}/leadership`,
  events: `${ENV.MANGU_API}/events`,

  // Auth / Admin Endpoints
  adminLogin: `${ENV.GLOBAL_API}/auth/api/login`,

  // Media / Gallery Endpoints
  mediaUpload: `${ENV.GLOBAL_API}/media/api/upload`,
  mediaImages: (folder: string, limit: number = 80) => 
    `${ENV.GLOBAL_API}/media/api/images?limit=${limit}&folder=${encodeURIComponent(folder)}`,
  mediaImagesNext: (cursor: string, folder: string, limit: number = 80) => 
    `${ENV.GLOBAL_API}/media/api/images/next?cursor=${encodeURIComponent(cursor)}&limit=${limit}&folder=${encodeURIComponent(folder)}`,
};
