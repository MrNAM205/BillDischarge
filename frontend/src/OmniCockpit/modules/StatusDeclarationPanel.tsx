import React, { useState } from 'react';
import { declareStatus } from '../../lib/api';

export default function StatusDeclarationPanel() {
  const [fullName, setFullName] = useState('');
  const [birthState, setBirthState] = useState('');
  const [signer, setSigner] = useState('');
  const [jurisdiction, setJurisdiction] = useState('Common Law');
  const [privateKey, setPrivateKey] = useState('');
  const [declaration, setDeclaration] = useState(null);

  async function handleDeclare() {
    const res = await declareStatus({ fullName, birthState, signer, jurisdiction, privateKey });
    setDeclaration(res.declaration);
  }

  return (
    <div>
      <h2>🏛️ Status Declaration (Brandon Joe Williams)</h2>
      <input placeholder="Full Name (e.g., John Henry Doe)" value={fullName}
        onChange={e => setFullName(e.target.value)} />
      <input placeholder="State of Birth" value={birthState}
        onChange={e => setBirthState(e.target.value)} />
      <input placeholder="Signer (e.g., by, for, Author)" value={signer}
        onChange={e => setSigner(e.target.value)} />
      <input placeholder="Jurisdiction" value={jurisdiction}
        onChange={e => setJurisdiction(e.target.value)} />
      <textarea placeholder="Private Key for Signing" value={privateKey}
        onChange={e => setPrivateKey(e.target.value)} />
      <button onClick={handleDeclare}>Generate & Sign Declaration</button>
      {declaration && <pre>{JSON.stringify(declaration, null, 2)}</pre>}
    </div>
  );
}