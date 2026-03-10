import { useState } from 'react';
import { ChevronDown, ChevronRight } from 'lucide-react';

const DATA_TYPES = [
  { name: 'SERIAL', desc: 'Auto-incrementing 4-byte integer', example: 'id SERIAL PRIMARY KEY' },
  { name: 'INTEGER', desc: '4-byte signed integer (-2B to 2B)', example: 'age INTEGER' },
  { name: 'BIGINT', desc: '8-byte signed integer', example: 'population BIGINT' },
  { name: 'VARCHAR(n)', desc: 'Variable-length string with limit', example: 'name VARCHAR(100)' },
  { name: 'TEXT', desc: 'Unlimited variable-length string', example: 'bio TEXT' },
  { name: 'BOOLEAN', desc: 'true/false', example: 'is_active BOOLEAN DEFAULT true' },
  { name: 'DATE', desc: 'Calendar date (no time)', example: 'birth_date DATE' },
  { name: 'TIMESTAMP', desc: 'Date + time without timezone', example: 'created_at TIMESTAMP' },
  { name: 'TIMESTAMPTZ', desc: 'Date + time with timezone', example: 'event_time TIMESTAMPTZ' },
  { name: 'NUMERIC(p,s)', desc: 'Exact decimal with precision/scale', example: 'price NUMERIC(10,2)' },
  { name: 'UUID', desc: '128-bit universally unique identifier', example: 'token UUID DEFAULT gen_random_uuid()' },
];

const CONSTRAINTS = [
  { name: 'PRIMARY KEY', desc: 'Uniquely identifies each row', syntax: 'id SERIAL PRIMARY KEY' },
  { name: 'FOREIGN KEY', desc: 'References a row in another table', syntax: 'user_id INT REFERENCES users(id)' },
  { name: 'NOT NULL', desc: 'Column cannot contain NULL', syntax: 'email VARCHAR(255) NOT NULL' },
  { name: 'UNIQUE', desc: 'All values must be distinct', syntax: 'email VARCHAR(255) UNIQUE' },
  { name: 'CHECK', desc: 'Custom validation expression', syntax: 'age INT CHECK (age >= 0)' },
  { name: 'DEFAULT', desc: 'Value when none is provided', syntax: "status VARCHAR(20) DEFAULT 'active'" },
];

const RELATIONSHIPS = [
  { name: 'One-to-One (1:1)', desc: 'Each row relates to exactly one row in another table', when: 'User profile split into users + user_settings' },
  { name: 'One-to-Many (1:N)', desc: 'One row relates to many rows in another table', when: 'One department has many employees' },
  { name: 'Many-to-Many (N:M)', desc: 'Many rows relate to many rows via a junction table', when: 'Students enroll in many courses, courses have many students' },
];

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="border-b border-gray-200 dark:border-dark-border last:border-0">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center gap-2 px-3 py-2 text-sm font-medium text-left hover:bg-gray-100 dark:hover:bg-dark-hover transition-colors"
      >
        {open ? <ChevronDown className="w-3.5 h-3.5 shrink-0" /> : <ChevronRight className="w-3.5 h-3.5 shrink-0" />}
        {title}
      </button>
      {open && <div className="px-3 pb-3">{children}</div>}
    </div>
  );
}

export default function TypeReference() {
  return (
    <div className="border border-gray-200 dark:border-dark-border rounded-lg overflow-hidden text-xs">
      <div className="px-3 py-2 bg-gray-100 dark:bg-dark-surface font-semibold text-sm">Reference Guide</div>
      <Section title="Data Types">
        <div className="space-y-2">
          {DATA_TYPES.map(t => (
            <div key={t.name}>
              <span className="font-mono font-semibold text-accent-blue">{t.name}</span>
              <p className="text-gray-500 dark:text-gray-400">{t.desc}</p>
              <code className="text-[10px] text-gray-400 dark:text-gray-500">{t.example}</code>
            </div>
          ))}
        </div>
      </Section>
      <Section title="Constraints">
        <div className="space-y-2">
          {CONSTRAINTS.map(c => (
            <div key={c.name}>
              <span className="font-mono font-semibold text-accent-green">{c.name}</span>
              <p className="text-gray-500 dark:text-gray-400">{c.desc}</p>
              <code className="text-[10px] text-gray-400 dark:text-gray-500">{c.syntax}</code>
            </div>
          ))}
        </div>
      </Section>
      <Section title="Relationships">
        <div className="space-y-2">
          {RELATIONSHIPS.map(r => (
            <div key={r.name}>
              <span className="font-semibold text-accent-purple">{r.name}</span>
              <p className="text-gray-500 dark:text-gray-400">{r.desc}</p>
              <p className="text-gray-400 dark:text-gray-500 italic">e.g. {r.when}</p>
            </div>
          ))}
        </div>
      </Section>
    </div>
  );
}
