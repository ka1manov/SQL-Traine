interface Props {
  categories: string[];
  selectedCategory: string;
  selectedDifficulty: string;
  onCategoryChange: (c: string) => void;
  onDifficultyChange: (d: string) => void;
}

const difficulties = ['', 'easy', 'medium', 'hard', 'expert'];

export default function TaskFilters({
  categories, selectedCategory, selectedDifficulty,
  onCategoryChange, onDifficultyChange,
}: Props) {
  return (
    <div className="flex gap-3 flex-wrap">
      <select
        value={selectedCategory}
        onChange={e => onCategoryChange(e.target.value)}
        className="bg-dark-card border border-dark-border rounded-lg px-3 py-1.5 text-sm text-gray-300 focus:outline-none focus:border-accent-blue"
      >
        <option value="">All Categories</option>
        {categories.map(c => (
          <option key={c} value={c}>{c}</option>
        ))}
      </select>
      <select
        value={selectedDifficulty}
        onChange={e => onDifficultyChange(e.target.value)}
        className="bg-dark-card border border-dark-border rounded-lg px-3 py-1.5 text-sm text-gray-300 focus:outline-none focus:border-accent-blue"
      >
        {difficulties.map(d => (
          <option key={d} value={d}>{d || 'All Difficulties'}</option>
        ))}
      </select>
    </div>
  );
}
