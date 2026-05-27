import { useCallback } from 'react';
import toast from 'react-hot-toast';

export function useNotification() {
  const notify = useCallback((message, type = 'info') => {
    toast[type]?.(message) ?? toast(message);
  }, []);

  return { notify };
}
