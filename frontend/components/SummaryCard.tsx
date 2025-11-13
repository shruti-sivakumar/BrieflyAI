"use client";

import { useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Download, Copy, ChevronDown, ChevronUp } from "lucide-react";

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
  const [expanded, setExpanded] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(summary);
    alert("Copied to clipboard!");
  };

  const handleDownload = () => {
    const blob = new Blob([summary], { type: "text/plain" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = `${model.replace(" ", "_")}_summary.txt`;
    a.click();

    URL.revokeObjectURL(url);
  };

  const isLong = summary.length > 350;
  const displayText = expanded ? summary : summary.slice(0, 350) + (isLong ? "..." : "");

  return (
    <Card>
      <CardHeader className="flex justify-between items-center">
        <CardTitle className="text-base font-semibold">{title}</CardTitle>
      </CardHeader>

      <CardContent className="space-y-3">
        <p className="text-sm leading-relaxed whitespace-pre-line">
          {displayText}
        </p>

        {/* Expand/Collapse */}
        {isLong && (
          <button
            onClick={() => setExpanded((v) => !v)}
            className="flex items-center gap-1 text-blue-600 text-xs"
          >
            {expanded ? (
              <>
                Show Less <ChevronUp size={14} />
              </>
            ) : (
              <>
                Show More <ChevronDown size={14} />
              </>
            )}
          </button>
        )}

        {/* Controls */}
        <div className="flex justify-between pt-2 border-t mt-3">
          <p className="text-xs text-gray-500">
            🧩 {model} {time ? `• ${time}s` : ""}
          </p>

          <div className="flex gap-2">
            <Button size="sm" variant="outline" onClick={handleCopy}>
              <Copy size={14} className="mr-1" /> Copy
            </Button>
            <Button size="sm" variant="outline" onClick={handleDownload}>
              <Download size={14} className="mr-1" /> Save
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
