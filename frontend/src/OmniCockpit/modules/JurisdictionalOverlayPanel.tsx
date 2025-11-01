import React, { useState } from 'react';
import { applyJurisdictionalOverlay } from '../../lib/api';

export default function JurisdictionalOverlayPanel() {
  const [venue, setVenue] = useState('Land');
  const [rebuttals, setRebuttals] = useState({
    title42: true,
    ucc: false,
  });
  const [overlay, setOverlay] = useState(null);

  const handleRebuttalChange = (e) => {
    setRebuttals({ ...rebuttals, [e.target.name]: e.target.checked });
  };

  async function handleApplyOverlay() {
    const selectedRebuttals = Object.keys(rebuttals).filter(key => rebuttals[key]);
    const res = await applyJurisdictionalOverlay({ venue, rebuttals: selectedRebuttals });
    setOverlay(res.overlay);
  }

  return (
    <div>
      <h2>🗺️ Jurisdictional Overlay (David Straight)</h2>
      <div>
        <label>Venue:</label>
        <select value={venue} onChange={e => setVenue(e.target.value)}>
          <option value="Land">Land</option>
          <option value="Sea">Sea</option>
          <option value="Air">Air</option>
        </select>
      </div>
      <div>
        <label>Rebuttals:</label>
        <div>
          <input type="checkbox" name="title42" checked={rebuttals.title42} onChange={handleRebuttalChange} />
          <label>Title 42 (Maritime)</label>
        </div>
        <div>
          <input type="checkbox" name="ucc" checked={rebuttals.ucc} onChange={handleRebuttalChange} />
          <label>UCC (Commercial)</label>
        </div>
      </div>
      <button onClick={handleApplyOverlay}>Apply Overlay</button>
      {overlay && <pre>{JSON.stringify(overlay, null, 2)}</pre>}
    </div>
  );
}