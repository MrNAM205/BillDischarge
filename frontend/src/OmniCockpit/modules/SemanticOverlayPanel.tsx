import React, { useState } from 'react';
import { scanSemantics } from '../../lib/api';

export default function SemanticOverlayPanel() {
  const [content, setContent] = useState('');
  const [flags, setFlags] = useState([]);

  async function handleScan() {
    const res = await scanSemantics({ content });
    setFlags(res.flags);
  }

  return (
    <div>
      <h2>🧠 Semantic Overlay Scanner</h2>
      <textarea placeholder="Paste corpus entry or manifest here"
        value={content}
        onChange={e => setContent(e.target.value)} />
      <button onClick={handleScan}>Scan for Adhesion Traps</button>
      <ul>
        {flags.map((f, i) => (
          <li key={i}>
            <strong>{f.term}</strong>: {f.message}
          </li>
        ))}
      </ul>
    </div>
  );
}