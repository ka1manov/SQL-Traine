const colorMap: Record<string, string> = {
  easy: 'bg-green-900/30 text-green-400 border-green-800',
  medium: 'bg-yellow-900/30 text-yellow-400 border-yellow-800',
  hard: 'bg-red-900/30 text-red-400 border-red-800',
  expert: 'bg-purple-900/30 text-purple-400 border-purple-800',
};

interface Props {
  text: string;
  variant?: string;
}

export default function Badge({ text, variant }: Props) {
  const colors = colorMap[variant || text.toLowerCase()] || 'bg-gray-800 text-gray-400 border-gray-700';
  return (
    <span className={`px-2 py-0.5 text-xs rounded-full border ${colors}`}>
      {text}
    </span>
  );
}
