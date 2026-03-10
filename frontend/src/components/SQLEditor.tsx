import { useContext } from 'react';
import Editor from '@monaco-editor/react';
import { ThemeContext } from '../contexts/ThemeContext';

interface Props {
  value: string;
  onChange: (value: string) => void;
  onRun?: () => void;
  onFormat?: () => void;
  height?: string;
}

export default function SQLEditor({ value, onChange, onRun, onFormat, height = '200px' }: Props) {
  const { theme } = useContext(ThemeContext);

  return (
    <div className="border border-dark-border dark:border-dark-border border-gray-300 rounded-lg overflow-hidden">
      <Editor
        height={height}
        defaultLanguage="sql"
        theme={theme === 'dark' ? 'vs-dark' : 'light'}
        value={value}
        onChange={(v) => onChange(v || '')}
        options={{
          minimap: { enabled: false },
          fontSize: 14,
          lineNumbers: 'on',
          scrollBeyondLastLine: false,
          wordWrap: 'on',
          padding: { top: 8 },
          automaticLayout: true,
        }}
        onMount={(editor, monaco) => {
          // Ctrl/Cmd + Enter = Run
          editor.addAction({
            id: 'run-query',
            label: 'Run Query',
            keybindings: [monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter],
            run: () => onRun?.(),
          });
          // Ctrl/Cmd + Shift + F = Format
          editor.addAction({
            id: 'format-sql',
            label: 'Format SQL',
            keybindings: [monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.KeyF],
            run: () => onFormat?.(),
          });
        }}
      />
    </div>
  );
}
