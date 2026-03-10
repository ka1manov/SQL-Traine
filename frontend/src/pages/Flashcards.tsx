import { useState, useEffect, useContext } from 'react';
import { Brain, ChevronLeft, ChevronRight, RotateCcw, Shuffle } from 'lucide-react';
import { fetchFlashcards, fetchFlashcardProgress, reviewFlashcard } from '../utils/api';
import { AuthContext } from '../contexts/AuthContext';
import type { Flashcard, FlashcardState } from '../types';

export default function Flashcards() {
  const [cards, setCards] = useState<Flashcard[]>([]);
  const [index, setIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [progress, setProgress] = useState<FlashcardState[]>([]);
  const auth = useContext(AuthContext);

  useEffect(() => {
    fetchFlashcards().then(setCards).catch(console.error);
    if (auth?.isLoggedIn) {
      fetchFlashcardProgress().then(setProgress).catch(() => {});
    }
  }, [auth?.isLoggedIn]);

  const handleShuffle = () => {
    const copy = [...cards];
    for (let i = copy.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [copy[i], copy[j]] = [copy[j], copy[i]];
    }
    setCards(copy);
    setIndex(0);
    setFlipped(false);
  };

  const handleReview = async (quality: number) => {
    if (!auth?.isLoggedIn || cards.length === 0) return;
    const card = cards[index];
    try {
      await reviewFlashcard(card.id, quality);
      fetchFlashcardProgress().then(setProgress).catch(() => {});
    } catch {}
    // Move to next card
    if (index < cards.length - 1) {
      setIndex(index + 1);
      setFlipped(false);
    }
  };

  if (cards.length === 0) return <div className="p-4 text-gray-500">Loading flashcards...</div>;

  const card = cards[index];
  const cardProgress = progress.find(p => p.card_id === card.id);
  const learnedCount = progress.filter(p => p.repetitions >= 2).length;

  return (
    <div className="p-4 flex flex-col items-center gap-6 max-w-2xl mx-auto pt-8">
      <div className="flex items-center gap-2">
        <Brain className="w-6 h-6 text-accent-purple" />
        <h1 className="text-xl font-bold">SQL Flashcards</h1>
      </div>

      <div className="flex items-center gap-4 text-sm text-gray-500">
        <span>{index + 1} / {cards.length}</span>
        <span>{learnedCount} learned</span>
      </div>

      <button
        onClick={() => setFlipped(!flipped)}
        className="w-full max-w-lg min-h-[240px] bg-dark-card dark:bg-dark-card bg-gray-50 border border-dark-border dark:border-dark-border border-gray-200 rounded-xl p-8 flex flex-col items-center justify-center gap-4 hover:border-accent-purple/50 transition-colors cursor-pointer"
      >
        <span className="text-xs text-gray-600 uppercase tracking-wider">{flipped ? 'Answer' : 'Question'}</span>
        <p className={`text-center ${flipped ? 'text-accent-green text-sm' : 'text-lg font-medium'}`}>
          {flipped ? card.answer : card.question}
        </p>
        {!flipped && <span className="text-xs text-gray-600 mt-2">Click to reveal answer</span>}
      </button>

      {/* SM-2 quality buttons (shown after flip) */}
      {flipped && auth?.isLoggedIn && (
        <div className="flex gap-2">
          <button onClick={() => handleReview(1)} className="px-4 py-2 bg-red-900/20 border border-red-800 text-red-400 rounded-lg text-sm hover:bg-red-900/40">Again</button>
          <button onClick={() => handleReview(3)} className="px-4 py-2 bg-yellow-900/20 border border-yellow-800 text-yellow-400 rounded-lg text-sm hover:bg-yellow-900/40">Hard</button>
          <button onClick={() => handleReview(4)} className="px-4 py-2 bg-green-900/20 border border-green-800 text-green-400 rounded-lg text-sm hover:bg-green-900/40">Good</button>
          <button onClick={() => handleReview(5)} className="px-4 py-2 bg-blue-900/20 border border-blue-800 text-blue-400 rounded-lg text-sm hover:bg-blue-900/40">Easy</button>
        </div>
      )}

      {cardProgress && (
        <div className="text-xs text-gray-600">
          Reps: {cardProgress.repetitions} | Next review: {cardProgress.interval_days}d | Ease: {cardProgress.ease_factor.toFixed(1)}
        </div>
      )}

      <div className="flex items-center gap-4">
        <button onClick={() => { setIndex(Math.max(0, index - 1)); setFlipped(false); }} disabled={index === 0}
          className="p-2 bg-dark-card border border-dark-border rounded-lg hover:bg-dark-hover disabled:opacity-30"><ChevronLeft className="w-5 h-5" /></button>
        <button onClick={() => setFlipped(false)}
          className="p-2 bg-dark-card border border-dark-border rounded-lg hover:bg-dark-hover"><RotateCcw className="w-5 h-5" /></button>
        <button onClick={handleShuffle}
          className="p-2 bg-dark-card border border-dark-border rounded-lg hover:bg-dark-hover"><Shuffle className="w-5 h-5" /></button>
        <button onClick={() => { setIndex(Math.min(cards.length - 1, index + 1)); setFlipped(false); }} disabled={index === cards.length - 1}
          className="p-2 bg-dark-card border border-dark-border rounded-lg hover:bg-dark-hover disabled:opacity-30"><ChevronRight className="w-5 h-5" /></button>
      </div>

      <span className="text-xs px-2 py-1 bg-dark-card border border-dark-border rounded text-gray-500">{card.category}</span>
    </div>
  );
}
