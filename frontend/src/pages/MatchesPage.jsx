import { useEffect, useState } from 'react'
import { fetchMatches } from '../api/client'
import MatchCard from '../components/MatchCard'
import { useCircleWS } from '../hooks/useCircleWS'
import { useAppStore } from '../store/useAppStore'
import { useCircleStore } from '../store/useCircleStore'

export default function MatchesPage() {
  const { circleId, circleMembers } = useAppStore()
  const { matches: liveMatches, addMatch } = useCircleStore()
  const { lastEvent } = useCircleWS(circleId)
  const [matches, setMatches] = useState([])

  useEffect(() => {
    fetchMatches(circleId).then((r) => setMatches(r.data)).catch(() => setMatches([]))
  }, [circleId])

  useEffect(() => {
    if (lastEvent?.event === 'match') addMatch(lastEvent.show || lastEvent)
  }, [lastEvent, addMatch])

  const merged = [...liveMatches, ...matches.filter((m) => !liveMatches.some((l) => l.tmdb_id === m.tmdb_id))]

  return <div className="mx-auto max-w-[420px] p-4">
    <h1 className="font-display text-5xl">Circle Matches</h1>
    <p className="mb-4 text-sm text-gray-300">{merged.length} shows your circle agrees on</p>
    {!merged.length ? <div>Keep swiping — matches appear when your circle agrees</div> : <div className="space-y-3">{merged.map((m, i) => <MatchCard key={m.tmdb_id || i} match={m} memberCount={circleMembers.length || 1} />)}</div>}
  </div>
}
