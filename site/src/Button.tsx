import { useState } from "react";
import styles from "./Button.module.scss";

export const Button: React.FC = () => {
  const [count, setCount] = useState(0);

  return (
    <div className="card">
      <button onClick={() => setCount((count) => count + 1)} className={styles.button}>
        count is {count}
      </button>
      <p>
        Edit <code>src/Button.tsx</code> and save to test HMR
      </p>
    </div>
  )
}