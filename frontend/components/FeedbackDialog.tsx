"use client";

import { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { submitFeedback } from "@/lib/api";

export default function FeedbackDialog({
  summaryId,
  open,
  onClose,
}: {
  summaryId: string;
  open: boolean;
  onClose: () => void;
}) {
  const [selected, setSelected] = useState<"bart" | "pegasus">("bart");
  const [rating, setRating] = useState<number | "">("");
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [done, setDone] = useState(false);

  const handleSubmit = async () => {
    if (!rating) return;
    setLoading(true);
    try {
      await submitFeedback(summaryId, selected, Number(rating), text);
      setDone(true);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent
        className="
          sm:max-w-md w-[90vw]
          bg-white rounded-2xl shadow-lg p-6
          space-y-4
        "
      >
        <DialogHeader>
          <DialogTitle className="text-lg font-semibold">
            📝 Feedback
          </DialogTitle>
        </DialogHeader>

        {done ? (
          <p className="text-green-600 text-sm text-center py-4">
            ✅ Thank you! Your feedback has been recorded.
          </p>
        ) : (
          <div className="space-y-4">
            {/* Model selection */}
            <div className="flex justify-center gap-3">
              <Button
                variant={selected === "bart" ? "default" : "outline"}
                onClick={() => setSelected("bart")}
                className="w-24"
              >
                BART
              </Button>
              <Button
                variant={selected === "pegasus" ? "default" : "outline"}
                onClick={() => setSelected("pegasus")}
                className="w-24"
              >
                Pegasus
              </Button>
            </div>

            {/* Rating */}
            <div>
              <label className="block text-sm font-medium mb-1">
                Rating (1–5)
              </label>
              <Input
                type="number"
                min={1}
                max={5}
                value={rating}
                onChange={(e) => setRating(e.target.valueAsNumber || "")}
                className="w-full"
              />
            </div>

            {/* Text feedback */}
            <div>
              <label className="block text-sm font-medium mb-1">
                Comments (optional)
              </label>
              <Textarea
                placeholder="What did you think of the summaries?"
                value={text}
                onChange={(e) => setText(e.target.value)}
                className="min-h-[100px]"
              />
            </div>

            {/* Actions */}
            <div className="flex justify-end gap-3 pt-2">
              <Button variant="outline" onClick={onClose}>
                Cancel
              </Button>
              <Button
                onClick={handleSubmit}
                disabled={loading || !rating}
                className="bg-blue-600 hover:bg-blue-700 text-white"
              >
                {loading ? "Submitting..." : "Submit"}
              </Button>
            </div>
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}
