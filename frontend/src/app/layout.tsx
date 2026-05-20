import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CMO Dashboard - Tigo Colombia",
  description: "Network Intelligence Dashboard",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" className="h-full">
      <body className="bg-gray-950 text-white min-h-screen h-full">
        {children}
      </body>
    </html>
  );
}
