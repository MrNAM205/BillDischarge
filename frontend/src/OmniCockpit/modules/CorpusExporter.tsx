
import React, { useState, useEffect } from 'react';
import { fetchCorpus, exportManifest } from '../../lib/api';

export default function CorpusExporter() {
  const [corpus, setCorpus] = useState([]);
  const [selected, setSelected] = useState<string[]>([]);
  const [manifest, setManifest] = useState(null);

  useEffect(() => {
    fetchCorpus().then(setCorpus);
  }, []);

  async function handleExport() {
    const res = await exportManifest({ files: selected });
    setManifest(res.manifest);
  }

  return (
    <div>
      <h2>📦 Export Trust Manifest</h2>
      <ul>
        {corpus.map(entry => (
          <li key={entry.file}>
            <label>
              <input type="checkbox"
                checked={selected.includes(entry.file)}
                onChange={e => {
                  const checked = e.target.checked;
                  setSelected(checked
                    ? [...selected, entry.file]
                    : selected.filter(f => f !== entry.file));
                }} />
              {entry.title} — {entry.timestamp}
            </label>
          </li>
        ))}
      </ul>
      <button onClick={handleExport}>Export Manifest</button>
      {manifest && <pre>{JSON.stringify(manifest, null, 2)}</pre>}
    </div>
  );
}
