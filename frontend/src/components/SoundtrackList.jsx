export default function SoundtrackList({ soundtrack = [] }) {
  if (!soundtrack.length) return null
  return soundtrack.map((song, i) => (
    <div key={`${song.title}-${i}`} className="flex items-center justify-between py-2 text-sm">
      <div>{i + 1}. {song.title} · {song.artist}</div>
      <div className="flex gap-2">
        <a className="rounded-full bg-spotify px-2" href={song.spotify_url} target="_blank" rel="noopener">♫</a>
        <a className="rounded-full bg-youtube px-2" href={song.youtube_url} target="_blank" rel="noopener">▶</a>
      </div>
    </div>
  ))
}
