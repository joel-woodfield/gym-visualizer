import Button from './Button';

export default function InputField({ label, value, onChange, onSubmit, buttonLabel }) {
  return (
    <>
      { onSubmit && (
        <form 
          onSubmit={(e) => {
            e.preventDefault();
            onSubmit();
          }}
          className="flex items-center gap-2"
        >
          <label className="text-sm text-gray-700">
            {label}
          </label>

          <input 
            type="text" 
            value={value}
            onChange={(e) => onChange(e.target.value)}
            className="
              px-2 py-1
              border border-gray-300
              rounded
              text-sm
              focus:outline-none focus:ring-2 focus:ring-blue-500
            "
          />

          <Button type="submit" text={buttonLabel} />
        </form>
      )}
      { !onSubmit && (
        <div className="flex items-center gap-2">
          <label className="text-sm text-gray-700">
            {label}
          </label>
          <input 
              type="text" 
              value={value}
              onChange={(e) => onChange(e.target.value)}
              className="
                px-2 py-1
                border border-gray-300
                rounded
                text-sm
                focus:outline-none focus:ring-2 focus:ring-blue-500
              "
          />
        </div>
      )}
    </>
  );
}