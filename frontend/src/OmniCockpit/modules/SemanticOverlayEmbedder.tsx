import React, { useState } from 'react';
import { embedSemantics } from '../../lib/api';

export default function SemanticOverlayEmbedder() {
  const [content, setContent] = useState('');
  const [embedded, setEmbedded] = useState('');

  async function handleEmbed() {
    const res = await embedSemantics({ content });
    setEmbedded(res.embeddedContent);
  }

  return (
    <div>
      <h2>🧬 Embed Semantic Rebuttals</h2>
      <textarea placeholder="Paste corpus entry or manifest here"
        value={content}
        onChange={e => setContent(e.target.value)} />
      <button onClick={handleEmbed}>Inject Rebuttals</button>
      {embedded && <pre>{embedded}</pre>}
    </div>
  );
}