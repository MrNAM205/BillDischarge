import React, { useState, useEffect } from 'react';

interface LineageEntry {
  timestamp: string;
  module: string;
  signer: string;
  jurisdiction: string;
  overlays: string[];
  manifest_hash: string;
  exported: boolean;
  signed: boolean;
  published: boolean;
}

const SovereignLineagePanel: React.FC = () => {
  const [history, setHistory] = useState<LineageEntry[]>([]);
  const [filteredHistory, setFilteredHistory] = useState<LineageEntry[]>([]);
  const [moduleFilter, setModuleFilter] = useState('');
  const [signerFilter, setSignerFilter] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        setLoading(true);
        // This is a placeholder for the actual API call
        const response = await fetch('http://localhost:8000/api/lineage/history');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setHistory(data);
        setFilteredHistory(data);
        setError(null);
      } catch (err) {
        if (err instanceof Error) {
          setError(`Failed to fetch lineage history: ${err.message}`);
        }
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  useEffect(() => {
    let filtered = history;
    if (moduleFilter) {
      filtered = filtered.filter(entry =>
        entry.module.toLowerCase().includes(moduleFilter.toLowerCase())
      );
    }
    if (signerFilter) {
      filtered = filtered.filter(entry =>
        entry.signer.toLowerCase().includes(signerFilter.toLowerCase())
      );
    }
    setFilteredHistory(filtered);
  }, [moduleFilter, signerFilter, history]);

  const handleReplay = (entry: LineageEntry) => {
    // Placeholder for replay functionality
    console.log('Replaying invocation:', entry);
    alert(`Replaying invocation from ${entry.timestamp} by ${entry.signer}`);
  };

  if (loading) {
    return <div>Loading lineage history...</div>;
  }

  if (error) {
    return <div style={{ color: 'red' }}>{error}</div>;
  }

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h2>Sovereign Lineage Tracker</h2>
      <div style={{ marginBottom: '20px' }}>
        <input
          type="text"
          placeholder="Filter by module..."
          value={moduleFilter}
          onChange={e => setModuleFilter(e.target.value)}
          style={{ marginRight: '10px', padding: '5px' }}
        />
        <input
          type="text"
          placeholder="Filter by signer..."
          value={signerFilter}
          onChange={e => setSignerFilter(e.target.value)}
          style={{ padding: '5px' }}
        />
      </div>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: '1px solid #ccc' }}>
            <th style={{ textAlign: 'left', padding: '8px' }}>Timestamp</th>
            <th style={{ textAlign: 'left', padding: '8px' }}>Module</th>
            <th style={{ textAlign: 'left', padding: '8px' }}>Signer</th>
            <th style={{ textAlign: 'left', padding: '8px' }}>Jurisdiction</th>
            <th style={{ textAlign: 'left', padding: '8px' }}>Manifest Hash</th>
            <th style={{ textAlign: 'left', padding: '8px' }}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {filteredHistory.map((entry, index) => (
            <tr key={index} style={{ borderBottom: '1.5px solid #eee' }}>
              <td style={{ padding: '8px' }}>{new Date(entry.timestamp).toLocaleString()}</td>
              <td style={{ padding: '8px' }}>{entry.module}</td>
              <td style={{ padding: '8px' }}>{entry.signer}</td>
              <td style={{ padding: '8px' }}>{entry.jurisdiction}</td>
              <td style={{ padding: '8px' }}>{entry.manifest_hash}</td>
              <td style={{ padding: '8px' }}>
                <button onClick={() => handleReplay(entry)} style={{ padding: '5px 10px' }}>
                  Replay
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default SovereignLineagePanel;
