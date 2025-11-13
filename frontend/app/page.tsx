"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Progress } from "@/components/ui/progress";
import { useStore } from "@/lib/store";
import { summarizeText, summarizeURL, summarizeFile } from "@/lib/api";
import FeedbackDialog from "@/components/FeedbackDialog";
import SummaryCard from "@/components/SummaryCard";

export default function HomePage() {
  const { summary, loading, error, setLoading, setSummary, setError } = useStore();
  const [text, setText] = useState("");
  const [url, setUrl] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [tab, setTab] = useState("text");
  const [showFeedback, setShowFeedback] = useState(false);

  const handleSummarize = async () => {
    try {
      setError(null);
      setLoading(true);

      let result;

      if (tab === "text") {
        if (text.trim().split(" ").length < 30) {
          setError("Please enter at least 30 words.");
          return;
        }
        result = await summarizeText(text);
      }

      if (tab === "url") {
        if (!url.startsWith("http")) {
          setError("Enter a valid URL starting with http or https.");
          return;
        }
        result = await summarizeURL(url);
      }

      if (tab === "file" && file) {
        result = await summarizeFile(file);
      }

      setSummary(result ?? null);
    } catch (err) {
      console.error(err);
      setError("Something went wrong while summarizing.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-start p-6">
      <div className="w-full max-w-3xl space-y-6 mt-10">
        <Card>
          <CardHeader>
            <CardTitle className="text-xl font-semibold">
              🧠 BrieflyAI — Your Very Own Summarizer
            </CardTitle>
          </CardHeader>

          <CardContent className="space-y-4">
            <Tabs defaultValue="text" value={tab} onValueChange={setTab}>
              <TabsList className="grid w-full grid-cols-3">
                <TabsTrigger value="text">Text</TabsTrigger>
                <TabsTrigger value="url">URL</TabsTrigger>
                <TabsTrigger value="file">File</TabsTrigger>
              </TabsList>

              <TabsContent value="text">
                <Textarea
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  placeholder="Paste or type your article text here..."
                  className="min-h-[150px]"
                />
              </TabsContent>

              <TabsContent value="url">
                <Input
                  type="url"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="https://example.com/article"
                />
              </TabsContent>

              <TabsContent value="file">
                <Input
                  type="file"
                  accept=".txt,.pdf,.docx"
                  onChange={(e) => setFile(e.target.files?.[0] || null)}
                />
                {file && <p className="text-sm text-gray-500 mt-2">Selected: {file.name}</p>}
              </TabsContent>
            </Tabs>

            <Button onClick={handleSummarize} disabled={loading} className="w-full">
              {loading ? "Summarizing..." : "Summarize"}
            </Button>

            {loading && <Progress value={70} className="h-2 bg-blue-200" />}
            {error && <p className="text-red-500 text-sm mt-2">{error}</p>}
          </CardContent>
        </Card>

        {summary && (
          <>
            <div className="grid md:grid-cols-2 gap-4">
              <SummaryCard
                title="BART Summary"
                summary={summary.bart.summary}
                model={summary.bart.model}
                />
                <SummaryCard
                title="Pegasus Summary"
                summary={summary.pegasus.summary}
                model={summary.pegasus.model}
            />
            </div>

            <Button
              onClick={() => setShowFeedback(true)}
              className="w-full bg-green-600 hover:bg-green-700 text-white"
            >
              Give Feedback
            </Button>

            {showFeedback && (
              <FeedbackDialog
                summaryId={summary.summary_id || ""}
                open={true}
                onClose={() => setShowFeedback(false)}
              />
            )}
          </>
        )}
      </div>
    </main>
  );
}