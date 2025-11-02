import React, { useState, useEffect } from 'react';
import {
  scanDocument,
  detectTraps,
  generateRebuttal,
  getCommonTrapPatterns,
  getSemanticAnalysisInfo
} from '../../lib/api';

interface ScanResult {
  success: boolean;
  message: string;
  semantic_analysis?: {
    institutional_framing: any[];
    semantic_traps: any[];
    summary: {
      total_framing_detected: number;
      total_traps_detected: number;
      document_risk_level: string;
      high_severity_items: number;
    };
  };
}

interface RebuttalResult {
  success: boolean;
  message: string;
  narrative_rebuttal?: {
    rebuttal_sections: Array<{
      title: string;
      content: string;
    }>;
    semantic_lineage: {
      author: string;
      basis: string;
      authority: string;
    };
  };
}

export default function SemanticWarfarePanel() {
  const [activeTab, setActiveTab] = useState<'scan' | 'rebuttal' | 'education'>('scan');
  const [loading, setLoading] = useState(false);
  const [scanResults, setScanResults] = useState<ScanResult | null>(null);
  const [rebuttalResult, setRebuttalResult] = useState<RebuttalResult | null>(null);
  const [commonPatterns, setCommonPatterns] = useState<any>(null);
  const [analysisInfo, setAnalysisInfo] = useState<any>(null);

  // Form states
  const [documentText, setDocumentText] = useState('');
  const [scanType, setScanType] = useState('comprehensive');
  const [severityThreshold, setSeverityThreshold] = useState('low');
  const [includeSignatoryBlock, setIncludeSignatoryBlock] = useState(false);
  const [signatoryName, setSignatoryName] = useState('');
  const [jurisdiction, setJurisdiction] = useState('Common Law');

  // File upload state
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);

  useEffect(() => {
    loadCommonPatterns();
    loadAnalysisInfo();
  }, []);

  const loadCommonPatterns = async () => {
    try {
      const result = await getCommonTrapPatterns();
      if (result.success) {
        setCommonPatterns(result.common_patterns);
      }
    } catch (error) {
      console.error('Failed to load common patterns:', error);
    }
  };

  const loadAnalysisInfo = async () => {
    try {
      const result = await getSemanticAnalysisInfo();
      if (result.success) {
        setAnalysisInfo(result.analysis_info);
      }
    } catch (error) {
      console.error('Failed to load analysis info:', error);
    }
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setUploadedFile(file);
      const reader = new FileReader();
      reader.onload = (e) => {
        const content = e.target?.result as string;
        setDocumentText(content);
      };
      reader.readAsText(file);
    }
  };

  const handleScanDocument = async () => {
    if (!documentText.trim()) {
      alert('Please enter document text or upload a file');
      return;
    }

    setLoading(true);
    setScanResults(null);

    try {
      const result = await scanDocument({
        document_text: documentText,
        scan_type: scanType
      });
      setScanResults(result);
    } catch (error) {
      setScanResults({
        success: false,
        message: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`
      });
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateRebuttal = async () => {
    if (!scanResults?.semantic_analysis) {
      alert('Please scan a document first to generate analysis');
      return;
    }

    setLoading(true);
    setRebuttalResult(null);

    try {
      const result = await generateRebuttal({
        semantic_analysis: scanResults.semantic_analysis,
        custom_parameters: {
          include_signatory_block: includeSignatoryBlock,
          signatory_name: signatoryName || 'SOVEREIGN INDIVIDUAL',
          jurisdiction: jurisdiction
        }
      });
      setRebuttalResult(result);
    } catch (error) {
      setRebuttalResult({
        success: false,
        message: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`
      });
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high': return '#dc3545';
      case 'medium': return '#ffc107';
      case 'low': return '#28a745';
      default: return '#6c757d';
    }
  };

  const getRiskLevelColor = (riskLevel: string) => {
    switch (riskLevel) {
      case 'high_risk_adhesion': return '#dc3545';
      case 'moderate_semantic_warfare': return '#ffc107';
      case 'low_level_framing': return '#28a745';
      case 'minimal_semantic_issues': return '#17a2b8';
      default: return '#6c757d';
    }
  };

  const renderScanTab = () => (
    <div className="scan-tab">
      <div className="upload-section">
        <h3>📄 Document Input</h3>
        <div className="file-upload-area">
          <input
            type="file"
            accept=".txt,.pdf,.doc,.docx"
            onChange={handleFileUpload}
            id="file-upload"
            style={{ display: 'none' }}
          />
          <label htmlFor="file-upload" className="upload-button">
            📁 Choose File to Upload
          </label>
          {uploadedFile && <span className="file-name">{uploadedFile.name}</span>}
        </div>

        <div className="text-input-area">
          <h4>Or paste document text directly:</h4>
          <textarea
            placeholder="Paste the document text you want to analyze for semantic traps and institutional framing..."
            value={documentText}
            onChange={e => setDocumentText(e.target.value)}
            rows={10}
            className="document-textarea"
          />
        </div>

        <div className="scan-options">
          <h4>🔍 Scan Options</h4>
          <div className="option-grid">
            <div className="option-item">
              <label>Scan Type:</label>
              <select
                value={scanType}
                onChange={e => setScanType(e.target.value)}
              >
                <option value="comprehensive">Comprehensive Analysis</option>
                <option value="traps_only">Semantic Traps Only</option>
                <option value="framing_only">Institutional Framing Only</option>
              </select>
            </div>

            <div className="option-item">
              <label>Severity Threshold:</label>
              <select
                value={severityThreshold}
                onChange={e => setSeverityThreshold(e.target.value)}
              >
                <option value="low">All Items</option>
                <option value="medium">Medium & High Severity</option>
                <option value="high">High Severity Only</option>
              </select>
            </div>
          </div>
        </div>

        <button
          onClick={handleScanDocument}
          disabled={loading || !documentText.trim()}
          className="scan-button primary-button"
        >
          {loading ? '🔄 Scanning...' : '🔍 Scan Document'}
        </button>
      </div>

      {scanResults && renderScanResults()}
    </div>
  );

  const renderScanResults = () => {
    const { semantic_analysis, success, message } = scanResults!;

    if (!success) {
      return (
        <div className="error-message">
          <h4>❌ Scan Failed</h4>
          <p>{message}</p>
        </div>
      );
    }

    if (!semantic_analysis) {
      return null;
    }

    const { institutional_framing, semantic_traps, summary } = semantic_analysis;

    return (
      <div className="scan-results">
        <div className="results-summary">
          <h3>📊 Analysis Summary</h3>
          <div className="summary-grid">
            <div className="summary-item">
              <span className="label">Institutional Framing:</span>
              <span className="value">{summary.total_framing_detected}</span>
            </div>
            <div className="summary-item">
              <span className="label">Semantic Traps:</span>
              <span className="value">{summary.total_traps_detected}</span>
            </div>
            <div className="summary-item">
              <span className="label">Risk Level:</span>
              <span
                className="value risk-level"
                style={{ color: getRiskLevelColor(summary.document_risk_level) }}
              >
                {summary.document_risk_level.replace(/_/g, ' ').toUpperCase()}
              </span>
            </div>
            <div className="summary-item">
              <span className="label">High Severity:</span>
              <span className="value" style={{ color: getSeverityColor('high') }}>
                {summary.high_severity_items}
              </span>
            </div>
          </div>
        </div>

        {institutional_framing && institutional_framing.length > 0 && (
          <div className="framing-results">
            <h3>🏛️ Institutional Framing Detected</h3>
            {institutional_framing.map((framing, index) => (
              <div key={index} className="framing-item">
                <div className="framing-header">
                  <span
                    className="framing-type"
                    style={{ color: getSeverityColor(framing.severity) }}
                  >
                    {framing.type.replace(/_/g, ' ').toUpperCase()}
                  </span>
                  <span
                    className="severity-badge"
                    style={{ backgroundColor: getSeverityColor(framing.severity) }}
                  >
                    {framing.severity.toUpperCase()}
                  </span>
                </div>
                <div className="framing-context">
                  <strong>Context:</strong> "{framing.context}"
                </div>
                <div className="framing-description">
                  <strong>Description:</strong> {framing.description}
                </div>
                <div className="framing-rebuttal">
                  <strong>Rebuttal:</strong> {framing.rebuttal}
                </div>
              </div>
            ))}
          </div>
        )}

        {semantic_traps && semantic_traps.length > 0 && (
          <div className="traps-results">
            <h3>🪤 Semantic Traps Detected</h3>
            {semantic_traps.map((trap, index) => (
              <div key={index} className="trap-item">
                <div className="trap-header">
                  <span
                    className="trap-type"
                    style={{ color: getSeverityColor(trap.severity) }}
                  >
                    {trap.trap_type.toUpperCase()}
                  </span>
                  <span
                    className="severity-badge"
                    style={{ backgroundColor: getSeverityColor(trap.severity) }}
                  >
                    {trap.severity.toUpperCase()}
                  </span>
                  <span className="trap-category">{trap.trap_category.replace(/_/g, ' ')}</span>
                </div>
                <div className="trap-context">
                  <strong>Found in:</strong> "...{trap.context}..."
                </div>
                <div className="trap-description">
                  <strong>Trap Description:</strong> {trap.description}
                </div>
                <div className="trap-rebuttal">
                  <strong>Rebuttal:</strong> {trap.rebuttal}
                </div>
              </div>
            ))}
          </div>
        )}

        <div className="rebuttal-section">
          <h3>🛡️ Generate Narrative Sovereignty Rebuttal</h3>
          <div className="rebuttal-options">
            <label>
              <input
                type="checkbox"
                checked={includeSignatoryBlock}
                onChange={e => setIncludeSignatoryBlock(e.target.checked)}
              />
              Include Custom Signatory Block
            </label>
            {includeSignatoryBlock && (
              <div className="signatory-options">
                <input
                  placeholder="Signatory Name"
                  value={signatoryName}
                  onChange={e => setSignatoryName(e.target.value)}
                />
                <select
                  value={jurisdiction}
                  onChange={e => setJurisdiction(e.target.value)}
                >
                  <option value="Common Law">Common Law</option>
                  <option value="State National">State National</option>
                  <option value="Sovereign Individual">Sovereign Individual</option>
                </select>
              </div>
            )}
          </div>

          <button
            onClick={handleGenerateRebuttal}
            disabled={loading}
            className="rebuttal-button primary-button"
          >
            {loading ? '🔄 Generating...' : '🛡️ Generate Rebuttal'}
          </button>
        </div>

        {rebuttalResult && renderRebuttalResults()}
      </div>
    );
  };

  const renderRebuttalResults = () => {
    const { narrative_rebuttal, success, message } = rebuttalResult!;

    if (!success) {
      return (
        <div className="error-message">
          <h4>❌ Rebuttal Generation Failed</h4>
          <p>{message}</p>
        </div>
      );
    }

    if (!narrative_rebuttal) {
      return null;
    }

    return (
      <div className="rebuttal-results">
        <div className="rebuttal-header">
          <h3>🛡️ Narrative Sovereignty Rebuttal Generated</h3>
          <div className="semantic-lineage">
            <strong>Generated by:</strong> {narrative_rebuttal.semantic_lineage.author}
            <br />
            <strong>Basis:</strong> {narrative_rebuttal.semantic_lineage.basis}
            <br />
            <strong>Authority:</strong> {narrative_rebuttal.semantic_lineage.authority}
          </div>
        </div>

        {narrative_rebuttal.rebuttal_sections.map((section, index) => (
          <div key={index} className="rebuttal-section">
            <h4>{section.title}</h4>
            <div className="rebuttal-content">
              <pre>{section.content}</pre>
            </div>
          </div>
        ))}

        <div className="rebuttal-actions">
          <button className="export-button">
            📥 Export as PDF
          </button>
          <button className="export-button">
            📄 Copy to Clipboard
          </button>
          <button className="export-button">
            💾 Save Rebuttal
          </button>
        </div>
      </div>
    );
  };

  const renderEducationTab = () => (
    <div className="education-tab">
      <h3>📚 Semantic Warfare Education</h3>

      {analysisInfo && (
        <div className="education-section">
          <h4>Understanding Semantic Warfare</h4>
          <div className="info-grid">
            <div className="info-card">
              <h5>🎯 Key Concepts</h5>
              <ul>
                {analysisInfo.semantic_warfare_overview.key_concepts.map((concept, index) => (
                  <li key={index}>{concept}</li>
                ))}
              </ul>
            </div>

            <div className="info-card">
              <h5>🔍 Analysis Types</h5>
              {Object.entries(analysisInfo.analysis_types).map(([key, value]) => (
                <div key={key} className="analysis-type">
                  <strong>{key.replace(/_/g, ' ')}:</strong> {value}
                </div>
              ))}
            </div>

            <div className="info-card">
              <h5>🪤 Trap Categories</h5>
              {Object.entries(analysisInfo.trap_categories).map(([key, value]) => (
                <div key={key} className="trap-category-info">
                  <strong>{key.replace(/_/g, ' ')}:</strong> {value}
                </div>
              ))}
            </div>

            <div className="info-card">
              <h5>⚠️ Severity Levels</h5>
              {Object.entries(analysisInfo.severity_levels).map(([key, value]) => (
                <div key={key} className="severity-level-info">
                  <span
                    className="severity-indicator"
                    style={{ backgroundColor: getSeverityColor(key) }}
                  ></span>
                  <strong>{key.replace(/_/g, ' ')}:</strong> {value}
                </div>
              ))}
            </div>

            <div className="info-card">
              <h5>🛡️ Rebuttal Strategies</h5>
              {Object.entries(analysisInfo.rebuttal_strategies).map(([key, value]) => (
                <div key={key} className="rebuttal-strategy">
                  <strong>{key.replace(/_/g, ' ')}:</strong> {value}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {commonPatterns && (
        <div className="education-section">
          <h4>🪤 Common Semantic Trap Patterns</h4>
          {Object.entries(commonPatterns).map(([category, pattern]: [string, any]) => (
            <div key={category} className="pattern-card">
              <h5>{category.replace(/_/g, ' ').toUpperCase()}</h5>
              <p><strong>Description:</strong> {pattern.description}</p>
              <p><strong>Common Contexts:</strong> {pattern.common_contexts.join(', ')}</p>
              <p><strong>Rebuttal Strategy:</strong> {pattern.rebuttal_strategy}</p>
              <div className="trap-examples">
                <strong>Example Traps:</strong> {pattern.traps.join(', ')}
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="education-section">
        <h4>🎯 Carl Miller's Teachings</h4>
        <div className="teachings-summary">
          <p><strong>Core Philosophy:</strong> Semantic warfare is the use of language to create presumptions, impose obligations, and control narratives. Carl Miller teaches that words like "person," "citizen," and "resident" are institutional constructs that can trap sovereign individuals in legal fictions.</p>

          <h5>Key Strategies:</h5>
          <ul>
            <li><strong>Narrative Control:</strong> Reclaim control over your legal and commercial narrative</li>
            <li><strong>Semantic Rebuttal:</strong> Explicitly reject institutional language and framing</li>
            <li><strong>Sovereign Declaration:</strong> Declare your status and jurisdiction with clarity</li>
            <li><strong>Consent Challenge:</strong> Challenge all presumptions of consent and obligation</li>
          </ul>

          <h5>Famous Cases:</h5>
          <ul>
            <li><strong>Marbury v. Madison:</strong> Established judicial review and constitutional supremacy</li>
            <li><strong>Bond v. United States:</strong> Protected individual sovereignty from government intrusion</li>
            <li><strong>Murdoch v. Pennsylvania:</strong> Protected religious freedom from state licensing</li>
          </ul>
        </div>
      </div>
    </div>
  );

  return (
    <div className="semantic-warfare-panel">
      <div className="panel-header">
        <h2>🧠 Semantic Warfare Analysis (Carl Miller)</h2>
        <p>Detect institutional framing, semantic traps, and generate narrative sovereignty rebuttals</p>
      </div>

      <div className="tab-navigation">
        <button
          className={`tab ${activeTab === 'scan' ? 'active' : ''}`}
          onClick={() => setActiveTab('scan')}
        >
          🔍 Document Scan
        </button>
        <button
          className={`tab ${activeTab === 'rebuttal' ? 'active' : ''}`}
          onClick={() => setActiveTab('rebuttal')}
        >
          🛡️ Rebuttal Generation
        </button>
        <button
          className={`tab ${activeTab === 'education' ? 'active' : ''}`}
          onClick={() => setActiveTab('education')}
        >
          📚 Education
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'scan' && renderScanTab()}
        {activeTab === 'rebuttal' && renderScanTab()}  // Rebuttal tab uses same scan + results
        {activeTab === 'education' && renderEducationTab()}
      </div>

      <style jsx>{`
        .semantic-warfare-panel {
          max-width: 1200px;
          margin: 0 auto;
          padding: 20px;
          font-family: Arial, sans-serif;
        }

        .panel-header {
          text-align: center;
          margin-bottom: 30px;
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
          border-bottom-color: #dc3545;
          color: #dc3545;
        }

        .upload-section {
          background: white;
          padding: 20px;
          border-radius: 8px;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
          margin-bottom: 20px;
        }

        .file-upload-area {
          text-align: center;
          margin-bottom: 20px;
        }

        .upload-button {
          display: inline-block;
          padding: 12px 24px;
          background: #007bff;
          color: white;
          border-radius: 4px;
          cursor: pointer;
          transition: background 0.3s;
        }

        .upload-button:hover {
          background: #0056b3;
        }

        .file-name {
          margin-left: 10px;
          color: #28a745;
        }

        .document-textarea {
          width: 100%;
          padding: 12px;
          border: 1px solid #ddd;
          border-radius: 4px;
          font-family: monospace;
          font-size: 14px;
          resize: vertical;
        }

        .scan-options {
          margin-top: 20px;
          padding: 15px;
          background: #f8f9fa;
          border-radius: 6px;
        }

        .option-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 15px;
          margin-top: 10px;
        }

        .option-item label {
          display: block;
          margin-bottom: 5px;
          font-weight: bold;
        }

        .option-item select {
          width: 100%;
          padding: 8px;
          border: 1px solid #ddd;
          border-radius: 4px;
        }

        .primary-button {
          background: #dc3545;
          color: white;
          border: none;
          padding: 12px 24px;
          border-radius: 4px;
          cursor: pointer;
          font-size: 16px;
          margin-top: 20px;
        }

        .primary-button:disabled {
          background: #ccc;
          cursor: not-allowed;
        }

        .scan-results {
          margin-top: 20px;
        }

        .results-summary {
          background: #f8f9fa;
          padding: 20px;
          border-radius: 8px;
          margin-bottom: 20px;
        }

        .summary-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 15px;
          margin-top: 15px;
        }

        .summary-item {
          display: flex;
          justify-content: space-between;
          padding: 10px;
          background: white;
          border-radius: 4px;
          border-left: 4px solid #007bff;
        }

        .summary-item .value {
          font-weight: bold;
        }

        .framing-results, .traps-results {
          margin-bottom: 20px;
        }

        .framing-item, .trap-item {
          background: white;
          border: 1px solid #ddd;
          border-radius: 6px;
          padding: 15px;
          margin-bottom: 10px;
        }

        .framing-header, .trap-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 10px;
        }

        .severity-badge {
          color: white;
          padding: 2px 8px;
          border-radius: 12px;
          font-size: 12px;
          font-weight: bold;
        }

        .framing-context, .trap-context {
          background: #f1f3f4;
          padding: 10px;
          border-radius: 4px;
          margin: 10px 0;
          font-style: italic;
        }

        .rebuttal-section {
          background: #e3f2fd;
          padding: 20px;
          border-radius: 8px;
          margin-top: 20px;
        }

        .rebuttal-options {
          margin-bottom: 15px;
        }

        .signatory-options {
          display: flex;
          gap: 10px;
          margin-top: 10px;
        }

        .signatory-options input,
        .signatory-options select {
          padding: 8px;
          border: 1px solid #ddd;
          border-radius: 4px;
        }

        .rebuttal-results {
          background: #e8f5e8;
          border: 1px solid #c3e6cb;
          border-radius: 8px;
          padding: 20px;
          margin-top: 20px;
        }

        .rebuttal-header {
          margin-bottom: 20px;
        }

        .semantic-lineage {
          background: #f8f9fa;
          padding: 10px;
          border-radius: 4px;
          font-size: 14px;
        }

        .rebuttal-content pre {
          background: #f8f9fa;
          padding: 15px;
          border-radius: 4px;
          overflow-x: auto;
          white-space: pre-wrap;
          line-height: 1.5;
        }

        .rebuttal-actions {
          display: flex;
          gap: 10px;
          margin-top: 20px;
        }

        .export-button {
          background: #28a745;
          color: white;
          border: none;
          padding: 8px 16px;
          border-radius: 4px;
          cursor: pointer;
        }

        .education-tab {
          background: white;
          padding: 20px;
          border-radius: 8px;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .education-section {
          margin-bottom: 30px;
        }

        .info-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 20px;
          margin-top: 15px;
        }

        .info-card, .pattern-card {
          background: #f8f9fa;
          padding: 15px;
          border-radius: 6px;
          border-left: 4px solid #007bff;
        }

        .analysis-type, .trap-category-info, .severity-level-info, .rebuttal-strategy {
          margin: 8px 0;
          padding: 8px;
          background: white;
          border-radius: 4px;
        }

        .severity-indicator {
          display: inline-block;
          width: 12px;
          height: 12px;
          border-radius: 50%;
          margin-right: 8px;
        }

        .teachings-summary {
          background: #f8f9fa;
          padding: 20px;
          border-radius: 8px;
          margin-top: 15px;
        }

        .teachings-summary ul {
          text-align: left;
          max-width: 800px;
          margin: 10px auto;
        }

        .teachings-summary li {
          margin: 8px 0;
        }

        .error-message {
          background: #f8d7da;
          border: 1px solid #f5c6cb;
          color: #721c24;
          padding: 15px;
          border-radius: 6px;
          margin: 20px 0;
        }
      `}</style>
    </div>
  );
}