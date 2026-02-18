"use client";
import { useEffect, useState } from "react";
import { apiGet, apiPost } from "@/lib/api";

export default function Competitor({ params }: any) {
  const id = params.id;
  const [history, setHistory] = useState<any[]>([]);
  const [message, setMessage] = useState("");

  const loadHistory = () => {
    apiGet(`/history/${id}`).then(res => setHistory(res.history));
  };

  const checkNow = async () => {
    const res = await apiPost(`/check/${id}`);
    setMessage(res.message);
    loadHistory();
  };

  useEffect(() => {
    loadHistory();
  }, []);

  return (
    <main>
      <h2>Competitor #{id}</h2>
      <button onClick={checkNow}>Check now</button>
      <p>{message}</p>

      <h3>History</h3>
      <ul>
        {history.map(h => (
          <li key={h.diff_id}>
            <pre>{h.summary}</pre>
          </li>
        ))}
      </ul>
    </main>
  );
}
