import SplitCostBadge from './SplitCostBadge'

export default function MatchCard({ match, memberCount }) {
  const rent = match.platforms?.find((p) => p.type === 'rent')
  return (
    <div className="rounded-xl bg-surface p-3">
      <div className="text-lg">{match.title}</div>
      <div className="h-2 rounded bg-surface2"><div className="h-full rounded bg-green" style={{ width: `${match.match_pct}%` }} /></div>
      <div className="text-xs">{match.match_pct}% · {match.likers?.join(', ')}</div>
      {rent && <SplitCostBadge price={rent.price || 3.99} memberCount={memberCount} availability="rent" />}
    </div>
  )
}
