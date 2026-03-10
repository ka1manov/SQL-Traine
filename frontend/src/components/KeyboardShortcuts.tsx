import { X } from 'lucide-react';

interface Props {
  open: boolean;
  onClose: () => void;
}

const shortcuts = [
  { keys: ['Ctrl', 'Enter'], action: 'Run query / Check solution' },
  { keys: ['Ctrl', 'Shift', 'F'], action: 'Format SQL' },
  { keys: ['Ctrl', 'S'], action: 'Save to history' },
  { keys: ['Ctrl', '/'], action: 'Toggle comment' },
  { keys: ['Ctrl', 'L'], action: 'Clear editor' },
  { keys: ['Ctrl', 'K'], action: 'Show keyboard shortcuts' },
  { keys: ['Tab'], action: 'Indent / Accept suggestion' },
  { keys: ['Esc'], action: 'Close modal' },
];

export default function KeyboardShortcuts({ open, onClose }: Props) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60" onClick={onClose}>
      <div className="bg-dark-card dark:bg-dark-card bg-white border border-dark-border rounded-xl p-6 w-full max-w-md" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-bold">Keyboard Shortcuts</h2>
          <button onClick={onClose} className="p-1 hover:bg-dark-hover rounded"><X className="w-4 h-4" /></button>
        </div>
        <div className="space-y-2">
          {shortcuts.map((s, i) => (
            <div key={i} className="flex items-center justify-between py-1.5 border-b border-dark-border/50 last:border-0">
              <span className="text-sm text-gray-400">{s.action}</span>
              <div className="flex gap-1">
                {s.keys.map((k, j) => (
                  <kbd key={j} className="px-2 py-0.5 bg-dark-bg dark:bg-dark-bg bg-gray-100 rounded text-xs font-mono text-gray-300 dark:text-gray-300 text-gray-600 border border-dark-border">
                    {navigator.platform.includes('Mac') ? k.replace('Ctrl', '⌘') : k}
                  </kbd>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
