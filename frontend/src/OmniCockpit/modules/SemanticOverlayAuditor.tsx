import React, { useState } from 'react';
import { auditSemantics } from '../../lib/api';

export default function SemanticOverlayAuditor() {
  const [content, setContent] = useState('');
  const [report, setReport] = useState(null);

  async function handleAudit() {
    const res = await auditSemantics({ content });
    setReport(res.report);
  }

  return (
    <div>
      <h2>📑 Semantic Lineage Report</h2>
      <textarea placeholder="Paste corpus entry or manifest here"
        value={content}
        onChange={e => setContent(e.target.value)} />
      <button onClick={handleAudit}>Generate Audit</button>
      {report && <pre>{JSON.stringify(report, null, 2)}</pre>}
    </div>
  );
}