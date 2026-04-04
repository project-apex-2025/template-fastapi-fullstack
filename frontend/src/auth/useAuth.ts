import { useState, useEffect, useCallback } from 'react';
import {
  signInWithRedirect,
  signOut,
  getCurrentUser,
  fetchAuthSession,
  AuthUser,
} from 'aws-amplify/auth';
import { Hub } from 'aws-amplify/utils';

export function useAuth() {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [alias, setAlias] = useState<string | null>(null);

  const checkAuth = useCallback(async () => {
    try {
      const u = await getCurrentUser();
      const session = await fetchAuthSession();
      const email = (session.tokens?.idToken?.payload?.email as string) ?? null;
      setUser(u);
      setIsAuthenticated(true);
      setAlias(email ? email.split('@')[0].toLowerCase() : null);
    } catch {
      setUser(null);
      setIsAuthenticated(false);
      setAlias(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    checkAuth();
    const unsubscribe = Hub.listen('auth', ({ payload }) => {
      if (payload.event === 'signedIn' || payload.event === 'tokenRefresh') checkAuth();
      if (payload.event === 'signedOut') {
        setUser(null);
        setIsAuthenticated(false);
        setAlias(null);
      }
    });
    return unsubscribe;
  }, [checkAuth]);

  const login = useCallback(async () => { await signInWithRedirect(); }, []);
  const logout = useCallback(async () => { await signOut(); }, []);

  return { user, isAuthenticated, isLoading, alias, login, logout };
}
