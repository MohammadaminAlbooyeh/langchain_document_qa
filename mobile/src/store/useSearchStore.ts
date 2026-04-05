import create from 'zustand'

export const useSearchStore = create((set) => ({
  query: '',
  setQuery: (q: string) => set({ query: q }),
}))
