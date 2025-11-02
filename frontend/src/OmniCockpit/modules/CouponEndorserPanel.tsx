import React, { useState, useEffect } from 'react';
import {
  endorseCoupon,
  endorseBill,
  createPromissoryNote,
  validateNegotiability,
  getEndorsementInfo,
  getEndorsementTemplates
} from '../../lib/api';

interface EndorsementResult {
  success: boolean;
  message: string;
  endorsed_coupon?: any;
  endorsed_bill?: any;
  promissory_note?: any;
}

interface ValidationResults {
  success: boolean;
  validation_result: any;
}

export default function CouponEndorserPanel() {
  const [activeTab, setActiveTab] = useState<'coupon' | 'bill' | 'note'>('coupon');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<EndorsementResult | null>(null);
  const [validationResults, setValidationResults] = useState<ValidationResults | null>(null);
  const [endorsementInfo, setEndorsementInfo] = useState<any>(null);
  const [templates, setTemplates] = useState<any>(null);

  // Form states for coupon endorsement
  const [couponData, setCouponData] = useState({
    endorser_name: '',
    amount: '',
    payee: '',
    account_number: '',
    endorsement_type: 'private_trust',
    due_date: ''
  });

  // Form states for bill endorsement
  const [billData, setBillData] = useState({
    endorser_name: '',
    amount: '',
    creditor: '',
    bill_number: '',
    endorsement_type: 'private_trust',
    due_date: ''
  });

  // Form states for promissory note
  const [noteData, setNoteData] = useState({
    maker_name: '',
    amount: '',
    payee: '',
    note_title: 'Promissory Note',
    due_date: '',
    payable_on_demand: true,
    jurisdiction: 'Common Law'
  });

  // Form states for validation
  const [validationData, setValidationData] = useState({
    document_type: 'coupon',
    amount: '',
    payee: '',
    due_date: '',
    payable_on_demand: null
  });

  // File upload state
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [fileContent, setFileContent] = useState<string>('');

  useEffect(() => {
    loadEndorsementInfo();
    loadTemplates();
  }, []);

  const loadEndorsementInfo = async () => {
    try {
      const info = await getEndorsementInfo();
      if (info.success) {
        setEndorsementInfo(info.endorsement_info);
      }
    } catch (error) {
      console.error('Failed to load endorsement info:', error);
    }
  };

  const loadTemplates = async () => {
    try {
      const templateData = await getEndorsementTemplates();
      if (templateData.success) {
        setTemplates(templateData.templates);
      }
    } catch (error) {
      console.error('Failed to load templates:', error);
    }
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setUploadedFile(file);
      // Read file content for parsing
      const reader = new FileReader();
      reader.onload = (e) => {
        const content = e.target?.result as string;
        setFileContent(content);
        parseFileContent(content);
      };
      reader.readAsText(file);
    }
  };

  const parseFileContent = (content: string) => {
    // Simple parsing logic - in real implementation would be more sophisticated
    const lines = content.split('\n');
    const parsed: any = {};

    lines.forEach(line => {
      if (line.toLowerCase().includes('amount') || line.includes('$')) {
        const amountMatch = line.match(/\$?([\d,]+\.?\d*)/);
        if (amountMatch) parsed.amount = amountMatch[1];
      }
      if (line.toLowerCase().includes('account')) {
        const accountMatch = line.match(/account\s*#?:?\s*(\w+)/i);
        if (accountMatch) parsed.account_number = accountMatch[1];
      }
      if (line.toLowerCase().includes('pay') || line.toLowerCase().includes('payee')) {
        const payeeMatch = line.match(/pay(?:ee)?\s*:?\s*(.+)/i);
        if (payeeMatch) parsed.payee = payeeMatch[1].trim();
      }
    });

    // Update form with parsed data
    if (activeTab === 'coupon') {
      setCouponData(prev => ({ ...prev, ...parsed }));
    } else if (activeTab === 'bill') {
      setBillData(prev => ({ ...prev, ...parsed, creditor: parsed.payee || '' }));
    }
  };

  const handleEndorseCoupon = async () => {
    setLoading(true);
    setResults(null);

    try {
      const result = await endorseCoupon(couponData);
      setResults(result);
    } catch (error) {
      setResults({
        success: false,
        message: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`
      });
    } finally {
      setLoading(false);
    }
  };

  const handleEndorseBill = async () => {
    setLoading(true);
    setResults(null);

    try {
      const result = await endorseBill(billData);
      setResults(result);
    } catch (error) {
      setResults({
        success: false,
        message: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`
      });
    } finally {
      setLoading(false);
    }
  };

  const handleCreateNote = async () => {
    setLoading(true);
    setResults(null);

    try {
      const result = await createPromissoryNote(noteData);
      setResults(result);
    } catch (error) {
      setResults({
        success: false,
        message: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`
      });
    } finally {
      setLoading(false);
    }
  };

  const handleValidateNegotiability = async () => {
    setLoading(true);
    setValidationResults(null);

    try {
      const result = await validateNegotiability(validationData);
      setValidationResults(result);
    } catch (error) {
      setValidationResults({
        success: false,
        validation_result: { error: error instanceof Error ? error.message : 'Unknown error' }
      });
    } finally {
      setLoading(false);
    }
  };

  const loadTemplate = (templateType: string) => {
    if (templates && templates[`${templateType}_template`]) {
      const template = templates[`${templateType}_template`];

      if (templateType === 'coupon_endorsement') {
        setCouponData(template);
      } else if (templateType === 'bill_endorsement') {
        setBillData(template);
      } else if (templateType === 'promissory_note') {
        setNoteData(template);
      }
    }
  };

  const renderCouponForm = () => (
    <div className="form-section">
      <h3>📄 Payment Coupon Endorsement (UCC 3-305)</h3>

      <div className="file-upload-section">
        <label>Upload Billing Statement (Optional):</label>
        <input type="file" accept=".txt,.pdf,.doc,.docx" onChange={handleFileUpload} />
        {uploadedFile && <span className="file-name">{uploadedFile.name}</span>}
      </div>

      <div className="form-grid">
        <input
          placeholder="Your Full Name"
          value={couponData.endorser_name}
          onChange={e => setCouponData(prev => ({ ...prev, endorser_name: e.target.value }))}
        />
        <input
          placeholder="Amount (e.g., 150.00)"
          value={couponData.amount}
          onChange={e => setCouponData(prev => ({ ...prev, amount: e.target.value }))}
        />
        <input
          placeholder="Payee Name"
          value={couponData.payee}
          onChange={e => setCouponData(prev => ({ ...prev, payee: e.target.value }))}
        />
        <input
          placeholder="Account Number"
          value={couponData.account_number}
          onChange={e => setCouponData(prev => ({ ...prev, account_number: e.target.value }))}
        />
        <select
          value={couponData.endorsement_type}
          onChange={e => setCouponData(prev => ({ ...prev, endorsement_type: e.target.value }))}
        >
          <option value="private_trust">Private Trust Endorsement</option>
          <option value="acceptance_for_value">Acceptance for Value</option>
        </select>
        <input
          type="date"
          placeholder="Due Date (Optional)"
          value={couponData.due_date}
          onChange={e => setCouponData(prev => ({ ...prev, due_date: e.target.value }))}
        />
      </div>

      <div className="template-buttons">
        <button onClick={() => loadTemplate('coupon_endorsement')} type="button">
          Load Template
        </button>
        <button onClick={handleValidateNegotiability} type="button" disabled={loading}>
          Validate Negotiability
        </button>
      </div>

      <button
        onClick={handleEndorseCoupon}
        disabled={loading || !couponData.endorser_name || !couponData.amount}
        className="primary-button"
      >
        {loading ? 'Processing...' : 'Endorse Coupon'}
      </button>
    </div>
  );

  const renderBillForm = () => (
    <div className="form-section">
      <h3>🧾 Bill Endorsement</h3>

      <div className="form-grid">
        <input
          placeholder="Your Full Name"
          value={billData.endorser_name}
          onChange={e => setBillData(prev => ({ ...prev, endorser_name: e.target.value }))}
        />
        <input
          placeholder="Bill Amount (e.g., 250.00)"
          value={billData.amount}
          onChange={e => setBillData(prev => ({ ...prev, amount: e.target.value }))}
        />
        <input
          placeholder="Creditor Name"
          value={billData.creditor}
          onChange={e => setBillData(prev => ({ ...prev, creditor: e.target.value }))}
        />
        <input
          placeholder="Bill Number/Reference"
          value={billData.bill_number}
          onChange={e => setBillData(prev => ({ ...prev, bill_number: e.target.value }))}
        />
        <select
          value={billData.endorsement_type}
          onChange={e => setBillData(prev => ({ ...prev, endorsement_type: e.target.value }))}
        >
          <option value="private_trust">Private Trust Endorsement</option>
          <option value="acceptance_for_value">Acceptance for Value</option>
        </select>
        <input
          type="date"
          placeholder="Due Date (Optional)"
          value={billData.due_date}
          onChange={e => setBillData(prev => ({ ...prev, due_date: e.target.value }))}
        />
      </div>

      <div className="template-buttons">
        <button onClick={() => loadTemplate('bill_endorsement')} type="button">
          Load Template
        </button>
      </div>

      <button
        onClick={handleEndorseBill}
        disabled={loading || !billData.endorser_name || !billData.amount}
        className="primary-button"
      >
        {loading ? 'Processing...' : 'Endorse Bill'}
      </button>
    </div>
  );

  const renderNoteForm = () => (
    <div className="form-section">
      <h3>📝 Promissory Note Creation (UCC 3-104)</h3>

      <div className="form-grid">
        <input
          placeholder="Maker Name (Your Name)"
          value={noteData.maker_name}
          onChange={e => setNoteData(prev => ({ ...prev, maker_name: e.target.value }))}
        />
        <input
          placeholder="Note Amount (e.g., 1000.00)"
          value={noteData.amount}
          onChange={e => setNoteData(prev => ({ ...prev, amount: e.target.value }))}
        />
        <input
          placeholder="Payee Name"
          value={noteData.payee}
          onChange={e => setNoteData(prev => ({ ...prev, payee: e.target.value }))}
        />
        <input
          placeholder="Note Title"
          value={noteData.note_title}
          onChange={e => setNoteData(prev => ({ ...prev, note_title: e.target.value }))}
        />
        <select
          value={noteData.jurisdiction}
          onChange={e => setNoteData(prev => ({ ...prev, jurisdiction: e.target.value }))}
        >
          <option value="Common Law">Common Law</option>
          <option value="State Court">State Court</option>
          <option value="Federal">Federal</option>
        </select>
      </div>

      <div className="checkbox-section">
        <label>
          <input
            type="checkbox"
            checked={noteData.payable_on_demand}
            onChange={e => setNoteData(prev => ({ ...prev, payable_on_demand: e.target.checked }))}
          />
          Payable on Demand
        </label>
        {!noteData.payable_on_demand && (
          <input
            type="date"
            placeholder="Due Date"
            value={noteData.due_date}
            onChange={e => setNoteData(prev => ({ ...prev, due_date: e.target.value }))}
          />
        )}
      </div>

      <div className="template-buttons">
        <button onClick={() => loadTemplate('promissory_note')} type="button">
          Load Template
        </button>
      </div>

      <button
        onClick={handleCreateNote}
        disabled={loading || !noteData.maker_name || !noteData.amount || !noteData.payee}
        className="primary-button"
      >
        {loading ? 'Processing...' : 'Create Promissory Note'}
      </button>
    </div>
  );

  const renderValidationResults = () => {
    if (!validationResults) return null;

    const { validation_result } = validationResults;

    return (
      <div className="validation-results">
        <h4>🔍 Negotiability Validation Results</h4>
        <div className={`validation-status ${validation_result.ucc_3_104_compliance ? 'compliant' : 'non-compliant'}`}>
          UCC 3-104 Compliance: {validation_result.ucc_3_104_compliance ? '✅ COMPLIANT' : '❌ NON-COMPLIANT'}
        </div>

        {validation_result.validation_checks && (
          <div className="validation-checks">
            <h5>Validation Checks:</h5>
            {Object.entries(validation_result.validation_checks).map(([check, passed]) => (
              <div key={check} className={`check-item ${passed ? 'passed' : 'failed'}`}>
                {check.replace(/_/g, ' ').toUpperCase()}: {passed ? '✅' : '❌'}
              </div>
            ))}
          </div>
        )}

        {validation_result.issues && validation_result.issues.length > 0 && (
          <div className="validation-issues">
            <h5>Issues Found:</h5>
            {validation_result.issues.map((issue, index) => (
              <div key={index} className="issue-item">❌ {issue}</div>
            ))}
          </div>
        )}

        {validation_result.recommendations && validation_result.recommendations.length > 0 && (
          <div className="validation-recommendations">
            <h5>Recommendations:</h5>
            {validation_result.recommendations.map((rec, index) => (
              <div key={index} className="recommendation-item">💡 {rec}</div>
            ))}
          </div>
        )}
      </div>
    );
  };

  const renderResults = () => {
    if (!results) return null;

    return (
      <div className={`results ${results.success ? 'success' : 'error'}`}>
        <h4>{results.success ? '✅ Endorsement Successful' : '❌ Endorsement Failed'}</h4>
        <p>{results.message}</p>

        {results.success && (
          <div className="endorsement-details">
            {results.endorsed_coupon && (
              <div className="detail-section">
                <h5>📄 Endorsed Coupon Details:</h5>
                <div className="semantic-lineage">
                  <strong>Trust Corpus:</strong> {results.endorsed_coupon.semantic_lineage?.trust_corpus}
                </div>
                <div className="ucc-compliance">
                  <strong>UCC Compliance:</strong> {Object.keys(results.endorsed_coupon.ucc_compliance || {}).join(', ')}
                </div>
                <div className="endorsement-text">
                  <strong>Endorsement Text:</strong>
                  <pre>{results.endorsed_coupon.endorsement_text}</pre>
                </div>
              </div>
            )}

            {results.endorsed_bill && (
              <div className="detail-section">
                <h5>🧾 Endorsed Bill Details:</h5>
                <div className="trust-corpus">
                  <strong>Trust Corpus:</strong> {results.endorsed_bill.trust_corpus?.trust_name}
                </div>
                <div className="endorsement-text">
                  <strong>Endorsement Text:</strong>
                  <pre>{results.endorsed_bill.endorsement_text}</pre>
                </div>
              </div>
            )}

            {results.promissory_note && (
              <div className="detail-section">
                <h5>📝 Promissory Note Details:</h5>
                <div className="authorship-declaration">
                  <strong>Author:</strong> {results.promissory_note.authorship_declaration?.author}
                </div>
                <div className="note-content">
                  <strong>Note Content:</strong>
                  <pre>{results.promissory_note.note_content}</pre>
                </div>
              </div>
            )}

            <div className="export-section">
              <button className="export-button">
                📥 Export as PDF
              </button>
              <button className="export-button">
                📄 Copy to Clipboard
              </button>
            </div>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="coupon-endorser-panel">
      <div className="panel-header">
        <h2>🏛️ Coupon Endorser (Brandon Joe Williams)</h2>
        <p>Endorse financial instruments into private trust using UCC 3-305 provisions</p>
      </div>

      {endorsementInfo && (
        <div className="info-section">
          <h3>📚 Endorsement Information</h3>
          <div className="ucc-provisions">
            <strong>UCC Provisions:</strong> {endorsementInfo.ucc_provisions ?
              Object.entries(endorsementInfo.ucc_provisions).map(([key, value]) =>
                `${key}: ${value}`).join(', ') : 'Loading...'}
          </div>
        </div>
      )}

      <div className="tab-navigation">
        <button
          className={`tab ${activeTab === 'coupon' ? 'active' : ''}`}
          onClick={() => setActiveTab('coupon')}
        >
          📄 Coupon Endorsement
        </button>
        <button
          className={`tab ${activeTab === 'bill' ? 'active' : ''}`}
          onClick={() => setActiveTab('bill')}
        >
          🧾 Bill Endorsement
        </button>
        <button
          className={`tab ${activeTab === 'note' ? 'active' : ''}`}
          onClick={() => setActiveTab('note')}
        >
          📝 Promissory Note
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'coupon' && renderCouponForm()}
        {activeTab === 'bill' && renderBillForm()}
        {activeTab === 'note' && renderNoteForm()}
      </div>

      {renderValidationResults()}
      {renderResults()}

      <div className="panel-footer">
        <div className="help-text">
          <p>💡 <strong>Tips:</strong></p>
          <ul>
            <li>Upload billing statements to auto-fill form fields</li>
            <li>Validate negotiability before endorsement</li>
            <li>Private Trust endorsement establishes settlement authority</li>
            <li>All endorsements include semantic lineage tracking</li>
          </ul>
        </div>
      </div>

      <style jsx>{`
        .coupon-endorser-panel {
          max-width: 1200px;
          margin: 0 auto;
          padding: 20px;
          font-family: Arial, sans-serif;
        }

        .panel-header {
          text-align: center;
          margin-bottom: 30px;
        }

        .info-section {
          background: #f5f5f5;
          padding: 15px;
          border-radius: 8px;
          margin-bottom: 20px;
        }

        .tab-navigation {
          display: flex;
          margin-bottom: 20px;
          border-bottom: 2px solid #ddd;
        }

        .tab {
          padding: 12px 24px;
          border: none;
          background: none;
          cursor: pointer;
          border-bottom: 2px solid transparent;
          transition: all 0.3s;
        }

        .tab.active {
          border-bottom-color: #007bff;
          color: #007bff;
        }

        .form-section {
          background: white;
          padding: 20px;
          border-radius: 8px;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
          margin-bottom: 20px;
        }

        .file-upload-section {
          margin-bottom: 20px;
          padding: 15px;
          border: 2px dashed #ddd;
          border-radius: 8px;
          text-align: center;
        }

        .form-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 15px;
          margin-bottom: 20px;
        }

        .form-grid input, .form-grid select {
          padding: 10px;
          border: 1px solid #ddd;
          border-radius: 4px;
          font-size: 14px;
        }

        .checkbox-section {
          margin: 15px 0;
          display: flex;
          align-items: center;
          gap: 15px;
        }

        .checkbox-section label {
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .template-buttons {
          display: flex;
          gap: 10px;
          margin-bottom: 20px;
        }

        .primary-button {
          background: #007bff;
          color: white;
          border: none;
          padding: 12px 24px;
          border-radius: 4px;
          cursor: pointer;
          font-size: 16px;
        }

        .primary-button:disabled {
          background: #ccc;
          cursor: not-allowed;
        }

        .validation-results {
          background: #f8f9fa;
          padding: 20px;
          border-radius: 8px;
          margin: 20px 0;
        }

        .validation-status.compliant {
          color: #28a745;
          font-weight: bold;
        }

        .validation-status.non-compliant {
          color: #dc3545;
          font-weight: bold;
        }

        .results {
          padding: 20px;
          border-radius: 8px;
          margin: 20px 0;
        }

        .results.success {
          background: #d4edda;
          border: 1px solid #c3e6cb;
        }

        .results.error {
          background: #f8d7da;
          border: 1px solid #f5c6cb;
        }

        .detail-section {
          margin-top: 15px;
          padding: 15px;
          background: white;
          border-radius: 6px;
        }

        .endorsement-text pre {
          background: #f8f9fa;
          padding: 15px;
          border-radius: 4px;
          overflow-x: auto;
          white-space: pre-wrap;
        }

        .export-section {
          display: flex;
          gap: 10px;
          margin-top: 15px;
        }

        .export-button {
          background: #28a745;
          color: white;
          border: none;
          padding: 8px 16px;
          border-radius: 4px;
          cursor: pointer;
        }

        .panel-footer {
          margin-top: 30px;
          padding-top: 20px;
          border-top: 1px solid #ddd;
        }

        .help-text ul {
          text-align: left;
          max-width: 600px;
          margin: 10px auto;
        }

        .check-item, .issue-item, .recommendation-item {
          margin: 5px 0;
          padding: 5px 10px;
          border-radius: 4px;
        }

        .check-item.passed {
          background: #d4edda;
        }

        .check-item.failed {
          background: #f8d7da;
        }

        .issue-item {
          background: #f8d7da;
        }

        .recommendation-item {
          background: #d1ecf1;
        }
      `}</style>
    </div>
  );
}