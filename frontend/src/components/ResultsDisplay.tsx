'use client';

import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface AnalysisResult {
  summary: string;
  classification: string;
  next_steps: string[];
  confidence_score: number;
  processing_time: number | null;
  timestamp: string;
}

interface ResultsDisplayProps {
  result: AnalysisResult;
  fileName: string;
  onReset: () => void;
}

function ConfidenceBar({ confidence }: { confidence: number }) {
  const percentage = Math.round(confidence * 100);
  const color =
    percentage >= 80
      ? 'bg-green-500'
      : percentage >= 60
      ? 'bg-yellow-500'
      : 'bg-red-500';

  return (
    <div className="flex items-center space-x-2">
      <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-500 ${color}`}
          style={{ width: `${percentage}%` }}
        />
      </div>
      <span className="text-sm font-medium text-gray-700">{percentage}%</span>
    </div>
  );
}

export default function ResultsDisplay({
  result,
  fileName,
  onReset,
}: ResultsDisplayProps) {
  const processingTimeMs = result.processing_time
    ? (result.processing_time * 1000).toFixed(0)
    : 'N/A';

  return (
    <div className="space-y-6">
      <div className="card">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold text-gray-900">
              Analysis Results
            </h2>
            <p className="mt-1 text-sm text-gray-500">
              Document: <span className="font-medium">{fileName}</span>
            </p>
          </div>
          <button
            type="button"
            onClick={onReset}
            className="btn-secondary"
          >
            Analyze New Document
          </button>
        </div>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">
          Summary
        </h3>
        <div className="prose prose-sm max-w-none text-gray-700">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {result.summary}
          </ReactMarkdown>
        </div>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">
          Classification
        </h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-700">Category</span>
            <span className="inline-flex items-center rounded-full bg-primary-100 px-3 py-1 text-sm font-medium text-primary-800">
              {result.classification}
            </span>
          </div>
          <div>
            <span className="text-sm font-medium text-gray-700">Confidence</span>
            <ConfidenceBar confidence={result.confidence_score} />
          </div>
        </div>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">
          Recommended Next Steps
        </h3>
        {result.next_steps.length === 0 ? (
          <p className="text-sm text-gray-500">No next steps identified.</p>
        ) : (
          <div className="space-y-4">
            {result.next_steps.map((step, index) => (
              <div
                key={index}
                className="rounded-lg border border-gray-200 p-4"
              >
                <p className="text-sm text-gray-700">{step}</p>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">
          Processing Details
        </h3>
        <dl className="grid grid-cols-2 gap-4 sm:grid-cols-3">
          <div>
            <dt className="text-xs font-medium text-gray-500">
              Processing Time
            </dt>
            <dd className="mt-1 text-sm font-medium text-gray-900">
              {processingTimeMs}ms
            </dd>
          </div>
          <div>
            <dt className="text-xs font-medium text-gray-500">Timestamp</dt>
            <dd className="mt-1 text-sm font-medium text-gray-900">
              {new Date(result.timestamp).toLocaleString()}
            </dd>
          </div>
        </dl>
      </div>
    </div>
  );
}
