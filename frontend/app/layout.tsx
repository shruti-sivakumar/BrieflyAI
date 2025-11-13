import "./globals.css";
import Link from "next/link";
import AuthControls from "@/components/AuthControls";

export const metadata = {
  title: "BrieflyAI — Your Own Summarizer",
  description: "Summarize with Pegasus & BART; Supabase Auth + FastAPI backend.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-800 antialiased min-h-screen flex flex-col">
        <nav className="w-full bg-white/80 backdrop-blur-sm border-b shadow-sm sticky top-0 z-50">
          <div className="max-w-6xl mx-auto flex items-center justify-between px-6 py-3">
            <Link href="/" className="text-lg font-semibold text-blue-600">
              🧠 BrieflyAI
            </Link>
            <div className="flex items-center gap-6 text-sm font-medium">
              <Link href="/" className="hover:text-blue-600">Summarizer</Link>
              <Link href="/history" className="hover:text-blue-600">History</Link>
            </div>
            {/* AuthControls now safely client-side */}
            <AuthControls />
          </div>
        </nav>

        <main className="flex-1">{children}</main>

        <footer className="text-center text-sm text-gray-500 py-4 border-t mt-10">
          FastAPI • Pegasus • BART • Supabase • Redis • Next.js
        </footer>
      </body>
    </html>
  );
}
