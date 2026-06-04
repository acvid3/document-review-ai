'use client';

import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import DocumentUpload from '@/components/DocumentUpload';
import ResultsDisplay from '@/components/ResultsDisplay';
import LoadingSpinner from '@/components/LoadingSpinner';
import ErrorAlert from '@/components/ErrorAlert';

interface AnalysisResult {
  summary: string;
  classification: string;
  next_steps: string[];
  confidence_score: number;
  processing_time: number | null;
  timestamp: string;
}

export default function Home() {
  const [documentText, setDocumentText] = useState<string>('');
  const [fileName, setFileName] = useState<string>('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleTextSubmit = useCallback(async (text: string, name: string) => {
    setIsProcessing(true);
    setError(null);
    setResult(null);
    setDocumentText(text);
    setFileName(name);

    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text,
          filename: name,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        throw new Error(
          errorData?.detail || `Server error: ${response.status} ${response.statusText}`
        );
      }

      const data: AnalysisResult = await response.json();
      setResult(data);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : 'An unexpected error occurred'
      );
    } finally {
      setIsProcessing(false);
    }
  }, []);

  const handleReset = useCallback(() => {
    setDocumentText('');
    setFileName('');
    setResult(null);
    setError(null);
  }, []);

  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      <div className="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8">
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            Document Review AI
          </h1>
          <p className="mt-2 text-lg text-gray-600">
            Proof of Concept — Evaluate AI-assisted document review workflow
          </p>
        </div>

        <div className="space-y-6">
          {!result && (
            <div className="card">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Upload Document
              </h2>
              <DocumentUpload
                onSubmit={handleTextSubmit}
                isProcessing={isProcessing}
              />
            </div>
          )}

          {isProcessing && (
            <div className="card">
              <LoadingSpinner
                message="Analyzing document with AI..."
                steps={[
                  'Extracting text content',
                  'Generating summary',
                  'Classifying document',
                  'Determining next steps',
                ]}
              />
            </div>
          )}

          {error && (
            <ErrorAlert
              message={error}
              onRetry={() => handleTextSubmit(documentText, fileName)}
              onDismiss={handleReset}
            />
          )}

          {result && !isProcessing && (
            <ResultsDisplay
              result={result}
              fileName={fileName}
              onReset={handleReset}
            />
          )}

          <div className="text-center text-sm text-gray-500">
            <p>
              This is a proof-of-concept prototype. Results should be reviewed
              by a human before taking action.
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}
