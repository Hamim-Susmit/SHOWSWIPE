import { AnimatePresence, motion } from 'framer-motion'
import { useEffect } from 'react'

export default function TrailerModal({ trailerKey, showTitle, onClose }) {
  useEffect(() => {
    const onEsc = (e) => e.key === 'Escape' && onClose()
    window.addEventListener('keydown', onEsc)
    return () => window.removeEventListener('keydown', onEsc)
  }, [onClose])

  return (
    <AnimatePresence>
      <motion.div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
        <button className="absolute right-4 top-4 text-2xl" onClick={onClose}>×</button>
        {!trailerKey ? <div>Trailer not available</div> : (
          <motion.iframe
            initial={{ scale: 0.9 }}
            animate={{ scale: 1 }}
            className="h-64 w-full max-w-3xl rounded-xl"
            src={`https://www.youtube.com/embed/${trailerKey}?autoplay=1&rel=0&modestbranding=1`}
            title={`${showTitle} trailer`}
            allow="autoplay; encrypted-media"
            allowFullScreen
          />
        )}
      </motion.div>
    </AnimatePresence>
  )
}
