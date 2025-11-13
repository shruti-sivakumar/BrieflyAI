"use client";

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

export default function SummaryCard({
  title,
  summary,
  model,
  time,
}: {
  title: string;
  summary: string;
  model: string;
  time?: number;
}) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-sm leading-relaxed whitespace-pre-line">{summary}</p>
        <p className="text-xs text-gray-500 mt-2">
          🧩 {model} {time ? `• ${time}s` : ""}
        </p>
      </CardContent>
    </Card>
  );
}