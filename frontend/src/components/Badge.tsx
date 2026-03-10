const colorMap: Record<string, string> = {
  easy: 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 border-green-200 dark:border-green-800',
  medium: 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400 border-yellow-200 dark:border-yellow-800',
  hard: 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 border-red-200 dark:border-red-800',
  expert: 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400 border-purple-200 dark:border-purple-800',
};

interface Props {
  text: string;
  variant?: string;
}

export default function Badge({ text, variant }: Props) {
  const colors = colorMap[variant || text.toLowerCase()] || 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 border-gray-200 dark:border-gray-700';
  return (
    <span className={`px-2 py-0.5 text-xs rounded-full border ${colors}`}>
      {text}
    </span>
  );
}
