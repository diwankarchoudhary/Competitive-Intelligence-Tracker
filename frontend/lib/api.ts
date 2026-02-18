const API_BASE = "https://competitive-intelligence-tracker.onrender.com";


export async function apiGet(path: string) {
  const url = `${API_BASE}${path}`;
  console.log("GET:", url);

  const res = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!res.ok) {
    throw new Error(`GET ${path} failed: ${res.status}`);
  }

  return res.json();
}

export async function apiPost(path: string) {
  const url = `${API_BASE}${path}`;
  console.log("POST:", url);

  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!res.ok) {
    throw new Error(`POST ${path} failed: ${res.status}`);
  }

  return res.json();
}
