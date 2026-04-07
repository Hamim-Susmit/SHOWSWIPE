import { create } from 'zustand'

export const useAppStore = create((set) => ({
  circleId: null,
  circleMembers: [],
  currentUserId: null,
  currentUserName: 'You',
  selectedPlatforms: ['Netflix', 'HBO Max'],
  selectedLanguages: ['en'],
  availabilityMode: 'flatrate',
  setCircle: (id, members) =>
    set({
      circleId: id,
      circleMembers: members,
      currentUserId: members?.[0]?.id || null,
      currentUserName: members?.[0]?.name || 'You',
    }),
  setPlatforms: (selectedPlatforms) => set({ selectedPlatforms }),
  setLanguages: (selectedLanguages) => set({ selectedLanguages }),
  setAvailabilityMode: (availabilityMode) => set({ availabilityMode }),
}))
