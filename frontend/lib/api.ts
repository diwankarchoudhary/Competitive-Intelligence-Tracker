const BASE_URL = "http://127.0.0.1:8000";

export async function apiGet(path: string) {
  const url = `${BASE_URL}${path}`;
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
  const url = `${BASE_URL}${path}`;
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
