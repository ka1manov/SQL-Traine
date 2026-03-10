import React, { createContext, useState, useEffect, useCallback } from 'react';
import type { AuthUser } from '../types';
import { login as apiLogin, register as apiRegister, setAuthToken } from '../utils/api';

interface AuthContextType {
  user: AuthUser | null;
  login: (username: string) => Promise<void>;
  logout: () => void;
  isLoggedIn: boolean;
}

export const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(() => {
    try {
      const stored = localStorage.getItem('sql_trainer_user');
      if (stored) {
        const u = JSON.parse(stored);
        setAuthToken(u.token);
        return u;
      }
    } catch {}
    return null;
  });

  const login = useCallback(async (username: string) => {
    const u = await apiLogin(username);
    setAuthToken(u.token);
    setUser(u);
    localStorage.setItem('sql_trainer_user', JSON.stringify(u));
  }, []);

  const logout = useCallback(() => {
    setAuthToken(null);
    setUser(null);
    localStorage.removeItem('sql_trainer_user');
  }, []);

  return (
    <AuthContext.Provider value={{ user, login, logout, isLoggedIn: !!user }}>
      {children}
    </AuthContext.Provider>
  );
}
