"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { clearToken, getToken } from "@/lib/api";

const NAV = [
  { href: "/dashboard", label: "Tableau de bord" },
  { href: "/classes", label: "Classes" },
  { href: "/modules", label: "Modules" },
  { href: "/students", label: "Etudiants" },
  { href: "/anomalies", label: "Anomalies" },
  { href: "/alerts", label: "Alertes" },
  { href: "/imports", label: "Imports" },
  { href: "/reports", label: "Rapports" },
];

export default function Shell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const [ready, setReady] = useState(false);

  // Garde d'auth cote client: redirige vers login si pas de token.
  useEffect(() => {
    if (!getToken()) {
      router.replace("/login");
    } else {
      setReady(true);
    }
  }, [router]);

  if (!ready) return null;

  return (
    <div className="h-screen flex overflow-hidden">
      {/* Sidebar fixe sur la hauteur de l'ecran, le contenu principal defile a part. */}
      <aside className="w-60 shrink-0 h-screen bg-brand-dark text-white flex flex-col">
        <div className="px-5 py-5 text-lg font-bold border-b border-white/10">
          EduTrack <span className="text-brand-light">Analytics</span>
        </div>
        <nav className="flex-1 overflow-y-auto px-2 py-3 space-y-1">
          {NAV.map((item) => {
            const active = pathname.startsWith(item.href);
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`block rounded-lg px-3 py-2 text-sm ${
                  active ? "bg-white/15 font-semibold" : "hover:bg-white/10"
                }`}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>
        <button
          onClick={() => {
            clearToken();
            router.replace("/login");
          }}
          className="m-3 rounded-lg border border-white/20 px-3 py-2 text-sm hover:bg-white/10"
        >
          Deconnexion
        </button>
      </aside>
      <main className="flex-1 h-screen overflow-y-auto p-8">{children}</main>
    </div>
  );
}
