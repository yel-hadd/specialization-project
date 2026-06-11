import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "EduTrack Analytics",
  description: "Plateforme d'analyse de performance des etudiants",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr">
      <body>{children}</body>
    </html>
  );
}
