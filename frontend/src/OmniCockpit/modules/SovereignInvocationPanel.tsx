import React, { useState } from 'react';
import { invokeSovereignManifest } from '../../lib/api';

export default function SovereignInvocationPanel() {
  const [content, setContent] = useState('');
  const [fullName, setFullName] = useState('');
  const [birthState, setBirthState] = useState('');
  const [signer, setSigner] = useState('');
  const [jurisdiction, setJurisdiction] = useState('Common Law');
  const [venue, setVenue] = useState('Land');
  const [rebuttals, setRebuttals] = useState({
    title42: true,
    ucc: false,
  });
  const [manifest, setManifest] = useState(null);

  const handleRebuttalChange = (e) => {
    setRebuttals({ ...rebuttals, [e.target.name]: e.target.checked });
  };

  async function handleInvoke() {
    const selectedRebuttals = Object.keys(rebuttals).filter(key => rebuttals[key]);
    const res = await invokeSovereignManifest({
      content,
      fullName,
      birthState,
      signer,
      jurisdiction,
      venue,
      rebuttals: selectedRebuttals,
    });
    setManifest(res.manifest);
  }

  return (
    <div>
      <h2>✨ Sovereign Invocation Flow</h2>
      <textarea placeholder="Paste content to analyze" value={content} onChange={e => setContent(e.target.value)} />
      <input placeholder="Full Name" value={fullName} onChange={e => setFullName(e.target.value)} />
      <input placeholder="Birth State" value={birthState} onChange={e => setBirthState(e.target.value)} />
      <input placeholder="Signer" value={signer} onChange={e => setSigner(e.target.value)} />
      <input placeholder="Jurisdiction" value={jurisdiction} onChange={e => setJurisdiction(e.target.value)} />
      <select value={venue} onChange={e => setVenue(e.target.value)}>
        <option value="Land">Land</option>
        <option value="Sea">Sea</option>
        <option value="Air">Air</option>
      </select>
      <div>
        <input type="checkbox" name="title42" checked={rebuttals.title42} onChange={handleRebuttalChange} />
        <label>Rebut Title 42</label>
      </div>
      <div>
        <input type="checkbox" name="ucc" checked={rebuttals.ucc} onChange={handleRebuttalChange} />
        <label>Rebut UCC</label>
      </div>
      <button onClick={handleInvoke}>Invoke Sovereign Manifest</button>
      {manifest && <pre>{JSON.stringify(manifest, null, 2)}</pre>}
    </div>
  );
}