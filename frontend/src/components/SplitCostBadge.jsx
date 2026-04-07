export default function SplitCostBadge({ price, memberCount, availability = 'rent' }) {
  if (availability !== 'rent' || memberCount <= 1) return null
  return (
    <div className="rounded-full bg-gold/30 px-3 py-1 text-xs text-gold">
      Rent ${price?.toFixed?.(2) ?? price} · split {memberCount} ways = ${(price / memberCount).toFixed(2)} each
    </div>
  )
}
