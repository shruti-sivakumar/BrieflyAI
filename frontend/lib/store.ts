import { create } from "zustand";
import type { SummaryResult } from "./api";

interface AppState {
  userId: string | null;
  summary: SummaryResult | null;
  loading: boolean;
  error: string | null;

  setUserId: (id: string | null) => void;
  setLoading: (value: boolean) => void;
  setSummary: (data: SummaryResult | null) => void;
  setError: (msg: string | null) => void;
}

export const useStore = create<AppState>((set) => ({
  userId: null,
  summary: null,
  loading: false,
  error: null,

  setUserId: (id) => set({ userId: id }),
  setLoading: (value) => set({ loading: value }),
  setSummary: (data) => set({ summary: data }),
  setError: (msg) => set({ error: msg }),
}));
