import SwipeCard from './SwipeCard'

export default function CardStack({ shows, index, onVote, memberCount }) {
  const stack = shows.slice(index, index + 3)
  return stack.map((show, i) => (
    <div key={show.tmdb_id} className="absolute inset-0" style={{ zIndex: 3 - i, transform: i === 1 ? 'scale(0.96) translateY(14px)' : i === 2 ? 'scale(0.92) translateY(28px)' : 'none' }}>
      <SwipeCard
        show={show}
        isTop={i === 0}
        memberCount={memberCount}
        onSwipeLeft={() => i === 0 && onVote('nope')}
        onSwipeRight={() => i === 0 && onVote('like')}
        onSuperLike={() => i === 0 && onVote('super')}
      />
    </div>
  ))
}
