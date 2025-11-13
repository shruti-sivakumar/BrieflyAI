"use client";

import { useEffect, useState } from "react";
import { getMySummaries } from "@/lib/api";
import { useStore } from "@/lib/store";
import SummaryCard from "@/components/SummaryCard";
import FeedbackDialog from "@/components/FeedbackDialog";
import { Button } from "@/components/ui/button";

export default function HistoryPage() {
  const { userId } = useStore();
  const [summaries, setSummaries] = useState<any[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);

  useEffect(() => {
    if (!userId) return;

    const fetchSummaries = async () => {
      const res = await getMySummaries(userId);
      setSummaries(res.summaries);
    };

    fetchSummaries();
  }, [userId]);

  return (
    <main className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-2xl font-semibold mb-6">📜 Your Summaries</h1>

        {summaries.length === 0 && (
          <p className="text-gray-500">No summaries yet. Try the main page!</p>
        )}

        <div className="space-y-4">
          {summaries.map((s) => (
            <div key={s.id} className="border rounded-lg p-4 bg-white shadow-sm">
              <div className="flex justify-between items-center">
                <h2 className="font-medium text-gray-700 text-sm">
                  {s.source_type.toUpperCase()} — {s.created_at?.slice(0, 10)}
                </h2>
                <Button size="sm" onClick={() => setSelectedId(s.id)}>
                  Feedback
                </Button>
              </div>

              <div className="grid md:grid-cols-2 gap-4 mt-3">
                <SummaryCard
                  title="BART Summary"
                  summary={s.bart_summary}
                  model="BART-large-CNN"
                />
                <SummaryCard
                  title="Pegasus Summary"
                  summary={s.pegasus_summary}
                  model="Pegasus-XSum"
                />
              </div>
            </div>
          ))}
        </div>

        {selectedId && (
          <FeedbackDialog summaryId={selectedId} open={true} onClose={() => setSelectedId(null)} />
        )}
      </div>
    </main>
  );
}
