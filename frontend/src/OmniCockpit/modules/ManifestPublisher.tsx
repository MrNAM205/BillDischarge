
import React, { useState } from 'react';
import { publishManifest } from '../../lib/api';

export default function ManifestPublisher() {
  const [filename, setFilename] = useState('');
  const [registryUrl, setRegistryUrl] = useState('');
  const [receipt, setReceipt] = useState(null);

  async function handlePublish() {
    const res = await publishManifest({ filename, registryUrl });
    setReceipt(res.receipt);
  }

  return (
    <div>
      <h2>🌐 Publish Signed Manifest</h2>
      <input placeholder="Signed Manifest Filename" value={filename}
        onChange={e => setFilename(e.target.value)} />
      <input placeholder="Registry URL" value={registryUrl}
        onChange={e => setRegistryUrl(e.target.value)} />
      <button onClick={handlePublish}>Publish</button>
      {receipt && <pre>{JSON.stringify(receipt, null, 2)}</pre>}
    </div>
  );
}
