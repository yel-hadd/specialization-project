"use client";

import Link from "next/link";
import { useState } from "react";
import Shell from "@/components/Shell";
import { PageTitle } from "@/components/ui";
import { useI18n } from "@/lib/i18n";
import { useFetch } from "@/lib/useApi";
import type { Student } from "@/lib/types";

export default function StudentsPage() {
  const { t } = useI18n();
  const { data } = useFetch<Student[]>("/students");
  const [q, setQ] = useState("");

  const filtered = (data || []).filter((s) =>
    `${s.first_name} ${s.last_name} ${s.student_code}`.toLowerCase().includes(q.toLowerCase())
  );

  return (
    <Shell>
      <PageTitle title={t("students.title")} subtitle={t("students.subtitle")} />
      <div className="card">
        <input
          className="input mb-4 max-w-sm"
          placeholder={t("students.search")}
          value={q}
          onChange={(e) => setQ(e.target.value)}
        />
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b text-left text-slate-500">
              <th className="py-2">{t("table.code")}</th>
              <th>{t("table.lastName")}</th>
              <th>{t("table.firstName")}</th>
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
                    {t("students.viewProfile")}
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
