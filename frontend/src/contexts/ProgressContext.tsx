import React, { createContext, useState, useEffect, useCallback, useContext } from 'react';
import type { ProgressEntry } from '../types';
import { fetchProgress, updateProgress as apiUpdateProgress } from '../utils/api';
import { AuthContext } from './AuthContext';

interface ProgressContextType {
  progress: ProgressEntry[];
  refresh: () => Promise<void>;
  recordAttempt: (taskId: number, matchPct: number, solved: boolean) => Promise<void>;
  isSolved: (taskId: number) => boolean;
  getAttempts: (taskId: number) => number;
}

export const ProgressContext = createContext<ProgressContextType | null>(null);

export function ProgressProvider({ children }: { children: React.ReactNode }) {
  const [progress, setProgress] = useState<ProgressEntry[]>([]);
  const auth = useContext(AuthContext);

  const refresh = useCallback(async () => {
    if (!auth?.isLoggedIn) {
      setProgress([]);
      return;
    }
    try {
      const data = await fetchProgress();
      setProgress(data);
    } catch (err) {
      console.error('Failed to fetch progress:', err);
    }
  }, [auth?.isLoggedIn]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const recordAttempt = useCallback(async (taskId: number, matchPct: number, solved: boolean) => {
    if (!auth?.isLoggedIn) return;
    try {
      await apiUpdateProgress({
        task_id: taskId,
        solved,
        best_match_pct: matchPct,
        attempts: 1,
      });
      await refresh();
    } catch (err) {
      console.error('Failed to record attempt:', err);
    }
  }, [refresh, auth?.isLoggedIn]);

  const isSolved = useCallback((taskId: number) => {
    return progress.some(p => p.task_id === taskId && p.solved);
  }, [progress]);

  const getAttempts = useCallback((taskId: number) => {
    return progress.find(p => p.task_id === taskId)?.attempts ?? 0;
  }, [progress]);

  return (
    <ProgressContext.Provider value={{ progress, refresh, recordAttempt, isSolved, getAttempts }}>
      {children}
    </ProgressContext.Provider>
  );
}
