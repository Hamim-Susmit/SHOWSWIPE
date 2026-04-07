export default function ActionBar({ onNope, onLike, onSuper }) {
  return <div className="mt-4 grid grid-cols-5 gap-2 text-sm"><button>↩</button><button onClick={onNope}>✕</button><button onClick={onLike}>♥</button><button onClick={onSuper}>★</button><button>ℹ</button></div>
}
