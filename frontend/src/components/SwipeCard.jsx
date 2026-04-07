import { motion } from 'framer-motion'
import { useRef, useState } from 'react'
import { useSwipe } from '../hooks/useSwipe'
import DetailPanel from './DetailPanel'
import TrailerModal from './TrailerModal'

export default function SwipeCard({ show, onSwipeLeft, onSwipeRight, onSuperLike, isTop, memberCount = 1 }) {
  const ref = useRef(null)
  const { likeOpacity, nopeOpacity } = useSwipe(ref, onSwipeLeft, onSwipeRight)
  const [detailOpen, setDetailOpen] = useState(false)
  const [trailerOpen, setTrailerOpen] = useState(false)

  return (
    <motion.div ref={ref} className="absolute inset-0 overflow-hidden rounded-3xl bg-surface shadow-2xl">
      <img src={show.poster_url || `https://image.tmdb.org/t/p/w500${show.poster_path}`} className="h-full w-full object-cover" />
      <div className="absolute inset-0 bg-gradient-to-b from-black/70 to-transparent" />
      <div className="absolute inset-0 bg-gradient-to-t from-black via-black/70 to-transparent" />
      <div className="absolute left-3 top-3 rounded-full bg-surface2 px-2 py-1 text-xs">{show.platforms?.[0]?.name || 'Streaming'}</div>
      <div className="absolute right-3 top-3 rounded-full bg-gold/80 px-2 py-1 text-xs">★ {show.rating || show.vote_average?.toFixed?.(1)}</div>
      <div className="absolute left-4 top-20 rotate-[-12deg] border-2 border-green p-2 text-green" style={{ opacity: likeOpacity }}>LIKE</div>
      <div className="absolute right-4 top-20 rotate-[12deg] border-2 border-accent p-2 text-accent" style={{ opacity: nopeOpacity }}>NOPE</div>
      <button onClick={() => setTrailerOpen(true)} className="absolute left-1/2 top-1/2 h-14 w-14 -translate-x-1/2 -translate-y-1/2 rounded-full bg-white/30">▶</button>
      <button onClick={() => setDetailOpen(true)} className="absolute bottom-40 left-1/2 h-1.5 w-12 -translate-x-1/2 rounded-full bg-white/70" />
      <div className="absolute bottom-0 w-full p-4">
        <h2 className="font-display text-5xl leading-none">{show.title}</h2>
        <p className="mt-2 text-sm italic text-gray-300">{show.tagline}</p>
      </div>
      <button onClick={onSuperLike} className="absolute bottom-28 left-1/2 -translate-x-1/2 rounded border border-gold px-2 py-1 text-xs text-gold">MUST WATCH</button>
      <DetailPanel show={show} open={detailOpen} onClose={() => setDetailOpen(false)} onLike={onSwipeRight} onNope={onSwipeLeft} memberCount={memberCount} />
      {trailerOpen && <TrailerModal trailerKey={show.trailer_key} showTitle={show.title} onClose={() => setTrailerOpen(false)} />}
    </motion.div>
  )
}
