import React, { useState, useEffect } from 'react';
import Tabs from './components/Tabs';
import FinancialHealth from './components/FinancialHealth';
import LegalKnowledge from './components/LegalKnowledge';
import Sovereignty from './components/Sovereignty';
import StateNationalStatus from './components/StateNationalStatus';
import Endorser from './components/Endorser';
import './App.css';

interface OmniStatusState {
    model: string;
    taskType: string;
    cognitionLineage: string[];
    status: string;
}

const OmniStatus: React.FC = () => {
    const [status, setStatus] = useState<OmniStatusState | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchStatus = async () => {
            try {
                const response = await fetch('/api/status');
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                setStatus(data);
                setError(null);
            } catch (e: any) {
                setError(e.message);
                setStatus(null);
            }
        };

        fetchStatus();
        const intervalId = setInterval(fetchStatus, 5000); // Poll every 5 seconds

        return () => clearInterval(intervalId);
    }, []);

    return (
        <div className="omni-status">
            {error && <p className="error">Error fetching status: {error}</p>}
            {status && (
                <>
                    <p><strong>Omni2 Status:</strong> {status.status}</p>
                    <p><strong>Active Model:</strong> {status.model}</p>
                    <p><strong>Cognition:</strong> {status.taskType}</p>
                </>
            )}
        </div>
    );
};


function App(): JSX.Element {
    return (
        <div className="container">
            <header>
                <h1>U.S. State National Status Correction</h1>
            </header>
            <OmniStatus />
            <Tabs>
                <div id="financial-health" title="Financial Health">
                    <FinancialHealth />
                </div>
                <div id="legal-knowledge" title="Legal Knowledge">
                    <LegalKnowledge />
                </div>
                <div id="sovereignty" title="Sovereignty">
                    <Sovereignty />
                </div>
                <div id="status-correction" title="State National Status">
                    <StateNationalStatus />
                </div>
                <div id="endorse-bill" title="Endorse Bill">
                    <Endorser />
                </div>
            </Tabs>
        </div>
    );
}

export default App;
