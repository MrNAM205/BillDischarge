import React, { useState, useEffect } from 'react';
import {
  searchLegalAuthorities,
  searchCaseLaw,
  searchStatutes,
  getAffidavitTemplates,
  getConstitutionalProvisions,
  getLegalResearchGuide
} from '../../lib/api';

interface SearchResult {
  success: boolean;
  message: string;
  search_results?: {
    case_law: any[];
    statutes: any[];
    constitutional: any[];
    summary: string;
    recommended_authorities: any[];
  };
  case_law_results?: any[];
  case_analysis?: any;
  statute_results?: any[];
  statute_analysis?: any;
  affidavit_templates?: any[];
  constitutional_provisions?: any[];
  grouped_provisions?: any;
}

export default function LegalResearchPanel() {
  const [activeTab, setActiveTab] = useState<'search' | 'case-law' | 'statutes' | 'affidavits' | 'constitutional' | 'guide'>('search');
  const [loading, setLoading] = useState(false);
  const [searchResults, setSearchResults] = useState<SearchResult | null>(null);
  const [researchGuide, setResearchGuide] = useState<any>(null);
  const [selectedAuthorities, setSelectedAuthorities] = useState<any[]>([]);

  // Form states for general search
  const [searchQuery, setSearchQuery] = useState('');
  const [jurisdiction, setJurisdiction] = useState('');
  const [remedyType, setRemedyType] = useState('');
  const [authorityType, setAuthorityType] = useState('');
  const [maxResults, setMaxResults] = useState(20);

  // Form states for case law search
  const [caseLawQuery, setCaseLawQuery] = useState('');
  const [caseJurisdiction, setCaseJurisdiction] = useState('');
  const [caseRemedyType, setCaseRemedyType] = useState('');
  const [timePeriod, setTimePeriod] = useState('');

  // Form states for statute search
  const [statuteQuery, setStatuteQuery] = useState('');
  const [codeType, setCodeType] = useState('');
  const [statuteJurisdiction, setStatuteJurisdiction] = useState('');

  // Form states for affidavit search
  const [affidavitType, setAffidavitType] = useState('');
  const [affidavitJurisdiction, setAffidavitJurisdiction] = useState('');
  const [useCase, setUseCase] = useState('');

  // Form states for constitutional search
  const [constitutionalQuery, setConstitutionalQuery] = useState('');
  const [article, setArticle] = useState('');
  const [amendment, setAmendment] = useState('');

  useEffect(() => {
    loadResearchGuide();
  }, []);

  const loadResearchGuide = async () => {
    try {
      const result = await getLegalResearchGuide();
      if (result.success) {
        setResearchGuide(result.research_guide);
      }
    } catch (error) {
      console.error('Failed to load research guide:', error);
    }
  };

  const handleGeneralSearch = async () => {
    if (!searchQuery.trim()) {
      alert('Please enter a search query');
      return;
    }

    setLoading(true);
    setSearchResults(null);

    try {
      const result = await searchLegalAuthorities({
        query: searchQuery,
        jurisdiction,
        remedy_type: remedyType,
        authority_type: authorityType,
        max_results: maxResults
      });
      setSearchResults(result);
    } catch (error) {
      setSearchResults({
        success: false,
        message: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`
      });
    } finally {
      setLoading(false);
    }
  };

  const handleCaseLawSearch = async () => {
    if (!caseLawQuery.trim()) {
      alert('Please enter a case law search query');
      return;
    }

    setLoading(true);
    setSearchResults(null);

    try {
      const result = await searchCaseLaw({
        query: caseLawQuery,
        jurisdiction: caseJurisdiction,
        remedy_type: caseRemedyType,
        time_period: timePeriod,
        max_results: 10
      });
      setSearchResults(result);
    } catch (error) {
      setSearchResults({
        success: false,
        message: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`
      });
    } finally {
      setLoading(false);
    }
  };

  const handleStatuteSearch = async () => {
    if (!statuteQuery.trim()) {
      alert('Please enter a statute search query');
      return;
    }

    setLoading(true);
    setSearchResults(null);

    try {
      const result = await searchStatutes({
        query: statuteQuery,
        code_type: codeType,
        jurisdiction: statuteJurisdiction,
        max_results: 10
      });
      setSearchResults(result);
    } catch (error) {
      setSearchResults({
        success: false,
        message: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`
      });
    } finally {
      setLoading(false);
    }
  };

  const handleAffidavitSearch = async () => {
    setLoading(true);
    setSearchResults(null);

    try {
      const result = await getAffidavitTemplates({
        affidavit_type: affidavitType,
        jurisdiction: affidavitJurisdiction,
        use_case: useCase
      });
      setSearchResults(result);
    } catch (error) {
      setSearchResults({
        success: false,
        message: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`
      });
    } finally {
      setLoading(false);
    }
  };

  const handleConstitutionalSearch = async () => {
    setLoading(true);
    setSearchResults(null);

    try {
      const params = {
        query: constitutionalQuery,
        article,
        amendment
      };
      const result = await getConstitutionalProvisions(params);
      setSearchResults(result);
    } catch (error) {
      setSearchResults({
        success: false,
        message: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`
      });
    } finally {
      setLoading(false);
    }
  };

  const toggleAuthoritySelection = (authority: any) => {
    setSelectedAuthorities(prev => {
      const exists = prev.find(a => a.citation === authority.citation);
      if (exists) {
        return prev.filter(a => a.citation !== authority.citation);
      } else {
        return [...prev, authority];
      }
    });
  };

  const exportSelectedAuthorities = () => {
    const selectedText = selectedAuthorities.map(auth =>
      `${auth.authority || auth.case_name || auth.statute_name} (${auth.citation})\n${auth.holding || auth.application || 'N/A'}`
    ).join('\n\n');

    const blob = new Blob([selectedText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'legal_authorities.txt';
    a.click();
    URL.revokeObjectURL(url);
  };

  const getRelevanceColor = (score: number) => {
    if (score >= 0.8) return '#28a745';
    if (score >= 0.5) return '#ffc107';
    return '#dc3545';
  };

  const renderSearchTab = () => (
    <div className="search-tab">
      <div className="search-section">
        <h3>🔍 Comprehensive Legal Search</h3>
        <div className="search-form">
          <div className="main-search">
            <input
              type="text"
              placeholder="Enter search query (e.g., 'Hale v. Henkel', 'UCC 1-207', 'sovereign immunity')"
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              className="search-input"
            />
            <button
              onClick={handleGeneralSearch}
              disabled={loading || !searchQuery.trim()}
              className="search-button primary-button"
            >
              {loading ? '🔄 Searching...' : '🔍 Search'}
            </button>
          </div>

          <div className="filter-options">
            <div className="filter-grid">
              <div className="filter-item">
                <label>Jurisdiction:</label>
                <select
                  value={jurisdiction}
                  onChange={e => setJurisdiction(e.target.value)}
                >
                  <option value="">All Jurisdictions</option>
                  <option value="federal">Federal</option>
                  <option value="state">State</option>
                  <option value="common_law">Common Law</option>
                </select>
              </div>

              <div className="filter-item">
                <label>Remedy Type:</label>
                <select
                  value={remedyType}
                  onChange={e => setRemedyType(e.target.value)}
                >
                  <option value="">All Types</option>
                  <option value="sovereignty">Sovereignty</option>
                  <option value="jurisdiction">Jurisdiction</option>
                  <option value="rights">Rights</option>
                </select>
              </div>

              <div className="filter-item">
                <label>Authority Type:</label>
                <select
                  value={authorityType}
                  onChange={e => setAuthorityType(e.target.value)}
                >
                  <option value="">All Types</option>
                  <option value="case_law">Case Law</option>
                  <option value="statutes">Statutes</option>
                  <option value="constitutional">Constitutional</option>
                </select>
              </div>

              <div className="filter-item">
                <label>Max Results:</label>
                <input
                  type="number"
                  value={maxResults}
                  onChange={e => setMaxResults(parseInt(e.target.value) || 20)}
                  min="5"
                  max="50"
                />
              </div>
            </div>
          </div>
        </div>

        {searchResults && renderSearchResults()}
      </div>
    </div>
  );

  const renderCaseLawTab = () => (
    <div className="case-law-tab">
      <div className="search-section">
        <h3>⚖️ Case Law Research</h3>
        <div className="search-form">
          <div className="main-search">
            <input
              type="text"
              placeholder="Search case law (e.g., 'Marbury v. Madison', 'due process', 'equal protection')"
              value={caseLawQuery}
              onChange={e => setCaseLawQuery(e.target.value)}
              className="search-input"
            />
            <button
              onClick={handleCaseLawSearch}
              disabled={loading || !caseLawQuery.trim()}
              className="search-button primary-button"
            >
              {loading ? '🔄 Searching...' : '⚖️ Search Cases'}
            </button>
          </div>

          <div className="filter-options">
            <div className="filter-grid">
              <div className="filter-item">
                <label>Jurisdiction:</label>
                <select
                  value={caseJurisdiction}
                  onChange={e => setCaseJurisdiction(e.target.value)}
                >
                  <option value="">All</option>
                  <option value="supreme_court">Supreme Court</option>
                  <option value="federal">Federal Courts</option>
                  <option value="state">State Courts</option>
                </select>
              </div>

              <div className="filter-item">
                <label>Remedy Type:</label>
                <select
                  value={caseRemedyType}
                  onChange={e => setCaseRemedyType(e.target.value)}
                >
                  <option value="">All</option>
                  <option value="sovereignty">Sovereignty</option>
                  <option value="rights_protection">Rights Protection</option>
                  <option value="jurisdiction">Jurisdiction</option>
                </select>
              </div>

              <div className="filter-item">
                <label>Time Period:</label>
                <select
                  value={timePeriod}
                  onChange={e => setTimePeriod(e.target.value)}
                >
                  <option value="">All Periods</option>
                  <option value="1800-1900">1800-1900</option>
                  <option value="1900-2000">1900-2000</option>
                  <option value="2000-present">2000-Present</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        {searchResults && renderCaseLawResults()}
      </div>
    </div>
  );

  const renderStatutesTab = () => (
    <div className="statutes-tab">
      <div className="search-section">
        <h3>📜 Statute Research</h3>
        <div className="search-form">
          <div className="main-search">
            <input
              type="text"
              placeholder="Search statutes (e.g., 'UCC 1-207', '18 USC 241', 'rights protected')"
              value={statuteQuery}
              onChange={e => setStatuteQuery(e.target.value)}
              className="search-input"
            />
            <button
              onClick={handleStatuteSearch}
              disabled={loading || !statuteQuery.trim()}
              className="search-button primary-button"
            >
              {loading ? '🔄 Searching...' : '📜 Search Statutes'}
            </button>
          </div>

          <div className="filter-options">
            <div className="filter-grid">
              <div className="filter-item">
                <label>Code Type:</label>
                <select
                  value={codeType}
                  onChange={e => setCodeType(e.target.value)}
                >
                  <option value="">All Codes</option>
                  <option value="UCC">UCC</option>
                  <option value="USC">U.S. Code</option>
                  <option value="Constitution">Constitution</option>
                  <option value="State">State Codes</option>
                </select>
              </div>

              <div className="filter-item">
                <label>Jurisdiction:</label>
                <select
                  value={statuteJurisdiction}
                  onChange={e => setStatuteJurisdiction(e.target.value)}
                >
                  <option value="">All</option>
                  <option value="federal">Federal</option>
                  <option value="state">State</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        {searchResults && renderStatuteResults()}
      </div>
    </div>
  );

  const renderAffidavitsTab = () => (
    <div className="affidavits-tab">
      <div className="search-section">
        <h3>📋 Affidavit Templates</h3>
        <div className="search-form">
          <div className="filter-options">
            <div className="filter-grid">
              <div className="filter-item">
                <label>Affidavit Type:</label>
                <select
                  value={affidavitType}
                  onChange={e => setAffidavitType(e.target.value)}
                >
                  <option value="">All Types</option>
                  <option value="status_correction">Status Correction</option>
                  <option value="jurisdiction">Jurisdiction Declaration</option>
                  <option value="rights_assertion">Rights Assertion</option>
                </select>
              </div>

              <div className="filter-item">
                <label>Jurisdiction:</label>
                <select
                  value={affidavitJurisdiction}
                  onChange={e => setAffidavitJurisdiction(e.target.value)}
                >
                  <option value="">All</option>
                  <option value="Common Law">Common Law</option>
                  <option value="State Court">State Court</option>
                  <option value="Federal">Federal</option>
                </select>
              </div>

              <div className="filter-item">
                <label>Use Case:</label>
                <input
                  type="text"
                  placeholder="e.g., tax defense, property rights"
                  value={useCase}
                  onChange={e => setUseCase(e.target.value)}
                />
              </div>
            </div>
          </div>

          <button
            onClick={handleAffidavitSearch}
            disabled={loading}
            className="search-button primary-button"
          >
            {loading ? '🔄 Loading...' : '📋 Get Templates'}
          </button>
        </div>

        {searchResults && renderAffidavitResults()}
      </div>
    </div>
  );

  const renderConstitutionalTab = () => (
    <div className="constitutional-tab">
      <div className="search-section">
        <h3>🇺🇸 Constitutional Research</h3>
        <div className="search-form">
          <div className="filter-options">
            <div className="filter-grid">
              <div className="filter-item">
                <label>Search Query:</label>
                <input
                  type="text"
                  placeholder="e.g., 'due process', 'freedom of speech'"
                  value={constitutionalQuery}
                  onChange={e => setConstitutionalQuery(e.target.value)}
                />
              </div>

              <div className="filter-item">
                <label>Article:</label>
                <input
                  type="text"
                  placeholder="e.g., I, II, III"
                  value={article}
                  onChange={e => setArticle(e.target.value)}
                />
              </div>

              <div className="filter-item">
                <label>Amendment:</label>
                <input
                  type="text"
                  placeholder="e.g., 1, 2, 14"
                  value={amendment}
                  onChange={e => setAmendment(e.target.value)}
                />
              </div>
            </div>
          </div>

          <button
            onClick={handleConstitutionalSearch}
            disabled={loading}
            className="search-button primary-button"
          >
            {loading ? '🔄 Searching...' : '🇺🇸 Search Constitution'}
          </button>
        </div>

        {searchResults && renderConstitutionalResults()}
      </div>
    </div>
  );

  const renderGuideTab = () => (
    <div className="guide-tab">
      <div className="guide-section">
        <h3>📚 Legal Research Guide</h3>

        {researchGuide && (
          <div className="guide-content">
            <div className="guide-section-card">
              <h4>🔍 Research Methodology</h4>
              <div className="methodology-grid">
                <div className="method-group">
                  <h5>Primary Sources</h5>
                  <ul>
                    {researchGuide.research_methodology.primary_sources.map((source, index) => (
                      <li key={index}>{source}</li>
                    ))}
                  </ul>
                </div>

                <div className="method-group">
                  <h5>Secondary Sources</h5>
                  <ul>
                    {researchGuide.research_methodology.secondary_sources.map((source, index) => (
                      <li key={index}>{source}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>

            <div className="guide-section-card">
              <h4>⭐ Key Authorities</h4>
              <div className="authorities-grid">
                <div className="authority-group">
                  <h5>🏛️ Sovereignty Cases</h5>
                  <ul>
                    {researchGuide.key_authorities.sovereignty_cases.map((caseName, index) => (
                      <li key={index}>{caseName}</li>
                    ))}
                  </ul>
                </div>

                <div className="authority-group">
                  <h5>📜 Constitutional Provisions</h5>
                  <ul>
                    {researchGuide.key_authorities.constitutional_provisions.map((provision, index) => (
                      <li key={index}>{provision}</li>
                    ))}
                  </ul>
                </div>

                <div className="authority-group">
                  <h5>⚖️ Statutory Authorities</h5>
                  <ul>
                    {researchGuide.key_authorities.statutory_authorities.map((statute, index) => (
                      <li key={index}>{statute}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>

            <div className="guide-section-card">
              <h4>💡 Research Strategies</h4>
              <ul className="strategies-list">
                {Object.entries(researchGuide.research_strategies).map(([key, strategy]) => (
                  <li key={key}>
                    <strong>{key.replace(/_/g, ' ')}:</strong> {strategy}
                  </li>
                ))}
              </ul>
            </div>

            <div className="guide-section-card">
              <h4>🎯 Common Research Topics</h4>
              {Object.entries(researchGuide.common_research_topics).map(([topic, description]) => (
                <div key={topic} className="research-topic">
                  <strong>{topic.replace(/_/g, ' ')}:</strong> {description}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );

  const renderSearchResults = () => {
    if (!searchResults?.success) {
      return (
        <div className="error-message">
          <h4>❌ Search Failed</h4>
          <p>{searchResults?.message}</p>
        </div>
      );
    }

    const search_data = searchResults.search_results;
    if (!search_data) return null;

    return (
      <div className="search-results">
        <div className="results-header">
          <h3>📊 Search Results</h3>
          <p>{search_data.summary}</p>
        </div>

        <div className="selected-authorities">
          <h4>📌 Selected Authorities ({selectedAuthorities.length})</h4>
          <div className="selected-list">
            {selectedAuthorities.map((auth, index) => (
              <div key={index} className="selected-item">
                {auth.authority || auth.case_name || auth.statute_name} ({auth.citation})
              </div>
            ))}
          </div>
          {selectedAuthorities.length > 0 && (
            <button onClick={exportSelectedAuthorities} className="export-button">
              📥 Export Selected
            </button>
          )}
        </div>

        <div className="results-grid">
          <div className="results-section">
            <h4>⚖️ Case Law ({search_data.case_law?.length || 0})</h4>
            {search_data.case_law?.map((caseItem, index) => (
              <div key={index} className="result-item case-item">
                <div className="result-header">
                  <input
                    type="checkbox"
                    onChange={() => toggleAuthoritySelection({
                      authority: caseItem.case_name,
                      citation: caseItem.citation,
                      holding: caseItem.holding
                    })}
                    checked={selectedAuthorities.some(a => a.citation === caseItem.citation)}
                  />
                  <span className="case-name">{caseItem.case_name}</span>
                  <span
                    className="relevance-score"
                    style={{ color: getRelevanceColor(caseItem.relevance_score) }}
                  >
                    Relevance: {(caseItem.relevance_score * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="result-details">
                  <p><strong>Citation:</strong> {caseItem.citation} ({caseItem.year})</p>
                  <p><strong>Holding:</strong> {caseItem.holding}</p>
                  <p><strong>Key Principles:</strong> {caseItem.key_principles?.join(', ')}</p>
                </div>
              </div>
            ))}
          </div>

          <div className="results-section">
            <h4>📜 Statutes ({search_data.statutes?.length || 0})</h4>
            {search_data.statutes?.map((statute, index) => (
              <div key={index} className="result-item statute-item">
                <div className="result-header">
                  <input
                    type="checkbox"
                    onChange={() => toggleAuthoritySelection({
                      authority: statute.statute_name,
                      citation: statute.citation,
                      holding: statute.application
                    })}
                    checked={selectedAuthorities.some(a => a.citation === statute.citation)}
                  />
                  <span className="statute-name">{statute.statute_name}</span>
                  <span className="code-type">{statute.code_type}</span>
                </div>
                <div className="result-details">
                  <p><strong>Citation:</strong> {statute.citation}</p>
                  <p><strong>Application:</strong> {statute.application}</p>
                  <p><strong>Key Provisions:</strong> {statute.key_provisions?.join(', ')}</p>
                </div>
              </div>
            ))}
          </div>

          <div className="results-section">
            <h4>🇺🇸 Constitutional ({search_data.constitutional?.length || 0})</h4>
            {search_data.constitutional?.map((provision, index) => (
              <div key={index} className="result-item constitutional-item">
                <div className="result-header">
                  <input
                    type="checkbox"
                    onChange={() => toggleAuthoritySelection({
                      authority: provision.provision,
                      citation: `Art. ${provision.article}${provision.section ? `§${provision.section}` : ''}`,
                      holding: provision.application
                    })}
                    checked={selectedAuthorities.some(a => a.citation === `Art. ${provision.article}${provision.section ? `§${provision.section}` : ''}`)}
                  />
                  <span className="provision-name">{provision.provision}</span>
                </div>
                <div className="result-details">
                  <p><strong>Article {provision.article}{provision.section ? ` §${provision.section}` : ''}</strong></p>
                  <p><strong>Application:</strong> {provision.application}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {search_data.recommended_authorities?.length > 0 && (
          <div className="recommended-authorities">
            <h4>⭐ Recommended Authorities for Citation</h4>
            {search_data.recommended_authorities.map((auth, index) => (
              <div key={index} className="recommended-item">
                <strong>{auth.authority}</strong> ({auth.citation}) - {auth.reason}
              </div>
            ))}
          </div>
        )}
      </div>
    );
  };

  const renderCaseLawResults = () => {
    if (!searchResults?.success || !searchResults.case_law_results) {
      return (
        <div className="error-message">
          <h4>❌ Case Law Search Failed</h4>
          <p>{searchResults?.message}</p>
        </div>
      );
    }

    const { case_law_results, case_analysis } = searchResults;

    return (
      <div className="case-law-results">
        <div className="results-header">
          <h3>⚖️ Case Law Results</h3>
          <p>Found {case_analysis?.total_cases_found || 0} cases</p>
        </div>

        {case_analysis && (
          <div className="case-analysis">
            <h4>📊 Case Analysis</h4>
            <div className="analysis-grid">
              <div className="analysis-item">
                <strong>Time Distribution:</strong>
                {Object.entries(case_analysis.time_distribution).map(([period, count]) => (
                  <span key={period}>{period}: {count}, </span>
                ))}
              </div>
              <div className="analysis-item">
                <strong>Jurisdiction Distribution:</strong>
                {Object.entries(case_analysis.jurisdiction_distribution).map(([jur, count]) => (
                  <span key={jur}>{jur}: {count}, </span>
                ))}
              </div>
            </div>
          </div>
        )}

        <div className="cases-list">
          {case_law_results.map((caseItem, index) => (
            <div key={index} className="result-item case-item">
              <div className="result-header">
                <input
                  type="checkbox"
                  onChange={() => toggleAuthoritySelection({
                    authority: caseItem.case_name,
                    citation: caseItem.citation,
                    holding: caseItem.holding
                  })}
                  checked={selectedAuthorities.some(a => a.citation === caseItem.citation)}
                />
                <span className="case-name">{caseItem.case_name}</span>
                <span
                  className="relevance-score"
                  style={{ color: getRelevanceColor(caseItem.relevance_score) }}
                >
                  Relevance: {(caseItem.relevance_score * 100).toFixed(1)}%
                </span>
              </div>
              <div className="result-details">
                <p><strong>Citation:</strong> {caseItem.citation} ({caseItem.year})</p>
                <p><strong>Holding:</strong> {caseItem.holding}</p>
                <p><strong>Key Principles:</strong> {caseItem.key_principles?.join(', ')}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderStatuteResults = () => {
    if (!searchResults?.success || !searchResults.statute_results) {
      return (
        <div className="error-message">
          <h4>❌ Statute Search Failed</h4>
          <p>{searchResults?.message}</p>
        </div>
      );
    }

    const { statute_results, statute_analysis } = searchResults;

    return (
      <div className="statute-results">
        <div className="results-header">
          <h3>📜 Statute Results</h3>
          <p>Found {statute_analysis?.total_statutes_found || 0} statutes</p>
        </div>

        {statute_analysis && (
          <div className="statute-analysis">
            <h4>📊 Statute Analysis</h4>
            <div className="analysis-grid">
              <div className="analysis-item">
                <strong>Code Types:</strong>
                {Object.entries(statute_analysis.code_type_distribution).map(([code, count]) => (
                  <span key={code}>{code}: {count}, </span>
                ))}
              </div>
              <div className="analysis-item">
                <strong>Applications:</strong>
                {Object.entries(statute_analysis.application_categories).map(([app, count]) => (
                  <span key={app}>{app}: {count}, </span>
                ))}
              </div>
            </div>
          </div>
        )}

        <div className="statutes-list">
          {statute_results.map((statute, index) => (
            <div key={index} className="result-item statute-item">
              <div className="result-header">
                <input
                  type="checkbox"
                  onChange={() => toggleAuthoritySelection({
                    authority: statute.statute_name,
                    citation: statute.citation,
                    holding: statute.application
                  })}
                  checked={selectedAuthorities.some(a => a.citation === statute.citation)}
                />
                <span className="statute-name">{statute.statute_name}</span>
                <span className="code-type">{statute.code_type}</span>
              </div>
              <div className="result-details">
                <p><strong>Citation:</strong> {statute.citation}</p>
                <p><strong>Application:</strong> {statute.application}</p>
                <p><strong>Key Provisions:</strong> {statute.key_provisions?.join(', ')}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderAffidavitResults = () => {
    if (!searchResults?.success || !searchResults.affidavit_templates) {
      return (
        <div className="error-message">
          <h4>❌ Affidavit Search Failed</h4>
          <p>{searchResults?.message}</p>
        </div>
      );
    }

    return (
      <div className="affidavit-results">
        <div className="results-header">
          <h3>📋 Affidavit Templates</h3>
          <p>Found {searchResults.affidavit_templates.length} templates</p>
        </div>

        <div className="templates-list">
          {searchResults.affidavit_templates.map((template, index) => (
            <div key={index} className="result-item template-item">
              <div className="result-header">
                <span className="template-title">{template.title}</span>
                <span className="template-type">{template.type}</span>
              </div>
              <div className="result-details">
                <p><strong>Description:</strong> {template.description}</p>
                <p><strong>Jurisdiction:</strong> {template.jurisdiction}</p>
                <p><strong>Required Elements:</strong> {template.required_elements?.join(', ')}</p>
                <p><strong>Usage Scenarios:</strong></p>
                <ul>
                  {template.usage_scenarios?.map((scenario, idx) => (
                    <li key={idx}>{scenario}</li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderConstitutionalResults = () => {
    if (!searchResults?.success || !searchResults.constitutional_provisions) {
      return (
        <div className="error-message">
          <h4>❌ Constitutional Search Failed</h4>
          <p>{searchResults?.message}</p>
        </div>
      );
    }

    return (
      <div className="constitutional-results">
        <div className="results-header">
          <h3>🇺🇸 Constitutional Provisions</h3>
          <p>Found {searchResults.constitutional_provisions.length} provisions</p>
        </div>

        <div className="provisions-list">
          {searchResults.constitutional_provisions.map((provision, index) => (
            <div key={index} className="result-item constitutional-item">
              <div className="result-header">
                <input
                  type="checkbox"
                  onChange={() => toggleAuthoritySelection({
                    authority: provision.provision,
                    citation: `Art. ${provision.article}${provision.section ? `§${provision.section}` : ''}`,
                    holding: provision.application
                  })}
                  checked={selectedAuthorities.some(a => a.citation === `Art. ${provision.article}${provision.section ? `§${provision.section}` : ''}`)}
                />
                <span className="provision-name">{provision.provision}</span>
              </div>
              <div className="result-details">
                <p><strong>Article {provision.article}{provision.section ? ` §${provision.section}` : ''}</strong></p>
                <p><strong>Text:</strong> {provision.text}</p>
                <p><strong>Application:</strong> {provision.application}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="legal-research-panel">
      <div className="panel-header">
        <h2>⚖️ Legal Research Panel</h2>
        <p>Search case law, constitutional provisions, and remedy statutes for sovereign invocation</p>
      </div>

      <div className="tab-navigation">
        <button
          className={`tab ${activeTab === 'search' ? 'active' : ''}`}
          onClick={() => setActiveTab('search')}
        >
          🔍 Comprehensive Search
        </button>
        <button
          className={`tab ${activeTab === 'case-law' ? 'active' : ''}`}
          onClick={() => setActiveTab('case-law')}
        >
          ⚖️ Case Law
        </button>
        <button
          className={`tab ${activeTab === 'statutes' ? 'active' : ''}`}
          onClick={() => setActiveTab('statutes')}
        >
          📜 Statutes
        </button>
        <button
          className={`tab ${activeTab === 'affidavits' ? 'active' : ''}`}
          onClick={() => setActiveTab('affidavits')}
        >
          📋 Affidavits
        </button>
        <button
          className={`tab ${activeTab === 'constitutional' ? 'active' : ''}`}
          onClick={() => setActiveTab('constitutional')}
        >
          🇺🇸 Constitution
        </button>
        <button
          className={`tab ${activeTab === 'guide' ? 'active' : ''}`}
          onClick={() => setActiveTab('guide')}
        >
          📚 Research Guide
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'search' && renderSearchTab()}
        {activeTab === 'case-law' && renderCaseLawTab()}
        {activeTab === 'statutes' && renderStatutesTab()}
        {activeTab === 'affidavits' && renderAffidavitsTab()}
        {activeTab === 'constitutional' && renderConstitutionalTab()}
        {activeTab === 'guide' && renderGuideTab()}
      </div>

      <style jsx>{`
        .legal-research-panel {
          max-width: 1400px;
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
          overflow-x: auto;
        }

        .tab {
          padding: 12px 20px;
          border: none;
          background: none;
          cursor: pointer;
          border-bottom: 2px solid transparent;
          transition: all 0.3s;
          white-space: nowrap;
          font-size: 14px;
        }

        .tab.active {
          border-bottom-color: #007bff;
          color: #007bff;
        }

        .search-section {
          background: white;
          padding: 20px;
          border-radius: 8px;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
          margin-bottom: 20px;
        }

        .search-form {
          margin-bottom: 20px;
        }

        .main-search {
          display: flex;
          gap: 10px;
          margin-bottom: 20px;
        }

        .search-input {
          flex: 1;
          padding: 12px;
          border: 1px solid #ddd;
          border-radius: 4px;
          font-size: 16px;
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

        .filter-options {
          background: #f8f9fa;
          padding: 15px;
          border-radius: 6px;
        }

        .filter-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 15px;
        }

        .filter-item label {
          display: block;
          margin-bottom: 5px;
          font-weight: bold;
        }

        .filter-item input,
        .filter-item select {
          width: 100%;
          padding: 8px;
          border: 1px solid #ddd;
          border-radius: 4px;
        }

        .search-results {
          background: #f8f9fa;
          padding: 20px;
          border-radius: 8px;
        }

        .results-header {
          margin-bottom: 20px;
        }

        .selected-authorities {
          background: white;
          padding: 15px;
          border-radius: 6px;
          margin-bottom: 20px;
        }

        .selected-list {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
          margin: 10px 0;
        }

        .selected-item {
          background: #007bff;
          color: white;
          padding: 4px 8px;
          border-radius: 12px;
          font-size: 12px;
        }

        .export-button {
          background: #28a745;
          color: white;
          border: none;
          padding: 8px 16px;
          border-radius: 4px;
          cursor: pointer;
        }

        .results-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
          gap: 20px;
        }

        .results-section {
          background: white;
          padding: 15px;
          border-radius: 6px;
        }

        .result-item {
          border: 1px solid #ddd;
          border-radius: 6px;
          padding: 15px;
          margin-bottom: 10px;
        }

        .result-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 10px;
        }

        .case-name, .statute-name, .provision-name, .template-title {
          font-weight: bold;
          flex: 1;
          margin: 0 10px;
        }

        .relevance-score {
          font-weight: bold;
        }

        .code-type, .template-type {
          background: #6c757d;
          color: white;
          padding: 2px 8px;
          border-radius: 12px;
          font-size: 12px;
        }

        .result-details p {
          margin: 5px 0;
          font-size: 14px;
        }

        .result-details ul {
          margin: 5px 0;
          padding-left: 20px;
        }

        .recommended-authorities {
          background: white;
          padding: 15px;
          border-radius: 6px;
          margin-top: 20px;
        }

        .recommended-item {
          background: #e3f2fd;
          padding: 10px;
          border-radius: 4px;
          margin-bottom: 5px;
        }

        .case-analysis, .statute-analysis {
          background: white;
          padding: 15px;
          border-radius: 6px;
          margin-bottom: 20px;
        }

        .analysis-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 15px;
        }

        .analysis-item {
          background: #f8f9fa;
          padding: 10px;
          border-radius: 4px;
        }

        .guide-content {
          background: white;
          padding: 20px;
          border-radius: 8px;
        }

        .guide-section-card {
          background: #f8f9fa;
          padding: 15px;
          border-radius: 6px;
          margin-bottom: 20px;
        }

        .methodology-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 20px;
        }

        .method-group h5 {
          color: #007bff;
          margin-bottom: 10px;
        }

        .authorities-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 20px;
        }

        .authority-group h5 {
          color: #28a745;
          margin-bottom: 10px;
        }

        .strategies-list li {
          margin: 10px 0;
          padding: 10px;
          background: white;
          border-radius: 4px;
        }

        .research-topic {
          margin: 10px 0;
          padding: 10px;
          background: white;
          border-radius: 4px;
        }

        .error-message {
          background: #f8d7da;
          border: 1px solid #f5c6cb;
          color: #721c24;
          padding: 15px;
          border-radius: 6px;
          text-align: center;
        }

        @media (max-width: 768px) {
          .main-search {
            flex-direction: column;
          }

          .filter-grid {
            grid-template-columns: 1fr;
          }

          .results-grid {
            grid-template-columns: 1fr;
          }

          .tab-navigation {
            overflow-x: scroll;
          }
        }
      `}</style>
    </div>
  );
}