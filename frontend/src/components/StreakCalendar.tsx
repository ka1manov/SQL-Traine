import { useMemo } from 'react';
import type { StreakData } from '../types';

interface Props {
  data: StreakData;
}

export default function StreakCalendar({ data }: Props) {
  const weeks = useMemo(() => {
    const today = new Date();
    const daysSet = new Set(data.days.map(d => d.date));
    const cells: { date: string; active: boolean }[] = [];

    for (let i = 83; i >= 0; i--) {
      const d = new Date(today);
      d.setDate(d.getDate() - i);
      const iso = d.toISOString().split('T')[0];
      cells.push({ date: iso, active: daysSet.has(iso) });
    }

    const result: typeof cells[] = [];
    for (let i = 0; i < cells.length; i += 7) {
      result.push(cells.slice(i, i + 7));
    }
    return result;
  }, [data.days]);

  return (
    <div className="space-y-2">
      <div className="flex items-center gap-4 text-sm">
        <div>
          <span className="text-2xl font-bold text-accent-yellow">{data.current_streak}</span>
          <span className="text-gray-500 ml-1">day streak</span>
        </div>
        <div>
          <span className="text-lg font-semibold text-gray-400">{data.best_streak}</span>
          <span className="text-gray-500 ml-1">best</span>
        </div>
      </div>
      <div className="flex gap-1">
        {weeks.map((week, wi) => (
          <div key={wi} className="flex flex-col gap-1">
            {week.map((day, di) => (
              <div
                key={di}
                title={day.date}
                className={`w-3 h-3 rounded-sm ${
                  day.active ? 'bg-accent-green' : 'bg-dark-border dark:bg-dark-border bg-gray-200'
                }`}
              />
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}
