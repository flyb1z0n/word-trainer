import { useState } from "react";

import "./App.css";
import { Button } from "./Button";
import { retrieveLaunchParams } from "@telegram-apps/sdk";

function App() {
  const [count, setCount] = useState(0);

  const { tgWebAppData } = retrieveLaunchParams();

  return (
    <>
      <div>{JSON.stringify(tgWebAppData)}</div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>

      <Button />
    </>
  );
}

export default App;
