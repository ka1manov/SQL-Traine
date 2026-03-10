interface Props {
  label: string;
  value: string | number;
  icon?: React.ReactNode;
  color?: string;
}

export default function StatsCard({ label, value, icon, color = 'text-accent-blue' }: Props) {
  return (
    <div className="bg-dark-card border border-dark-border rounded-lg p-4">
      <div className="flex items-center gap-2 mb-1">
        {icon}
        <span className="text-xs text-gray-500 uppercase tracking-wider">{label}</span>
      </div>
      <div className={`text-2xl font-bold ${color}`}>{value}</div>
    </div>
  );
}
