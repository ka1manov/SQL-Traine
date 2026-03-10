interface Props {
  label: string;
  value: number;
  max: number;
  color?: string;
}

export default function ProgressBar({ label, value, max, color = 'bg-accent-blue' }: Props) {
  const pct = max > 0 ? Math.round((value / max) * 100) : 0;
  return (
    <div>
      <div className="flex justify-between text-sm mb-1">
        <span className="text-gray-400">{label}</span>
        <span className="text-gray-500">{value}/{max} ({pct}%)</span>
      </div>
      <div className="w-full bg-dark-bg rounded-full h-2.5 overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-500 ${color}`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}
