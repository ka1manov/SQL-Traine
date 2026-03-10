import { CheckCircle2 } from 'lucide-react';
import Badge from './Badge';
import type { Task } from '../types';

interface Props {
  task: Task;
  solved?: boolean;
  onClick: () => void;
}

export default function TaskCard({ task, solved, onClick }: Props) {
  return (
    <button
      onClick={onClick}
      className="w-full text-left p-4 bg-white dark:bg-dark-card hover:bg-gray-50 dark:hover:bg-dark-hover border border-gray-200 dark:border-dark-border rounded-lg transition-colors"
    >
      <div className="flex items-start justify-between gap-2">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs text-gray-500">#{task.id}</span>
            <h3 className="font-medium text-sm truncate">{task.title}</h3>
            {solved && <CheckCircle2 className="w-4 h-4 text-accent-green shrink-0" />}
          </div>
          <p className="text-xs text-gray-500 line-clamp-2">{task.description}</p>
        </div>
        <div className="flex flex-col items-end gap-1 shrink-0">
          <Badge text={task.difficulty} />
          <span className="text-xs text-gray-500 dark:text-gray-600">{task.category}</span>
        </div>
      </div>
    </button>
  );
}
