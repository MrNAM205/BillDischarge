import React, { useState, useEffect } from 'react';
import { getLineageHistory } from '../../lib/api';

export default function SovereignLineagePanel() {
  const [history, setHistory] = useState([]);
  const [moduleFilter, setModuleFilter] = useState('');
  const [signerFilter, setSignerFilter] = useState('');

  async function fetchHistory() {
    const res = await getLineageHistory({ module: moduleFilter, signer: signerFilter });
    setHistory(res.history);
  }

  useEffect(() => {
    fetchHistory();
  }, []);

  return (
    <div>
      <h2>📜 Sovereign Lineage Tracker</h2>
      <div>
        <input placeholder="Filter by module" value={moduleFilter} onChange={e => setModuleFilter(e.target.value)} />
        <input placeholder="Filter by signer" value={signerFilter} onChange={e => setSignerFilter(e.target.value)} />
        <button onClick={fetchHistory}>Filter</button>
      </div>
      <pre>{JSON.stringify(history, null, 2)}</pre>
    </div>
  );
}