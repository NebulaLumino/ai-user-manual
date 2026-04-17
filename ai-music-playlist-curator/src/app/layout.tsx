import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = { title: "ai-music-playlist-curator", description: "AI-powered Music-Playlist-Curator" };
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (<html lang="en"><body className="antialiased">{{children}}</body></html>);
}
