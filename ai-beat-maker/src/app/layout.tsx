import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = { title: "ai-beat-maker", description: "AI-powered Beat-Maker" };
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (<html lang="en"><body className="antialiased">{{children}}</body></html>);
}
