export default function Button({ text, onClick, type = "button" }) {
  return (
    <button
      onClick={onClick}
      className="
        px-4 py-2
        rounded-md
        bg-blue-600
        text-white text-sm font-medium
        hover:bg-blue-700
        active:bg-blue-800
        transition
      "
      type={type}
    >
      {text}
    </button>
  )
}