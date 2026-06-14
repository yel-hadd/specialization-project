"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { clearToken, getToken } from "@/lib/api";
import { useI18n } from "@/lib/i18n";
import { LanguageSwitcher } from "@/components/ui";

const NAV = [
  { href: "/dashboard", key: "nav.dashboard" },
  { href: "/classes", key: "nav.classes" },
  { href: "/modules", key: "nav.modules" },
  { href: "/students", key: "nav.students" },
  { href: "/anomalies", key: "nav.anomalies" },
  { href: "/alerts", key: "nav.alerts" },
  { href: "/imports", key: "nav.imports" },
  { href: "/reports", key: "nav.reports" },
];

export default function Shell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const { t } = useI18n();
  const [ready, setReady] = useState(false);

  // Client-side auth guard: redirect to login when no token is present.
  useEffect(() => {
    if (!getToken()) {
      router.replace("/login");
    } else {
      setReady(true);
    }
  }, [router]);

  if (!ready) return null;

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar fixed to the screen height; the main content scrolls separately. */}
      <aside className="flex h-screen w-60 shrink-0 flex-col bg-brand-dark text-white">
        <div className="border-b border-white/10 px-5 py-5 text-lg font-bold">
          EduTrack <span className="text-brand-light">Analytics</span>
        </div>
        <nav className="flex-1 space-y-1 overflow-y-auto px-2 py-3">
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
                {t(item.key)}
              </Link>
            );
          })}
        </nav>
        <LanguageSwitcher className="px-3 pb-2" />
        <button
          onClick={() => {
            clearToken();
            router.replace("/login");
          }}
          className="m-3 rounded-lg border border-white/20 px-3 py-2 text-sm hover:bg-white/10"
        >
          {t("nav.logout")}
        </button>
      </aside>
      <main className="h-screen flex-1 overflow-y-auto p-8">{children}</main>
    </div>
  );
}
