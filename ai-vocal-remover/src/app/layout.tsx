import type { Metadata } from "next";
import "./globals.css";

const metadata: Metadata = {
  title: "placeholder",
  description: "AI-powered app",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
