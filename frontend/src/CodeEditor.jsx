import { useState } from "react";
import Editor from "@monaco-editor/react";

import Button from "./ui/Button";

const OPTIONS = {
  readOnly: false,
  minimap: { enabled: false },
  lineNumbers: "off",
}

const DEFAULT_CODE = `import numpy as np

def policy(obs: np.ndarray, num_actions: int) -> int:
    # Write your code here
    action = np.random.randint(0, num_actions)
    return action`


export default function CodeEditor({ onCodeSubmit }) {
  const [code, setCode] = useState(DEFAULT_CODE);

  return (
    <div className="min-h-0 min-w-0 grid grid-rows-[1fr_auto] border-l-2 border-gray-200">
      <div className="min-h-0 min-w-0">
        <Editor 
          defaultLanguage="python" 
          defaultValue={DEFAULT_CODE}
          options={OPTIONS}
          onChange={(value) => setCode(value)}
        />
      </div>
      
      <Button onClick={() => onCodeSubmit(code)} text="Submit code" />
    </div>
  )
}
