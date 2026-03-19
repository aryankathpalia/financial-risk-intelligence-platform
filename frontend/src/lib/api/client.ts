const RAW_BASE_URL = import.meta.env.VITE_API_BASE_URL;

if (!RAW_BASE_URL) {
  throw new Error("VITE_API_BASE_URL is not defined");
}

// FORCE HTTPS EVEN IF ENV IS WRONG
const BASE_URL = RAW_BASE_URL.replace(/^http:\/\//, "https://");

// -----------------------------
// SIMPLE IN-MEMORY CACHE
// -----------------------------
type CacheEntry<T> = {
  data: T;
  timestamp: number;
};

const CACHE_TTL = 30_000; // 30 seconds (tweak if needed)

const responseCache = new Map<string, CacheEntry<any>>();
const inFlightRequests = new Map<string, Promise<any>>();

// -----------------------------
// API FETCH WITH CACHE
// -----------------------------
export async function apiFetch<T>(
  path: string,
  options: RequestInit = {},
  useCache: boolean = true
): Promise<T> {
  const url = `${BASE_URL}${path}`;
  const now = Date.now();

  // 1️ Return cached response if valid
  if (useCache && responseCache.has(url)) {
    const cached = responseCache.get(url)!;
    if (now - cached.timestamp < CACHE_TTL) {
      return cached.data as T;
    } else {
      responseCache.delete(url); // stale
    }
  }

  // 2️ Deduplicate in-flight requests
  if (useCache && inFlightRequests.has(url)) {
    return inFlightRequests.get(url)! as Promise<T>;
  }

  // 3️ Make network request
  const request = fetch(url, {
    headers: {
      "Content-Type": "application/json",
    },
    ...options,
  })
    .then(async (res) => {
      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || "API request failed");
      }
      return res.json();
    })
    .then((data) => {
      if (useCache) {
        responseCache.set(url, {
          data,
          timestamp: Date.now(),
        });
      }
      return data;
    })
    .finally(() => {
      inFlightRequests.delete(url);
    });

  if (useCache) {
    inFlightRequests.set(url, request);
  }

  return request;
}
