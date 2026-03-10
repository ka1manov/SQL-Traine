import { useState, useContext } from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import {
  Database, Terminal, ListChecks, Star, BookOpen, Layers,
  Brain, BarChart3, Briefcase, Table2, Trophy, Menu, X, LogIn, LogOut, Keyboard,
  FileQuestion, ScrollText, Blocks,
} from 'lucide-react';
import ThemeToggle from './ThemeToggle';
import KeyboardShortcuts from './KeyboardShortcuts';
import { AuthContext } from '../contexts/AuthContext';

const navItems = [
  { to: '/', icon: Terminal, label: 'Sandbox' },
  { to: '/tasks', icon: ListChecks, label: 'Tasks' },
  { to: '/daily', icon: Star, label: 'Daily' },
  { to: '/learn', icon: BookOpen, label: 'Learn' },
  { to: '/patterns', icon: ScrollText, label: 'Patterns' },
  { to: '/interview', icon: FileQuestion, label: 'Interview Q' },
  { to: '/flashcards', icon: Brain, label: 'Flashcards' },
  { to: '/explorer', icon: Table2, label: 'Explorer' },
  { to: '/schema-builder', icon: Blocks, label: 'Schema Builder' },
  { to: '/mock', icon: Layers, label: 'Mock Interview' },
  { to: '/eda', icon: BarChart3, label: 'EDA' },
  { to: '/take-home', icon: Briefcase, label: 'Take-Home' },
  { to: '/leaderboard', icon: Trophy, label: 'Leaderboard' },
  { to: '/progress', icon: BarChart3, label: 'Progress' },
];

export default function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [shortcutsOpen, setShortcutsOpen] = useState(false);
  const auth = useContext(AuthContext);
  const [loginInput, setLoginInput] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (loginInput.trim()) {
      await auth?.login(loginInput.trim());
      setLoginInput('');
    }
  };

  const sidebar = (
    <>
      <div className="p-4 border-b border-dark-border dark:border-dark-border border-gray-200 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Database className="w-6 h-6 text-accent-blue" />
          <span className="font-bold text-lg">SQL Lab</span>
        </div>
        <div className="flex items-center gap-1">
          <ThemeToggle />
          <button onClick={() => setShortcutsOpen(true)} className="p-1.5 rounded-lg hover:bg-dark-hover text-gray-400 lg:inline-flex hidden" title="Shortcuts">
            <Keyboard className="w-4 h-4" />
          </button>
          <button onClick={() => setSidebarOpen(false)} className="p-1.5 rounded-lg hover:bg-dark-hover text-gray-400 lg:hidden">
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>
      <nav className="flex-1 overflow-y-auto py-2">
        {navItems.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            onClick={() => setSidebarOpen(false)}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-2.5 text-sm transition-colors ${
                isActive
                  ? 'bg-accent-blue/10 text-accent-blue border-r-2 border-accent-blue'
                  : 'text-gray-400 hover:text-gray-200 hover:bg-dark-hover dark:hover:bg-dark-hover hover:bg-gray-100'
              }`
            }
          >
            <Icon className="w-4 h-4" />
            {label}
          </NavLink>
        ))}
      </nav>
      <div className="p-3 border-t border-dark-border dark:border-dark-border border-gray-200">
        {auth?.isLoggedIn ? (
          <div className="flex items-center justify-between">
            <span className="text-xs text-gray-500 truncate">{auth.user?.username}</span>
            <button onClick={auth.logout} className="p-1 text-gray-500 hover:text-gray-300" title="Logout">
              <LogOut className="w-3.5 h-3.5" />
            </button>
          </div>
        ) : (
          <form onSubmit={handleLogin} className="flex gap-1">
            <input
              value={loginInput}
              onChange={e => setLoginInput(e.target.value)}
              placeholder="Username"
              className="flex-1 min-w-0 px-2 py-1 bg-dark-bg dark:bg-dark-bg bg-gray-50 border border-dark-border dark:border-dark-border border-gray-300 rounded text-xs focus:outline-none focus:border-accent-blue"
            />
            <button type="submit" className="p-1 text-accent-blue hover:text-blue-400" title="Login">
              <LogIn className="w-3.5 h-3.5" />
            </button>
          </form>
        )}
      </div>
    </>
  );

  return (
    <div className="flex h-screen overflow-hidden bg-dark-bg dark:bg-dark-bg bg-white text-gray-100 dark:text-gray-100 text-gray-900">
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div className="fixed inset-0 z-40 bg-black/50 lg:hidden" onClick={() => setSidebarOpen(false)} />
      )}

      {/* Sidebar */}
      <aside className={`
        fixed inset-y-0 left-0 z-50 w-56 bg-dark-surface dark:bg-dark-surface bg-gray-50 border-r border-dark-border dark:border-dark-border border-gray-200 flex flex-col shrink-0
        transform transition-transform lg:relative lg:translate-x-0
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        {sidebar}
      </aside>

      {/* Main */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <div className="lg:hidden flex items-center gap-2 p-2 border-b border-dark-border dark:border-dark-border border-gray-200">
          <button onClick={() => setSidebarOpen(true)} className="p-2 hover:bg-dark-hover rounded-lg">
            <Menu className="w-5 h-5" />
          </button>
          <Database className="w-5 h-5 text-accent-blue" />
          <span className="font-bold">SQL Lab</span>
        </div>
        <main className="flex-1 overflow-y-auto">
          <Outlet />
        </main>
      </div>

      <KeyboardShortcuts open={shortcutsOpen} onClose={() => setShortcutsOpen(false)} />
    </div>
  );
}
