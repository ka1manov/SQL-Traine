import { lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import { ProgressProvider } from './contexts/ProgressContext';
import { AuthProvider } from './contexts/AuthContext';
import { ThemeProvider } from './contexts/ThemeContext';
import ErrorBoundary from './components/ErrorBoundary';

const Sandbox = lazy(() => import('./pages/Sandbox'));
const Tasks = lazy(() => import('./pages/Tasks'));
const DailyChallenge = lazy(() => import('./pages/DailyChallenge'));
const Learn = lazy(() => import('./pages/Learn'));
const Flashcards = lazy(() => import('./pages/Flashcards'));
const Explorer = lazy(() => import('./pages/Explorer'));
const MockInterview = lazy(() => import('./pages/MockInterview'));
const EDA = lazy(() => import('./pages/EDA'));
const TakeHome = lazy(() => import('./pages/TakeHome'));
const Progress = lazy(() => import('./pages/Progress'));
const Leaderboard = lazy(() => import('./pages/Leaderboard'));

function Loading() {
  return (
    <div className="flex items-center justify-center h-full">
      <div className="animate-spin w-8 h-8 border-2 border-accent-blue border-t-transparent rounded-full" />
    </div>
  );
}

export default function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <ThemeProvider>
          <AuthProvider>
            <ProgressProvider>
              <Routes>
                <Route element={<Layout />}>
                  <Route path="/" element={<Suspense fallback={<Loading />}><Sandbox /></Suspense>} />
                  <Route path="/tasks" element={<Suspense fallback={<Loading />}><Tasks /></Suspense>} />
                  <Route path="/daily" element={<Suspense fallback={<Loading />}><DailyChallenge /></Suspense>} />
                  <Route path="/learn" element={<Suspense fallback={<Loading />}><Learn /></Suspense>} />
                  <Route path="/flashcards" element={<Suspense fallback={<Loading />}><Flashcards /></Suspense>} />
                  <Route path="/explorer" element={<Suspense fallback={<Loading />}><Explorer /></Suspense>} />
                  <Route path="/mock" element={<Suspense fallback={<Loading />}><MockInterview /></Suspense>} />
                  <Route path="/eda" element={<Suspense fallback={<Loading />}><EDA /></Suspense>} />
                  <Route path="/take-home" element={<Suspense fallback={<Loading />}><TakeHome /></Suspense>} />
                  <Route path="/progress" element={<Suspense fallback={<Loading />}><Progress /></Suspense>} />
                  <Route path="/leaderboard" element={<Suspense fallback={<Loading />}><Leaderboard /></Suspense>} />
                </Route>
              </Routes>
            </ProgressProvider>
          </AuthProvider>
        </ThemeProvider>
      </BrowserRouter>
    </ErrorBoundary>
  );
}
