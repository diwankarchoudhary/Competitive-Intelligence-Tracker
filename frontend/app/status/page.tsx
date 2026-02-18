"use client";
import { useEffect, useState } from "react";
import { apiGet } from "@/lib/api";

export default function Status() {
  const [status, setStatus] = useState<any>(null);

  useEffect(() => {
    apiGet("/status").then(setStatus);
  }, []);

  if (!status) return <p>Loading...</p>;

  return (
    <main>
      <h1>Status</h1>
      <pre>{JSON.stringify(status, null, 2)}</pre>
    </main>
  );
}
