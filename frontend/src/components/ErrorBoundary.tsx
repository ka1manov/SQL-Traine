import React from 'react';

interface State {
  hasError: boolean;
  error: Error | null;
}

export default class ErrorBoundary extends React.Component<{ children: React.ReactNode }, State> {
  state: State = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex flex-col items-center justify-center h-full gap-4 p-8">
          <h2 className="text-xl font-bold text-accent-red">Something went wrong</h2>
          <p className="text-sm text-gray-500 dark:text-gray-400">{this.state.error?.message}</p>
          <button
            onClick={() => {
              this.setState({ hasError: false, error: null });
              window.location.href = '/';
            }}
            className="px-4 py-2 bg-accent-blue hover:bg-blue-600 rounded-lg text-sm text-white"
          >
            Go Home
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}
