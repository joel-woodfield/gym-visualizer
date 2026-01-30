export default function ControlButton({ icon, onClick }) {
  return (
    <button
      onClick={onClick}
      className="
        w-12 h-12
        flex items-center justify-center
        rounded-md
        bg-gray-50
        text-gray-700
        hover:bg-gray-100
        active:bg-gray-200
        focus:outline-none focus:ring-2 focus:ring-blue-500
        transition
      "
    >
      <span className="text-2xl leading-none select-none">
        {icon}
      </span>
    </button>
  );
}
