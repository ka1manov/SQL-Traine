export interface ExecuteResponse {
  columns: string[];
  rows: any[][];
  row_count: number;
  error: string | null;
  execution_time_ms: number;
  total_rows?: number;
}

export interface Task {
  id: number;
  title: string;
  description: string;
  category: string;
  difficulty: string;
  hint: string | null;
  tables: string[];
  solution_sql?: string;
  explanation?: string | null;
}

export interface DiffResult {
  match_pct: number;
  matching_rows: any[][];
  missing_rows: any[][];
  extra_rows: any[][];
  expected_columns: string[];
  actual_columns: string[];
  order_correct: boolean;
  column_order_match: boolean;
}

export interface CheckResponse {
  correct: boolean;
  match_pct: number;
  diff: DiffResult | null;
  actual: ExecuteResponse | null;
  expected: ExecuteResponse | null;
  error: string | null;
}

export interface ProgressEntry {
  task_id: number;
  solved: boolean;
  best_match_pct: number;
  attempts: number;
}

export interface Flashcard {
  id: number;
  question: string;
  answer: string;
  category: string;
}

export interface FlashcardState {
  card_id: number;
  ease_factor: number;
  interval_days: number;
  repetitions: number;
  next_review: string;
}

export interface AssignmentStep {
  step: number;
  title: string;
  description: string;
  hint: string;
  solution_sql: string | null;
}

export interface Assignment {
  id: number;
  title: string;
  company: string;
  description: string;
  tables: string[];
  steps: AssignmentStep[];
}

export interface QuizQuestion {
  question: string;
  answer: string;
}

export interface SQLExample {
  title: string;
  sql: string;
  explanation: string;
}

export interface PathStep {
  title: string;
  description: string;
  task_ids: number[];
  example_sql: string | null;
  theory: string;
  key_points: string[];
  syntax: string | null;
  examples: SQLExample[];
  quiz: QuizQuestion[];
  tips: string[];
}

export interface LearningPath {
  id: number;
  title: string;
  description: string;
  icon: string;
  steps: PathStep[];
}

export interface MockSession {
  session_id: string;
  task_ids: number[];
  time_limit: number;
}

export interface MockResult {
  total_score: number;
  tasks_solved: number;
  total_tasks: number;
  time_used: number | null;
  details: any[];
}

export interface AuthUser {
  user_id: number;
  username: string;
  token: string;
}

export interface HistoryEntry {
  id: number;
  sql_text: string;
  execution_time_ms: number | null;
  row_count: number;
  had_error: boolean;
  created_at: string;
}

export interface LeaderboardEntry {
  username: string;
  tasks_solved: number;
  total_attempts: number;
  avg_match_pct: number;
}

export interface StreakData {
  current_streak: number;
  best_streak: number;
  days: { date: string; task_id: number }[];
}

export interface ColumnInfo {
  name: string;
  type: string;
  nullable: boolean;
  default: string | null;
  fk: string | null;
}

export interface QueryTemplate {
  id: number;
  title: string;
  category: string;
  description: string;
  sql: string;
}

export interface TasksMeta {
  total: number;
  categories: Record<string, number[]>;
  difficulties: Record<string, number[]>;
}

export interface InterviewQuestion {
  id: number;
  title: string;
  description: string;
  company_tags: string[];
  pattern: string;
  difficulty: string;
  tables: string[];
  hint: string | null;
  solution_sql?: string;
  explanation?: string;
}

export interface InterviewMeta {
  total: number;
  companies: Record<string, number>;
  patterns: Record<string, number>;
}

export interface SQLPattern {
  id: number;
  name: string;
  category: string;
  description: string;
  template_sql: string;
  example_sql: string;
  explanation: string;
  use_cases: string[];
  related_task_ids: number[];
}

// Schema Builder
export type ColumnDataType =
  | 'SERIAL' | 'BIGSERIAL' | 'INTEGER' | 'BIGINT' | 'SMALLINT'
  | 'VARCHAR' | 'TEXT' | 'BOOLEAN' | 'DATE' | 'TIMESTAMP' | 'TIMESTAMPTZ'
  | 'NUMERIC' | 'REAL' | 'DOUBLE PRECISION' | 'JSONB' | 'JSON' | 'UUID';

export interface SchemaColumn {
  id: string;
  name: string;
  dataType: ColumnDataType;
  length: number | null;
  precision: number | null;
  scale: number | null;
  isPrimaryKey: boolean;
  isNotNull: boolean;
  isUnique: boolean;
  defaultValue: string | null;
  checkConstraint: string | null;
  foreignKey: { tableId: string; columnId: string } | null;
}

export interface SchemaTable {
  id: string;
  name: string;
  columns: SchemaColumn[];
  position: { x: number; y: number };
}

export interface SchemaState {
  tables: SchemaTable[];
}

export interface ValidateDDLResponse {
  valid: boolean;
  error: string | null;
  details: string | null;
}
