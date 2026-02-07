const BASE_URL = import.meta.env.VITE_API_BASE_URL.replace(/\/$/, "");


if (!BASE_URL) {
  throw new Error("VITE_API_BASE_URL is not defined");
}


export async function apiFetch<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
    },
    ...options,
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || "API request failed");
  }

  return res.json();
}
