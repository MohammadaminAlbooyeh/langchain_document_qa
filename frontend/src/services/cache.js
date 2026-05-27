const cache = new Map();

export const getCached = (key) => {
  const entry = cache.get(key);
  if (!entry) return null;
  if (Date.now() > entry.expiry) {
    cache.delete(key);
    return null;
  }
  return entry.data;
};

export const setCache = (key, data, ttlMinutes = 5) => {
  cache.set(key, {
    data,
    expiry: Date.now() + ttlMinutes * 60 * 1000,
  });
};

export const clearCache = () => cache.clear();
