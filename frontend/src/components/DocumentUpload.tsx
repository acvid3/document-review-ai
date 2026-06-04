'use client';

import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

interface DocumentUploadProps {
  onSubmit: (text: string, fileName: string) => void;
  isProcessing: boolean;
}

export default function DocumentUpload({
  onSubmit,
  isProcessing,
}: DocumentUploadProps) {
  const [textInput, setTextInput] = useState('');
  const [fileName, setFileName] = useState<string | null>(null);
  const [fileContent, setFileContent] = useState<string | null>(null);
  const [inputMode, setInputMode] = useState<'paste' | 'upload'>('paste');

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      const file = acceptedFiles[0];
      if (!file) return;

      setFileName(file.name);

      const reader = new FileReader();
      reader.onload = (event) => {
        const content = event.target?.result as string;
        setFileContent(content);
      };
      reader.readAsText(file);
    },
    []
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/plain': ['.txt'],
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': [
        '.docx',
      ],
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024,
    disabled: isProcessing,
  });

  const handleSubmit = () => {
    const text = inputMode === 'paste' ? textInput : fileContent;
    const name =
      inputMode === 'paste'
        ? 'Pasted Text'
        : fileName || 'Uploaded Document';

    if (!text || text.trim().length === 0) return;

    onSubmit(text, name);
  };

  const canSubmit =
    (inputMode === 'paste' && textInput.trim().length > 0) ||
    (inputMode === 'upload' && fileContent !== null);

  return (
    <div className="space-y-4">
      <div className="flex space-x-2">
        <button
          type="button"
          onClick={() => setInputMode('paste')}
          className={`rounded-md px-4 py-2 text-sm font-medium transition-colors ${
            inputMode === 'paste'
              ? 'bg-primary-600 text-white'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
          disabled={isProcessing}
        >
          Paste Text
        </button>
        <button
          type="button"
          onClick={() => setInputMode('upload')}
          className={`rounded-md px-4 py-2 text-sm font-medium transition-colors ${
            inputMode === 'upload'
              ? 'bg-primary-600 text-white'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
          disabled={isProcessing}
        >
          Upload File
        </button>
      </div>

      {inputMode === 'paste' ? (
        <div>
          <label htmlFor="text-input" className="label">
            Document Text
          </label>
          <textarea
            id="text-input"
            rows={10}
            className="input-field resize-y"
            placeholder="Paste your document text here..."
            value={textInput}
            onChange={(e) => setTextInput(e.target.value)}
            disabled={isProcessing}
          />
          <p className="mt-1 text-xs text-gray-500">
            {textInput.length} characters
          </p>
        </div>
      ) : (
        <div>
          <label className="label">Upload Document</label>
          <div
            {...getRootProps()}
            className={`mt-1 flex justify-center rounded-lg border-2 border-dashed px-6 py-10 transition-colors ${
              isDragActive
                ? 'border-primary-500 bg-primary-50'
                : 'border-gray-300 hover:border-gray-400'
            } ${isProcessing ? 'cursor-not-allowed opacity-50' : 'cursor-pointer'}`}
          >
            <input {...getInputProps()} />
            <div className="text-center">
              <svg
                className="mx-auto h-12 w-12 text-gray-400"
                stroke="currentColor"
                fill="none"
                viewBox="0 0 48 48"
                aria-hidden="true"
              >
                <path
                  d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                  strokeWidth={2}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
              <div className="mt-4 flex text-sm text-gray-600">
                <span className="relative rounded-md bg-white font-medium text-primary-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-primary-500 focus-within:ring-offset-2 hover:text-primary-500">
                  Upload a file
                </span>
                <p className="pl-1">or drag and drop</p>
              </div>
              <p className="text-xs text-gray-500">
                TXT, PDF, DOC, DOCX up to 10MB
              </p>
            </div>
          </div>
          {fileName && (
            <p className="mt-2 text-sm text-gray-600">
              Selected: <span className="font-medium">{fileName}</span>
            </p>
          )}
        </div>
      )}

      <div className="flex justify-end">
        <button
          type="button"
          onClick={handleSubmit}
          disabled={!canSubmit || isProcessing}
          className="btn-primary"
        >
          {isProcessing ? (
            <>
              <svg
                className="-ml-1 mr-2 h-4 w-4 animate-spin"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
              Processing...
            </>
          ) : (
            'Analyze Document'
          )}
        </button>
      </div>
    </div>
  );
}
