import Editor from "@monaco-editor/react";


const OPTIONS = {
  readOnly: false,
  minimap: { enabled: false },
  lineNumbers: "off",
}

const DEFAULT_CODE = `import numpy as np

def policy(obs: np.ndarray) -> int:
    # Write your code here
    return 0`


export default function CodeEditor() {
  return (
    <>
      <Editor 
        height="400px" 
        width="400px" 
        defaultLanguage="python" 
        defaultValue={DEFAULT_CODE}
        options={OPTIONS}
      />
    </>
  )
}
