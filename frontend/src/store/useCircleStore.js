import { create } from 'zustand'

export const useCircleStore = create((set) => ({
  votes: {},
  matches: [],
  liveActivity: [],
  recordVote: (showId, userId, voteType) =>
    set((state) => ({ votes: { ...state.votes, [showId]: { ...(state.votes[showId] || {}), [userId]: voteType } } })),
  addMatch: (match) => set((state) => ({ matches: [match, ...state.matches.filter((m) => m.tmdb_id !== match.tmdb_id)] })),
  pushActivity: (event) => set((state) => ({ liveActivity: [event, ...state.liveActivity].slice(0, 5) })),
}))
