import { useEffect, useMemo, useRef, useState } from 'react'
import { useAnimation } from 'framer-motion'

const clamp = (n, min, max) => Math.max(min, Math.min(max, n))

export function useSwipe(cardRef, onSwipeLeft, onSwipeRight, threshold = 80) {
  const controls = useAnimation()
  const [dragX, setDragX] = useState(0)
  const [isDragging, setIsDragging] = useState(false)
  const startX = useRef(0)

  useEffect(() => {
    const node = cardRef.current
    if (!node) return

    const getX = (e) => ('touches' in e ? e.touches[0]?.clientX : e.clientX)
    const start = (e) => { setIsDragging(true); startX.current = getX(e) }
    const move = (e) => {
      if (!isDragging) return
      const x = getX(e)
      const delta = x - startX.current
      setDragX(delta)
      node.style.transform = `translateX(${delta}px) rotate(${delta * 0.04}deg)`
    }
    const end = async () => {
      if (!isDragging) return
      setIsDragging(false)
      if (dragX > threshold) onSwipeRight?.()
      else if (dragX < -threshold) onSwipeLeft?.()
      await controls.start({ x: 0, rotate: 0, transition: { type: 'spring', stiffness: 300, damping: 30 } })
      node.style.transform = 'translateX(0px) rotate(0deg)'
      setDragX(0)
    }

    node.addEventListener('mousedown', start)
    window.addEventListener('mousemove', move)
    window.addEventListener('mouseup', end)
    node.addEventListener('touchstart', start)
    window.addEventListener('touchmove', move)
    window.addEventListener('touchend', end)
    return () => {
      node.removeEventListener('mousedown', start)
      window.removeEventListener('mousemove', move)
      window.removeEventListener('mouseup', end)
      node.removeEventListener('touchstart', start)
      window.removeEventListener('touchmove', move)
      window.removeEventListener('touchend', end)
    }
  }, [cardRef, controls, dragX, isDragging, onSwipeLeft, onSwipeRight, threshold])

  return useMemo(() => ({
    dragX,
    isDragging,
    likeOpacity: clamp(dragX / 70, 0, 1),
    nopeOpacity: clamp(-dragX / 70, 0, 1),
    controls,
  }), [dragX, isDragging, controls])
}
