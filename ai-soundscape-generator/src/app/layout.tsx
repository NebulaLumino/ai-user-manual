import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = { title: "ai-soundscape-generator", description: "AI-powered Soundscape-Generator" };
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (<html lang="en"><body className="antialiased">{{children}}</body></html>);
}
