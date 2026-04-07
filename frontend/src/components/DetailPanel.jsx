import { motion } from 'framer-motion'
import CastRow from './CastRow'
import SoundtrackList from './SoundtrackList'
import SplitCostBadge from './SplitCostBadge'

export default function DetailPanel({ show, open, onClose, onLike, onNope, memberCount }) {
  return (
    <>
      {open && <div className="absolute inset-0 bg-black/50" onClick={onClose} />}
      <motion.div initial={false} animate={{ y: open ? 0 : '100%' }} transition={{ type: 'spring', stiffness: 400, damping: 40 }} className="absolute bottom-0 left-0 z-20 h-[72%] w-full rounded-t-3xl bg-surface p-4">
        <div className="sticky top-0 mx-auto mb-2 h-1.5 w-12 rounded-full bg-gray-400" />
        <div className="no-scrollbar h-[85%] overflow-y-auto pr-1">
          <h2 className="font-display text-4xl">{show.title}</h2>
          <p className="text-sm text-gray-300">{show.year} · {show.seasons} seasons · {show.original_language}</p>
          <p className="mt-3 text-sm leading-6">{show.overview}</p>
          <h3 className="mt-4 font-display text-2xl">Cast</h3><CastRow cast={show.cast} />
          <h3 className="mt-4 font-display text-2xl">Crew</h3>
          <div className="grid grid-cols-2 gap-2">{show.crew?.slice(0, 4).map((c, i) => <div key={i} className="rounded bg-surface2 p-2 text-xs"><div className="text-gray-400">{c.job}</div><div>{c.name}</div></div>)}</div>
          <h3 className="mt-4 font-display text-2xl">Soundtrack</h3><SoundtrackList soundtrack={show.soundtrack} />
          <h3 className="mt-4 font-display text-2xl">Available on</h3>
          <div className="flex flex-wrap gap-2">{show.platforms?.map((p, i) => <div key={i} className="rounded-full px-3 py-1 text-xs" style={{ background: `${p.color}55` }}>{p.name} · {p.type}</div>)}</div>
          {show.platforms?.filter((p) => p.type === 'rent').map((p, i) => <SplitCostBadge key={i} price={p.price || 3.99} memberCount={memberCount} availability="rent" />)}
        </div>
        <div className="mt-3 grid grid-cols-2 gap-2">
          <button className="rounded-xl bg-accent py-2" onClick={onNope}>✕ Nope</button>
          <button className="rounded-xl bg-green py-2" onClick={onLike}>♥ Like</button>
        </div>
      </motion.div>
    </>
  )
}
