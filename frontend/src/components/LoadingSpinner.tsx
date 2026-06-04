'use client';

import { useState, useEffect } from 'react';

interface LoadingSpinnerProps {
  message?: string;
  steps?: string[];
}

export default function LoadingSpinner({
  message = 'Processing...',
  steps = [],
}: LoadingSpinnerProps) {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);

  useEffect(() => {
    if (steps.length === 0) return;

    const interval = setInterval(() => {
      setCurrentStepIndex((prev) => (prev + 1) % steps.length);
    }, 2000);

    return () => clearInterval(interval);
  }, [steps.length]);

  return (
    <div className="flex flex-col items-center justify-center py-8">
      <div className="relative">
        <div className="h-16 w-16">
          <div className="absolute inset-0 rounded-full border-4 border-gray-200" />
          <div className="absolute inset-0 rounded-full border-4 border-primary-600 border-t-transparent animate-spin" />
        </div>
      </div>
      <p className="mt-4 text-sm font-medium text-gray-700">{message}</p>
      {steps.length > 0 && (
        <div className="mt-4 space-y-2">
          {steps.map((step, index) => (
            <div key={index} className="flex items-center space-x-2">
              <div
                className={`h-2 w-2 rounded-full transition-colors duration-300 ${
                  index === currentStepIndex
                    ? 'bg-primary-600'
                    : index < currentStepIndex
                    ? 'bg-green-500'
                    : 'bg-gray-300'
                }`}
              />
              <span
                className={`text-sm ${
                  index === currentStepIndex
                    ? 'text-gray-900 font-medium'
                    : 'text-gray-500'
                }`}
              >
                {step}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
