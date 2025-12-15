import { useState } from "react";
import Editor from "@monaco-editor/react";


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
    <div className="code-editor">
      <Editor 
        height="400px" 
        width="400px" 
        defaultLanguage="python" 
        defaultValue={DEFAULT_CODE}
        options={OPTIONS}
        onChange={(value) => setCode(value)}
      />
      <button onClick={() => onCodeSubmit(code)}>Submit code</button>
    </div>
  )
}
