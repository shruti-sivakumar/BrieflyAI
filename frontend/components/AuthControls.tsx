"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import { useStore } from "@/lib/store";

export default function AuthControls() {
  const [email, setEmail] = useState("");
  const [userEmail, setUserEmail] = useState<string | null>(null);
  
  // 🔥 Zustand updater
  const setUserId = useStore((s) => s.setUserId);

  useEffect(() => {
    const load = async () => {
      const { data } = await supabase.auth.getUser();
      const uid = data.user?.id ?? null;

      setUserEmail(data.user?.email ?? null);

      // 🔥 Store Supabase UID in global state
      setUserId(uid);
      console.log("ZUSTAND USER ID =", uid);
    };

    load();

    const { data: listener } = supabase.auth.onAuthStateChange(() => load());
    return () => listener.subscription.unsubscribe();
  }, []);

  const signIn = async () => {
    if (!email) return;
    await supabase.auth.signInWithOtp({ email });
    alert("Check your inbox for the login link.");
  };

  const signOut = async () => {
    await supabase.auth.signOut();
    setUserId(null); // important
  };

  return (
    <div className="flex items-center gap-3">
      {userEmail ? (
        <>
          <span className="text-sm text-gray-600">{userEmail}</span>
          <button onClick={signOut} className="text-blue-600 hover:underline text-sm">
            Sign out
          </button>
        </>
      ) : (
        <>
          <input
            type="email"
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="border rounded px-2 py-1 text-sm"
          />
          <button onClick={signIn} className="text-blue-600 hover:underline text-sm">
            Sign in
          </button>
        </>
      )}
    </div>
  );
}
