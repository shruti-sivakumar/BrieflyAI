import axios from "axios";
import { supabase } from "./supabase";
import { useStore } from "./store";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api";

const api = axios.create({
  baseURL: API_URL
});

async function authHeader() {
  const { data } = await supabase.auth.getSession();
  const token = data.session?.access_token;
  return token ? { Authorization: `Bearer ${token}` } : {};
}

/* ===== Types ===== */
export interface SummaryModel {
  model: string;
  summary: string;
  processing_time: number;
}
export interface SummaryResult {
  original_length: number;
  bart: SummaryModel;
  pegasus: SummaryModel;
  summary_id?: string;
  filename?: string;
}
export interface UserSummariesResponse {
  user_id: string;
  count: number;
  summaries: any[];
}

/* ===== API calls (WITH user_id FIXED) ===== */
export const summarizeText = async (text: string): Promise<SummaryResult> => {
  const headers = await authHeader();
  const userId = useStore.getState().userId;

  const res = await api.post(
    "/summarize/text",
    { text, user_id: userId },
    { headers }
  );

  return res.data;
};

export const summarizeURL = async (url: string): Promise<SummaryResult> => {
  const headers = await authHeader();
  const userId = useStore.getState().userId;

  const res = await api.post(
    "/summarize/url",
    { url, user_id: userId },
    { headers }
  );

  return res.data;
};

export const summarizeFile = async (file: File): Promise<SummaryResult> => {
  const headers = await authHeader();
  const userId = useStore.getState().userId;

  const fd = new FormData();
  fd.append("file", file);
  fd.append("user_id", userId || "");

  const res = await api.post("/summarize/file", fd, {
    headers: { ...headers, "Content-Type": "multipart/form-data" },
  });

  return res.data;
};

export const getMySummaries = async (userId: string, skip = 0, limit = 20) => {
  if (!userId) return { count: 0, summaries: [] };

  const headers = await authHeader();

  const res = await api.get(`/summaries/${userId}`, {
    headers,
    params: { skip, limit }
  });

  return res.data;
};

export const submitFeedback = async (
  summaryId: string,
  selectedModel: "bart" | "pegasus",
  rating?: number,
  feedbackText?: string
) => {
  const headers = await authHeader();
  const params = new URLSearchParams();
  params.append("selected_model", selectedModel);
  if (rating) params.append("rating", String(rating));
  if (feedbackText) params.append("feedback_text", feedbackText);

  const res = await api.post(
    `/summaries/${summaryId}/feedback?${params.toString()}`,
    null,
    { headers }
  );

  return res.data;
};