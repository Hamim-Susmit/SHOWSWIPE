import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchShows, submitVote } from '../api/client'
import ActionBar from '../components/ActionBar'
import CardStack from '../components/CardStack'
import { useCircleWS } from '../hooks/useCircleWS'
import { useAppStore } from '../store/useAppStore'

export default function SwipePage() {
  const { circleId, currentUserId, selectedPlatforms, selectedLanguages, availabilityMode, circleMembers } = useAppStore()
  const [shows, setShows] = useState([])
  const [index, setIndex] = useState(0)
  const [page, setPage] = useState(1)
  const [error, setError] = useState('')
  const { lastEvent } = useCircleWS(circleId)

  useEffect(() => { load(1) }, [])
  const remaining = useMemo(() => Math.max(0, shows.length - index), [shows.length, index])

  const load = async (next) => {
    try {
      const res = await fetchShows({ platforms: selectedPlatforms, languages: selectedLanguages, availability: availabilityMode, page: next })
      setShows((prev) => next === 1 ? res.data : [...prev, ...res.data])
      setPage(next)
    } catch { setError('Something went wrong — tap to retry') }
  }

  const vote = async (vote_type) => {
    const show = shows[index]
    if (!show) return
    await submitVote({ show_id: show.tmdb_id, user_id: currentUserId, circle_id: circleId, vote_type })
    const nextIndex = index + 1
    setIndex(nextIndex)
    if (shows.length - nextIndex <= 5) load(page + 1)
  }

  if (error) return <button onClick={() => load(page)}>{error}</button>
  if (!shows.length) return <div className="p-4">Loading…</div>
  if (remaining === 0) return <div className="p-4">You've seen everything! 🎬 Check your matches <Link to="/matches" className="underline">Matches</Link></div>

  return <div className="mx-auto flex min-h-screen max-w-[420px] flex-col p-3">
    <div className="mb-2 flex items-center justify-between"><h1 className="font-display text-4xl">ShowSwipe</h1><div>{remaining} remaining</div></div>
    <div className="mb-2 text-xs text-accent2">{lastEvent ? JSON.stringify(lastEvent) : 'Live activity waiting…'}</div>
    <div className="relative h-[70vh]">
      <CardStack shows={shows} index={index} onVote={vote} memberCount={circleMembers.length || 1} />
    </div>
    <ActionBar onNope={() => vote('nope')} onLike={() => vote('like')} onSuper={() => vote('super')} />
    <Link className="mt-3 text-center underline" to="/matches">View Matches</Link>
  </div>
}
