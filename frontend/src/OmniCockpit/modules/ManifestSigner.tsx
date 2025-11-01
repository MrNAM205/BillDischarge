
import React, { useState } from 'react';
import { signManifest } from '../../lib/api';

export default function ManifestSigner() {
  const [filename, setFilename] = useState('');
  const [privateKey, setPrivateKey] = useState('');
  const [signed, setSigned] = useState(null);

  async function handleSign() {
    const res = await signManifest({ filename, privateKey });
    setSigned(res.signedManifest);
  }

  return (
    <div>
      <h2>🔐 Sign Trust Manifest</h2>
      <input placeholder="Manifest Filename" value={filename}
        onChange={e => setFilename(e.target.value)} />
      <input placeholder="Private Key" value={privateKey}
        onChange={e => setPrivateKey(e.target.value)} />
      <button onClick={handleSign}>Sign Manifest</button>
      {signed && <pre>{JSON.stringify(signed, null, 2)}</pre>}
    </div>
  );
}
