import { useEffect, useRef, useState } from 'react'
import { useCircleStore } from '../store/useCircleStore'

export function useCircleWS(circleId) {
  const [isConnected, setConnected] = useState(false)
  const [lastEvent, setLastEvent] = useState(null)
  const retry = useRef(0)
  const { pushActivity, addMatch } = useCircleStore()

  useEffect(() => {
    if (!circleId) return
    let ws
    let cancelled = false

    const connect = () => {
      ws = new WebSocket(`ws://localhost:8000/ws/circle/${circleId}`)
      ws.onopen = () => { retry.current = 0; setConnected(true) }
      ws.onmessage = (msg) => {
        const event = JSON.parse(msg.data)
        setLastEvent(event)
        if (event.event === 'vote') pushActivity(event)
        if (event.event === 'match') {
          addMatch({ title: event.show_title, match_pct: event.match_pct, likers: event.likers })
          pushActivity(event)
        }
      }
      ws.onclose = () => {
        setConnected(false)
        if (!cancelled) {
          const timeout = Math.min(1000 * 2 ** retry.current, 10000)
          retry.current += 1
          setTimeout(connect, timeout)
        }
      }
    }

    connect()
    return () => { cancelled = true; ws?.close() }
  }, [circleId, pushActivity, addMatch])

  return { isConnected, lastEvent }
}
