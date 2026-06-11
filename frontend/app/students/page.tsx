"use client";

import Link from "next/link";
import { useState } from "react";
import Shell from "@/components/Shell";
import { PageTitle } from "@/components/ui";
import { useFetch } from "@/lib/useApi";
import type { Student } from "@/lib/types";

export default function StudentsPage() {
  const { data } = useFetch<Student[]>("/students");
  const [q, setQ] = useState("");

  const filtered = (data || []).filter((s) =>
    `${s.first_name} ${s.last_name} ${s.student_code}`.toLowerCase().includes(q.toLowerCase())
  );

  return (
    <Shell>
      <PageTitle title="Etudiants" subtitle="Liste et fiches individuelles" />
      <div className="card">
        <input
          className="input mb-4 max-w-sm"
          placeholder="Rechercher par nom ou code..."
          value={q}
          onChange={(e) => setQ(e.target.value)}
        />
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-slate-500 border-b">
              <th className="py-2">Code</th>
              <th>Nom</th>
              <th>Prenom</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {filtered.slice(0, 200).map((s) => (
              <tr key={s.id} className="border-b last:border-0">
                <td className="py-2 font-mono text-xs">{s.student_code}</td>
                <td className="font-medium">{s.last_name}</td>
                <td>{s.first_name}</td>
                <td className="text-right">
                  <Link href={`/students/${s.id}`} className="text-brand hover:underline">
                    Voir la fiche
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Shell>
  );
}
