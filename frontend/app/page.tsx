"use client";
import { useEffect, useState } from "react";
import { apiGet } from "@/lib/api";
import Link from "next/link";

export default function Home() {
  const [competitors, setCompetitors] = useState<any[]>([]);

  useEffect(() => {
    apiGet("/competitors").then(setCompetitors);
  }, []);

  return (
    <main>
      <h1>Competitive Intelligence Tracker</h1>

      <ul>
        {competitors.map(c => (
          <li key={c.id}>
            <Link href={`/competitors/${c.id}`}>
              {c.name}
            </Link>
          </li>
        ))}
      </ul>
    </main>
  );
}
