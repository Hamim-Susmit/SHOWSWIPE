import axios from 'axios'

const api = axios.create({ baseURL: 'http://localhost:8000' })

export const fetchShows = (params) => api.get('/api/shows', { params })
export const fetchShowDetail = (tmdbId) => api.get(`/api/shows/${tmdbId}`)
export const createCircle = (data) => api.post('/api/circle', data)
export const fetchCircle = (circleId) => api.get(`/api/circle/${circleId}`)
export const submitVote = (data) => api.post('/api/votes', data)
export const fetchMatches = (circleId) => api.get(`/api/matches/${circleId}`)
