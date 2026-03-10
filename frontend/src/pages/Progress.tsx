import { useState, useEffect, useMemo } from 'react';
import { BarChart3, CheckCircle2, Target, Zap, Download } from 'lucide-react';
import StatsCard from '../components/StatsCard';
import ProgressBar from '../components/ProgressBar';
import { SimpleRadarChart, SimplePieChart } from '../components/Charts';
import { useProgress } from '../hooks/useProgress';
import { fetchTasksMeta } from '../utils/api';
import type { TasksMeta } from '../types';

export default function Progress() {
  const { progress, isSolved } = useProgress();
  const [meta, setMeta] = useState<TasksMeta | null>(null);

  useEffect(() => {
    fetchTasksMeta().then(setMeta).catch(console.error);
  }, []);

  const totalTasks = meta?.total ?? 36;
  const categories = meta?.categories ?? {};
  const difficulties = meta?.difficulties ?? {};

  const solvedCount = useMemo(() => progress.filter(p => p.solved).length, [progress]);
  const totalAttempts = useMemo(() => progress.reduce((sum, p) => sum + p.attempts, 0), [progress]);
  const avgMatch = useMemo(() => {
    if (progress.length === 0) return 0;
    return Math.round(progress.reduce((sum, p) => sum + p.best_match_pct, 0) / progress.length);
  }, [progress]);

  const radarData = useMemo(() =>
    Object.entries(categories).map(([cat, taskIds]) => ({
      category: cat.split(' ')[0],
      value: taskIds.filter(id => isSolved(id)).length / taskIds.length * 100,
    })), [categories, isSolved]);

  const pieData = useMemo(() =>
    Object.entries(difficulties).map(([d, taskIds]) => ({
      name: d.charAt(0).toUpperCase() + d.slice(1),
      value: taskIds.filter(id => isSolved(id)).length,
    })), [difficulties, isSolved]);

  const handleExport = () => {
    const data = {
      exported_at: new Date().toISOString(),
      total_tasks: totalTasks,
      solved: solvedCount,
      avg_match: avgMatch,
      total_attempts: totalAttempts,
      progress: progress,
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `sql-trainer-progress-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="p-4 space-y-6 max-w-5xl">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <BarChart3 className="w-6 h-6 text-accent-blue" />
          <h1 className="text-xl font-bold">Progress Dashboard</h1>
        </div>
        <button onClick={handleExport}
          className="flex items-center gap-1.5 px-3 py-1.5 bg-dark-card dark:bg-dark-card bg-gray-100 border border-dark-border dark:border-dark-border border-gray-200 rounded-lg text-xs text-gray-400 hover:bg-dark-hover">
          <Download className="w-3.5 h-3.5" /> Export
        </button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <StatsCard
          label="Solved"
          value={`${solvedCount}/${totalTasks}`}
          icon={<CheckCircle2 className="w-4 h-4 text-accent-green" />}
          color="text-accent-green"
        />
        <StatsCard
          label="Completion"
          value={`${Math.round((solvedCount / totalTasks) * 100)}%`}
          icon={<Target className="w-4 h-4 text-accent-blue" />}
        />
        <StatsCard
          label="Attempts"
          value={totalAttempts}
          icon={<Zap className="w-4 h-4 text-accent-yellow" />}
          color="text-accent-yellow"
        />
        <StatsCard
          label="Avg Match"
          value={`${avgMatch}%`}
          icon={<BarChart3 className="w-4 h-4 text-accent-purple" />}
          color="text-accent-purple"
        />
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        <div className="bg-dark-card dark:bg-dark-card bg-gray-50 border border-dark-border dark:border-dark-border border-gray-200 rounded-lg p-4">
          <h3 className="text-sm font-medium text-gray-400 dark:text-gray-400 text-gray-600 mb-3">Skills Radar</h3>
          {radarData.length > 0 ? (
            <SimpleRadarChart data={radarData} height={280} />
          ) : (
            <div className="h-[280px] flex items-center justify-center text-gray-500 text-sm">Loading...</div>
          )}
        </div>
        <div className="bg-dark-card dark:bg-dark-card bg-gray-50 border border-dark-border dark:border-dark-border border-gray-200 rounded-lg p-4">
          <h3 className="text-sm font-medium text-gray-400 dark:text-gray-400 text-gray-600 mb-3">By Difficulty</h3>
          {pieData.length > 0 ? (
            <SimplePieChart data={pieData} height={280} />
          ) : (
            <div className="h-[280px] flex items-center justify-center text-gray-500 text-sm">Loading...</div>
          )}
        </div>
      </div>

      {Object.keys(categories).length > 0 && (
        <div className="bg-dark-card dark:bg-dark-card bg-gray-50 border border-dark-border dark:border-dark-border border-gray-200 rounded-lg p-4 space-y-3">
          <h3 className="text-sm font-medium text-gray-400 dark:text-gray-400 text-gray-600">Category Progress</h3>
          {Object.entries(categories).map(([cat, taskIds]) => (
            <ProgressBar
              key={cat}
              label={cat}
              value={taskIds.filter(id => isSolved(id)).length}
              max={taskIds.length}
            />
          ))}
        </div>
      )}
    </div>
  );
}
