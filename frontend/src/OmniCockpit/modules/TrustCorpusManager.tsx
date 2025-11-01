
import React, { useState, useEffect } from 'react';
import { fetchCorpus, addToCorpus } from '../../lib/api';

export default function TrustCorpusManager() {
  const [corpus, setCorpus] = useState([]);
  const [newEntry, setNewEntry] = useState({ title: '', content: '' });

  useEffect(() => {
    fetchCorpus().then(setCorpus);
  }, []);

  async function handleAdd() {
    const res = await addToCorpus(newEntry);
    setCorpus([...corpus, res.entry]);
    setNewEntry({ title: '', content: '' });
  }

  return (
    <div>
      <h2>📂 Trust Corpus Manager</h2>
      <input placeholder="Instrument Title" value={newEntry.title}
        onChange={e => setNewEntry({ ...newEntry, title: e.target.value })} />
      <textarea placeholder="YAML or JSON Instrument"
        value={newEntry.content}
        onChange={e => setNewEntry({ ...newEntry, content: e.target.value })} />
      <button onClick={handleAdd}>Add to Corpus</button>

      <h3>📜 Stored Instruments</h3>
      <ul>
        {corpus.map((entry, i) => (
          <li key={i}>
            <strong>{entry.title}</strong> — {entry.timestamp}
          </li>
        ))}
      </ul>
    </div>
  );
}
