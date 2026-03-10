import axios from 'axios';
import type {
  ExecuteResponse, Task, CheckResponse, ProgressEntry, Flashcard,
  Assignment, LearningPath, MockSession, MockResult, AuthUser,
  HistoryEntry, LeaderboardEntry, StreakData, ColumnInfo, QueryTemplate,
  FlashcardState, TasksMeta, InterviewQuestion, InterviewMeta, SQLPattern,
} from '../types';

const api = axios.create({ baseURL: '/api' });

// Auth interceptor
export function setAuthToken(token: string | null) {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common['Authorization'];
  }
}

// Auth
export async function register(username: string): Promise<AuthUser> {
  const { data } = await api.post('/auth/register', { username });
  return data;
}

export async function login(username: string): Promise<AuthUser> {
  const { data } = await api.post('/auth/login', { username });
  return data;
}

// Execute
export async function executeSQL(sql: string, session_id?: string): Promise<ExecuteResponse> {
  const { data } = await api.post('/execute', { sql, session_id });
  return data;
}

// Tasks
export async function fetchTasks(category?: string, difficulty?: string): Promise<Task[]> {
  const params: Record<string, string> = {};
  if (category) params.category = category;
  if (difficulty) params.difficulty = difficulty;
  const { data } = await api.get('/tasks', { params });
  return data;
}

export async function fetchTask(id: number): Promise<Task> {
  const { data } = await api.get(`/tasks/${id}`);
  return data;
}

export async function fetchTasksMeta(): Promise<TasksMeta> {
  const { data } = await api.get('/tasks/meta');
  return data;
}

export async function checkTask(taskId: number, sql: string, session_id?: string): Promise<CheckResponse> {
  const { data } = await api.post(`/tasks/${taskId}/check`, { sql, session_id });
  return data;
}

// Progress
export async function fetchProgress(): Promise<ProgressEntry[]> {
  const { data } = await api.get('/progress');
  return data;
}

export async function updateProgress(entry: ProgressEntry): Promise<ProgressEntry> {
  const { data } = await api.post('/progress', entry);
  return data;
}

// Flashcards
export async function fetchFlashcards(): Promise<Flashcard[]> {
  const { data } = await api.get('/flashcards');
  return data;
}

export async function fetchFlashcardProgress(): Promise<FlashcardState[]> {
  const { data } = await api.get('/flashcards/progress');
  return data;
}

export async function reviewFlashcard(card_id: number, quality: number): Promise<any> {
  const { data } = await api.post('/flashcards/review', { card_id, quality });
  return data;
}

// Assignments
export async function fetchAssignments(): Promise<Assignment[]> {
  const { data } = await api.get('/assignments');
  return data;
}

export async function fetchLearningPaths(): Promise<LearningPath[]> {
  const { data } = await api.get('/learning-paths');
  return data;
}

export async function fetchDaily(): Promise<Task> {
  const { data } = await api.get('/daily');
  return data;
}

// Tables
export async function fetchTables(): Promise<string[]> {
  const { data } = await api.get('/tables');
  return data.tables;
}

export async function fetchTableData(name: string, limit?: number, offset?: number): Promise<ExecuteResponse> {
  const params: Record<string, number> = {};
  if (limit) params.limit = limit;
  if (offset) params.offset = offset;
  const { data } = await api.get(`/tables/${name}`, { params });
  return data;
}

export async function fetchTableSchema(name: string): Promise<ColumnInfo[]> {
  const { data } = await api.get(`/tables/${name}/schema`);
  return data;
}

// Mock
export async function startMock(difficulty?: string): Promise<MockSession> {
  const { data } = await api.post('/mock/start', { difficulty });
  return data;
}

export async function endMock(session_id: string, results: any[]): Promise<MockResult> {
  const { data } = await api.post('/mock/end', { session_id, results });
  return data;
}

// History
export async function fetchHistory(limit?: number): Promise<HistoryEntry[]> {
  const { data } = await api.get('/history', { params: { limit } });
  return data;
}

export async function clearHistory(): Promise<void> {
  await api.delete('/history');
}

// Bookmarks
export async function fetchBookmarks(): Promise<{ task_id: number; created_at: string }[]> {
  const { data } = await api.get('/bookmarks');
  return data;
}

export async function addBookmark(task_id: number): Promise<void> {
  await api.post('/bookmarks', { task_id });
}

export async function removeBookmark(task_id: number): Promise<void> {
  await api.delete(`/bookmarks/${task_id}`);
}

// Streaks
export async function fetchStreaks(): Promise<StreakData> {
  const { data } = await api.get('/streaks');
  return data;
}

export async function recordStreak(task_id: number): Promise<void> {
  await api.post('/streaks', { task_id });
}

// Leaderboard
export async function fetchLeaderboard(): Promise<LeaderboardEntry[]> {
  const { data } = await api.get('/leaderboard');
  return data;
}

// Format
export async function formatSQL(sql: string): Promise<string> {
  const { data } = await api.post('/format', { sql });
  return data.formatted;
}

// Templates
export async function fetchTemplates(): Promise<QueryTemplate[]> {
  const { data } = await api.get('/templates');
  return data;
}

// Interview Questions
export async function fetchInterviewQuestions(company?: string, pattern?: string, difficulty?: string): Promise<InterviewQuestion[]> {
  const params: Record<string, string> = {};
  if (company) params.company = company;
  if (pattern) params.pattern = pattern;
  if (difficulty) params.difficulty = difficulty;
  const { data } = await api.get('/interview-questions', { params });
  return data;
}

export async function fetchInterviewMeta(): Promise<InterviewMeta> {
  const { data } = await api.get('/interview-questions/meta');
  return data;
}

export async function fetchInterviewQuestion(id: number): Promise<InterviewQuestion> {
  const { data } = await api.get(`/interview-questions/${id}`);
  return data;
}

export async function checkInterviewQuestion(id: number, sql: string, session_id?: string): Promise<CheckResponse> {
  const { data } = await api.post(`/interview-questions/${id}/check`, { sql, session_id });
  return data;
}

// Patterns
export async function fetchPatterns(category?: string): Promise<SQLPattern[]> {
  const params: Record<string, string> = {};
  if (category) params.category = category;
  const { data } = await api.get('/patterns', { params });
  return data;
}

export async function fetchPatternCategories(): Promise<string[]> {
  const { data } = await api.get('/patterns/categories');
  return data;
}
