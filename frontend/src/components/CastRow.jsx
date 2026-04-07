export default function CastRow({ cast = [] }) {
  return (
    <div className="no-scrollbar flex gap-3 overflow-x-auto">
      {cast.map((c) => (
        <div key={c.id} className="w-20 shrink-0 text-center text-xs">
          {c.profile_url ? <img src={c.profile_url} className="mx-auto h-14 w-14 rounded-full object-cover" /> : <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-surface2">{c.name?.slice(0, 2)}</div>}
          <div className="mt-1 truncate">{c.name}</div>
          <div className="truncate text-gray-400">{c.character}</div>
        </div>
      ))}
    </div>
  )
}
