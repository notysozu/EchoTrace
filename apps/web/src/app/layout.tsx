import type { Metadata } from "next";
import "./globals.css";
import Providers from "./providers";
import MiniPlayer from "@/components/MiniPlayer";

export const metadata: Metadata = {
  title: "EchoTrace",
  description: "Audio-first historical knowledge platform.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="bg-slate-950 text-slate-50 antialiased min-h-screen pb-24">
        <Providers>
          <main className="max-w-4xl mx-auto px-4 py-8">
            {children}
          </main>
          <MiniPlayer />
        </Providers>
      </body>
    </html>
  );
}
