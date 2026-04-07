import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { createCircle } from '../api/client'
import { useAppStore } from '../store/useAppStore'

const platforms = ['Netflix', 'Prime Video', 'Apple TV+', 'HBO Max', 'Hulu', 'Disney+', 'Peacock', 'Tubi']
const langs = [['English', 'en'], ['Spanish', 'es'], ['Korean', 'ko'], ['French', 'fr'], ['Japanese', 'ja'], ['Hindi', 'hi'], ['German', 'de'], ['Italian', 'it'], ['Portuguese', 'pt']]

export default function SetupPage() {
  const navigate = useNavigate()
  const { selectedPlatforms, selectedLanguages, setPlatforms, setLanguages, availabilityMode, setAvailabilityMode, setCircle } = useAppStore()
  const [members, setMembers] = useState(['You'])
  const [name, setName] = useState('')

  const toggle = (arr, set, value) => set(arr.includes(value) ? arr.filter((v) => v !== value) : [...arr, value])
  const start = async () => {
    const res = await createCircle({ name: 'Binge Circle', members: members.map((m) => ({ name: m })) })
    setCircle(res.data.circle_id, res.data.members)
    navigate('/swipe')
  }

  return <div className="mx-auto max-w-[420px] p-4">
    <h1 className="font-display text-5xl">ShowSwipe</h1>
    <h2 className="mt-4">Platforms</h2>
    <div className="flex flex-wrap gap-2">{platforms.map((p) => <button key={p} onClick={() => toggle(selectedPlatforms, setPlatforms, p)} className={`rounded-full px-3 py-1 ${selectedPlatforms.includes(p) ? 'bg-accent2' : 'bg-surface2'}`}>{p}</button>)}</div>
    <h2 className="mt-4">Availability</h2>
    <div className="grid gap-2">{[['flatrate', 'Subscription only'], ['rent', 'Include rentals'], ['ads', 'Free with ads'], ['all', 'Show everything']].map(([k, l]) => <button key={k} onClick={() => setAvailabilityMode(k)} className={`rounded p-2 text-left ${availabilityMode === k ? 'bg-accent2' : 'bg-surface2'}`}>{l}</button>)}</div>
    <h2 className="mt-4">Languages</h2>
    <div className="flex flex-wrap gap-2">{langs.map(([label, code]) => <button key={code} onClick={() => toggle(selectedLanguages, setLanguages, code)} className={`rounded-full px-3 py-1 ${selectedLanguages.includes(code) ? 'bg-green' : 'bg-surface2'}`}>{label}</button>)}</div>
    <h2 className="mt-4">Your Binge Circle</h2>
    <div className="flex flex-wrap gap-2">{members.map((m) => <div className="rounded-full bg-surface2 px-3 py-1" key={m}>{m}</div>)}</div>
    <div className="mt-2 flex gap-2"><input value={name} onChange={(e) => setName(e.target.value)} className="flex-1 rounded bg-surface2 p-2" /><button onClick={() => { if (name && members.length < 6) { setMembers([...members, name]); setName('') } }} className="rounded bg-accent2 px-3">Add</button></div>
    <button onClick={start} className="mt-6 w-full rounded-xl bg-accent py-3 font-semibold">Start Swiping</button>
  </div>
}
