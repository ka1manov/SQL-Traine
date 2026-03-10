import { useState, useEffect } from 'react';
import {
  BookOpen, ChevronRight, Code2, Lightbulb, Brain,
  Play, AlertTriangle, ArrowLeft, ChevronDown, CheckCircle2, BarChart3,
} from 'lucide-react';
import { fetchLearningPaths } from '../utils/api';
import { useProgress } from '../hooks/useProgress';
import type { LearningPath, PathStep } from '../types';

/* ------------------------------------------------------------------ */
/*  Lesson Detail View                                                 */
/* ------------------------------------------------------------------ */

function LessonView({
  path,
  stepIdx,
  setStepIdx,
  onBack,
  isSolved,
}: {
  path: LearningPath;
  stepIdx: number;
  setStepIdx: (i: number) => void;
  onBack: () => void;
  isSolved: (id: number) => boolean;
}) {
  const step: PathStep = path.steps[stepIdx];
  const [revealedQuiz, setRevealedQuiz] = useState<Set<string>>(new Set());

  const toggleQuiz = (key: string) =>
    setRevealedQuiz(prev => {
      const next = new Set(prev);
      next.has(key) ? next.delete(key) : next.add(key);
      return next;
    });

  // Reset revealed quizzes when step changes
  useEffect(() => setRevealedQuiz(new Set()), [stepIdx]);

  return (
    <div className="p-4 space-y-6 max-w-4xl">
      {/* Back button */}
      <button
        onClick={onBack}
        className="flex items-center gap-1 text-sm text-gray-400 hover:text-gray-200 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" /> Back to learning paths
      </button>

      {/* Title */}
      <div>
        <h1 className="text-xl font-bold">{path.title}</h1>
        <p className="text-sm text-gray-500">{path.description}</p>
      </div>

      {/* Step tabs */}
      <div className="flex gap-2 flex-wrap">
        {path.steps.map((s, i) => (
          <button
            key={i}
            onClick={() => setStepIdx(i)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              stepIdx === i
                ? 'bg-accent-blue text-white'
                : 'bg-dark-card dark:bg-dark-card bg-gray-50 border border-dark-border dark:border-dark-border border-gray-200 text-gray-400 hover:bg-dark-hover dark:hover:bg-dark-hover hover:bg-gray-100'
            }`}
          >
            {s.title}
          </button>
        ))}
      </div>

      {/* Section: Theory */}
      {step.theory && (
        <section className="space-y-3">
          <h2 className="flex items-center gap-2 text-lg font-semibold">
            <BookOpen className="w-5 h-5 text-accent-blue" /> Theory
          </h2>
          <div className="space-y-3 text-sm leading-relaxed text-gray-300 dark:text-gray-300 text-gray-700">
            {step.theory.split('\n\n').map((para, i) => (
              <p key={i}>{para}</p>
            ))}
          </div>
        </section>
      )}

      {/* Section: Key Points */}
      {step.key_points.length > 0 && (
        <section className="rounded-lg border border-blue-800/40 dark:border-blue-800/40 border-blue-200 bg-blue-950/20 dark:bg-blue-950/20 bg-blue-50 p-4 space-y-2">
          <h2 className="flex items-center gap-2 text-base font-semibold text-blue-400 dark:text-blue-400 text-blue-700">
            <Lightbulb className="w-5 h-5" /> Key Points
          </h2>
          <ul className="space-y-1.5 text-sm">
            {step.key_points.map((kp, i) => (
              <li key={i} className="flex items-start gap-2">
                <span className="text-blue-400 dark:text-blue-400 text-blue-600 mt-0.5 shrink-0">•</span>
                <span className="text-gray-300 dark:text-gray-300 text-gray-700">{kp}</span>
              </li>
            ))}
          </ul>
        </section>
      )}

      {/* Section: Syntax */}
      {step.syntax && (
        <section className="space-y-2">
          <h2 className="flex items-center gap-2 text-base font-semibold">
            <Code2 className="w-5 h-5 text-accent-blue" /> Syntax
          </h2>
          <pre className="bg-dark-bg dark:bg-dark-bg bg-gray-100 rounded-lg p-4 text-sm font-mono text-accent-blue overflow-x-auto">
            {step.syntax}
          </pre>
        </section>
      )}

      {/* Section: Examples */}
      {step.examples.length > 0 && (
        <section className="space-y-4">
          <h2 className="flex items-center gap-2 text-base font-semibold">
            <Code2 className="w-5 h-5 text-green-400" /> Examples
          </h2>
          {step.examples.map((ex, i) => (
            <div
              key={i}
              className="bg-dark-card dark:bg-dark-card bg-gray-50 border border-dark-border dark:border-dark-border border-gray-200 rounded-lg p-4 space-y-2"
            >
              <h3 className="text-sm font-semibold">{ex.title}</h3>
              <pre className="bg-dark-bg dark:bg-dark-bg bg-gray-100 rounded p-3 text-xs font-mono text-accent-blue overflow-x-auto">
                {ex.sql}
              </pre>
              <p className="text-xs text-gray-400 dark:text-gray-400 text-gray-600 leading-relaxed">
                {ex.explanation}
              </p>
            </div>
          ))}
        </section>
      )}

      {/* Section: Quiz */}
      {step.quiz.length > 0 && (
        <section className="space-y-3">
          <h2 className="flex items-center gap-2 text-base font-semibold">
            <Brain className="w-5 h-5 text-purple-400" /> Knowledge Check
          </h2>
          {step.quiz.map((q, qi) => {
            const key = `${stepIdx}-${qi}`;
            const revealed = revealedQuiz.has(key);
            return (
              <div
                key={qi}
                className="bg-dark-card dark:bg-dark-card bg-gray-50 border border-dark-border dark:border-dark-border border-gray-200 rounded-lg p-4 space-y-2"
              >
                <p className="text-sm font-medium">{q.question}</p>
                <button
                  onClick={() => toggleQuiz(key)}
                  className="flex items-center gap-1 text-xs text-purple-400 hover:text-purple-300 transition-colors"
                >
                  <ChevronDown className={`w-3.5 h-3.5 transition-transform ${revealed ? 'rotate-180' : ''}`} />
                  {revealed ? 'Hide Answer' : 'Reveal Answer'}
                </button>
                {revealed && (
                  <div className="text-sm text-gray-300 dark:text-gray-300 text-gray-700 bg-dark-bg dark:bg-dark-bg bg-gray-100 rounded p-3 leading-relaxed">
                    {q.answer}
                  </div>
                )}
              </div>
            );
          })}
        </section>
      )}

      {/* Section: Practice Tasks */}
      {step.task_ids.length > 0 && (
        <section className="space-y-2">
          <h2 className="flex items-center gap-2 text-base font-semibold">
            <Play className="w-5 h-5 text-accent-green" /> Practice Tasks
          </h2>
          <div className="flex gap-2 flex-wrap">
            {step.task_ids.map(id => (
              <a
                key={id}
                href={`/tasks?id=${id}`}
                className={`text-xs px-2.5 py-1 rounded-md font-medium transition-colors ${
                  isSolved(id)
                    ? 'bg-green-900/30 dark:bg-green-900/30 bg-green-100 text-green-400 dark:text-green-400 text-green-700'
                    : 'bg-dark-card dark:bg-dark-card bg-gray-200 text-gray-400 dark:text-gray-400 text-gray-600 hover:bg-dark-hover dark:hover:bg-dark-hover hover:bg-gray-300'
                }`}
              >
                Task #{id} {isSolved(id) ? '✓' : '→'}
              </a>
            ))}
          </div>
        </section>
      )}

      {/* Section: Interview Tips */}
      {step.tips.length > 0 && (
        <section className="rounded-lg border border-yellow-800/40 dark:border-yellow-800/40 border-yellow-200 bg-yellow-950/20 dark:bg-yellow-950/20 bg-yellow-50 p-4 space-y-2">
          <h2 className="flex items-center gap-2 text-base font-semibold text-yellow-400 dark:text-yellow-400 text-yellow-700">
            <AlertTriangle className="w-5 h-5" /> Interview Tips
          </h2>
          <ul className="space-y-1.5 text-sm">
            {step.tips.map((tip, i) => (
              <li key={i} className="flex items-start gap-2">
                <span className="text-yellow-400 dark:text-yellow-400 text-yellow-600 mt-0.5 shrink-0">•</span>
                <span className="text-gray-300 dark:text-gray-300 text-gray-700">{tip}</span>
              </li>
            ))}
          </ul>
        </section>
      )}

      {/* Navigation footer */}
      <div className="flex justify-between pt-4 border-t border-dark-border dark:border-dark-border border-gray-200">
        <button
          onClick={() => setStepIdx(stepIdx - 1)}
          disabled={stepIdx === 0}
          className="text-sm text-gray-400 hover:text-gray-200 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
        >
          ← Previous Lesson
        </button>
        <button
          onClick={() => setStepIdx(stepIdx + 1)}
          disabled={stepIdx === path.steps.length - 1}
          className="text-sm text-accent-blue hover:text-blue-300 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
        >
          Next Lesson →
        </button>
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Progress Audit View                                                */
/* ------------------------------------------------------------------ */

function AuditView({
  paths,
  isSolved,
  onOpenStep,
}: {
  paths: LearningPath[];
  isSolved: (id: number) => boolean;
  onOpenStep: (path: LearningPath, stepIdx: number) => void;
}) {
  return (
    <div className="space-y-4">
      {paths.map(path => {
        const allTaskIds = path.steps.flatMap(s => s.task_ids);
        const solvedCount = allTaskIds.filter(id => isSolved(id)).length;
        const total = allTaskIds.length;
        const pct = total > 0 ? Math.round((solvedCount / total) * 100) : 0;

        return (
          <div
            key={path.id}
            className="bg-dark-card dark:bg-dark-card bg-gray-50 border border-dark-border dark:border-dark-border border-gray-200 rounded-lg p-4 space-y-3"
          >
            {/* Header */}
            <div className="flex items-center justify-between">
              <h3 className="font-semibold">{path.title}</h3>
              <span className="text-sm text-gray-400 dark:text-gray-400 text-gray-600">
                {solvedCount}/{total} · {pct}%
              </span>
            </div>

            {/* Progress bar */}
            <div className="w-full bg-dark-bg dark:bg-dark-bg bg-gray-200 rounded-full h-2.5 overflow-hidden">
              <div
                className={`h-full rounded-full transition-all ${
                  pct === 100 ? 'bg-accent-green' : pct > 0 ? 'bg-accent-blue' : 'bg-gray-600'
                }`}
                style={{ width: `${pct}%` }}
              />
            </div>

            {/* Step rows */}
            <div className="space-y-2">
              {path.steps.map((step, i) => {
                const stepSolved = step.task_ids.filter(id => isSolved(id)).length;
                const stepTotal = step.task_ids.length;
                const allDone = stepTotal > 0 && stepSolved === stepTotal;

                return (
                  <button
                    key={i}
                    onClick={() => onOpenStep(path, i)}
                    className="w-full flex items-center gap-3 p-2 rounded-lg hover:bg-dark-hover dark:hover:bg-dark-hover hover:bg-gray-100 transition-colors text-left"
                  >
                    {allDone ? (
                      <CheckCircle2 className="w-4 h-4 text-accent-green shrink-0" />
                    ) : (
                      <div className="w-4 h-4 rounded-full border-2 border-gray-600 dark:border-gray-600 border-gray-300 shrink-0" />
                    )}

                    <span className="flex-1 text-sm font-medium truncate">{step.title}</span>

                    <span className="text-xs text-gray-500 shrink-0">
                      {stepSolved}/{stepTotal}
                    </span>

                    <div className="flex gap-1 shrink-0">
                      {step.task_ids.map(id => (
                        <span
                          key={id}
                          className={`text-[10px] px-1.5 py-0.5 rounded font-medium ${
                            isSolved(id)
                              ? 'bg-green-900/30 dark:bg-green-900/30 bg-green-100 text-green-400 dark:text-green-400 text-green-700'
                              : 'bg-dark-bg dark:bg-dark-bg bg-gray-200 text-gray-500'
                          }`}
                        >
                          #{id}
                        </span>
                      ))}
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        );
      })}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Path List View (main)                                              */
/* ------------------------------------------------------------------ */

export default function Learn() {
  const [paths, setPaths] = useState<LearningPath[]>([]);
  const [expanded, setExpanded] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedPath, setSelectedPath] = useState<LearningPath | null>(null);
  const [stepIdx, setStepIdx] = useState(0);
  const [viewMode, setViewMode] = useState<'paths' | 'audit'>('paths');
  const { isSolved } = useProgress();

  useEffect(() => {
    fetchLearningPaths()
      .then(setPaths)
      .catch(err => {
        console.error('Failed to load learning paths:', err);
        setError('Failed to load learning paths');
      });
  }, []);

  /* ---------- Lesson detail view ---------- */
  if (selectedPath) {
    return (
      <LessonView
        path={selectedPath}
        stepIdx={stepIdx}
        setStepIdx={setStepIdx}
        onBack={() => { setSelectedPath(null); setStepIdx(0); }}
        isSolved={isSolved}
      />
    );
  }

  /* ---------- Error state ---------- */
  if (error) {
    return (
      <div className="p-4 max-w-4xl">
        <div className="bg-red-900/20 dark:bg-red-900/20 bg-red-50 border border-red-800 dark:border-red-800 border-red-200 rounded-lg p-4 text-red-400 dark:text-red-400 text-red-600 text-sm">
          {error}
        </div>
      </div>
    );
  }

  /* ---------- Path list view ---------- */
  return (
    <div className="p-4 space-y-4 max-w-4xl">
      <div className="flex items-center justify-between flex-wrap gap-2">
        <div className="flex items-center gap-2">
          <BookOpen className="w-6 h-6 text-accent-blue" />
          <h1 className="text-xl font-bold">Learning Paths</h1>
        </div>
        <div className="flex gap-1">
          <button
            onClick={() => setViewMode('paths')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              viewMode === 'paths'
                ? 'bg-accent-blue text-white'
                : 'bg-dark-card dark:bg-dark-card bg-gray-50 border border-dark-border dark:border-dark-border border-gray-200 text-gray-400 hover:bg-dark-hover dark:hover:bg-dark-hover hover:bg-gray-100'
            }`}
          >
            <BookOpen className="w-3.5 h-3.5 inline-block mr-1 -mt-0.5" />
            Paths
          </button>
          <button
            onClick={() => setViewMode('audit')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              viewMode === 'audit'
                ? 'bg-accent-blue text-white'
                : 'bg-dark-card dark:bg-dark-card bg-gray-50 border border-dark-border dark:border-dark-border border-gray-200 text-gray-400 hover:bg-dark-hover dark:hover:bg-dark-hover hover:bg-gray-100'
            }`}
          >
            <BarChart3 className="w-3.5 h-3.5 inline-block mr-1 -mt-0.5" />
            Progress Audit
          </button>
        </div>
      </div>

      {paths.length === 0 && (
        <div className="text-gray-500 text-sm">Loading learning paths...</div>
      )}

      {viewMode === 'audit' ? (
        <AuditView
          paths={paths}
          isSolved={isSolved}
          onOpenStep={(path, i) => { setSelectedPath(path); setStepIdx(i); }}
        />
      ) : (
      <div className="space-y-3">
        {paths.map(path => {
          const allTaskIds = path.steps.flatMap(s => s.task_ids);
          const solvedCount = allTaskIds.filter(id => isSolved(id)).length;
          const total = allTaskIds.length;
          const pct = total > 0 ? Math.round((solvedCount / total) * 100) : 0;

          return (
            <div key={path.id} className="bg-dark-card dark:bg-dark-card bg-gray-50 border border-dark-border dark:border-dark-border border-gray-200 rounded-lg overflow-hidden">
              <button
                onClick={() => setExpanded(expanded === path.id ? null : path.id)}
                className="w-full flex items-center justify-between p-4 hover:bg-dark-hover dark:hover:bg-dark-hover hover:bg-gray-100 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <ChevronRight className={`w-4 h-4 transition-transform ${expanded === path.id ? 'rotate-90' : ''}`} />
                  <div className="text-left">
                    <h3 className="font-medium">{path.title}</h3>
                    <p className="text-xs text-gray-500">{path.description}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2 text-sm">
                  <div className="w-24 bg-dark-bg dark:bg-dark-bg bg-gray-200 rounded-full h-2 overflow-hidden">
                    <div className="bg-accent-blue h-full rounded-full transition-all" style={{ width: `${pct}%` }} />
                  </div>
                  <span className="text-gray-500 text-xs">{solvedCount}/{total}</span>
                </div>
              </button>

              {expanded === path.id && (
                <div className="px-4 pb-4 space-y-3 border-t border-dark-border dark:border-dark-border border-gray-200 pt-3">
                  {path.steps.map((step, i) => (
                    <div key={i} className="pl-4 border-l-2 border-dark-border dark:border-dark-border border-gray-300 flex items-center justify-between">
                      <div className="flex-1 min-w-0">
                        <h4 className="font-medium text-sm">{step.title}</h4>
                        <p className="text-xs text-gray-500 mt-0.5">{step.description}</p>
                        <div className="flex gap-1 mt-1.5 flex-wrap">
                          {step.task_ids.map(id => (
                            <span key={id} className={`text-xs px-1.5 py-0.5 rounded ${
                              isSolved(id)
                                ? 'bg-green-900/30 dark:bg-green-900/30 bg-green-100 text-green-400 dark:text-green-400 text-green-700'
                                : 'bg-dark-bg dark:bg-dark-bg bg-gray-200 text-gray-500'
                            }`}>
                              #{id}
                            </span>
                          ))}
                        </div>
                      </div>
                      <button
                        onClick={(e) => { e.stopPropagation(); setSelectedPath(path); setStepIdx(i); }}
                        className="shrink-0 ml-3 px-3 py-1.5 rounded-lg text-xs font-medium bg-accent-blue text-white hover:bg-blue-600 transition-colors"
                      >
                        Start Lesson
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>
      )}
    </div>
  );
}
