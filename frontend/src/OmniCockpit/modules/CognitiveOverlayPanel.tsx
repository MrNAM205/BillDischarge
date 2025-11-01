import React, { useState } from 'react';
import { scanCognitive } from '../../lib/api';

export default function CognitiveOverlayPanel() {
  const [content, setContent] = useState('');
  const [overlay, setOverlay] = useState(null);

  async function handleScan() {
    const res = await scanCognitive({ content });
    setOverlay(res.overlay);
  }

  return (
    <div>
      <h2>🧠 Cognitive Overlay Scanner (Carl Miller)</h2>
      <textarea placeholder="Paste corpus entry or manifest here"
        value={content}
        onChange={e => setContent(e.target.value)} />
      <button onClick={handleScan}>Scan for Narrative Traps</button>
      {overlay && <pre>{JSON.stringify(overlay, null, 2)}</pre>}
    </div>
  );
}