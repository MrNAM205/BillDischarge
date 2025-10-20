import React, { useState, useEffect } from 'react';

interface Log {
    filename: string;
    timestamp: string;
    model: string;
}

const RemedyJournal: React.FC = () => {
    const [logs, setLogs] = useState<Log[]>([]);
    const [selectedLog, setSelectedLog] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchLogs = async () => {
            try {
                const response = await fetch('/api/logs');
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                setLogs(data);
                setError(null);
            } catch (e: any) {
                setError(e.message);
                setLogs([]);
            }
        };

        fetchLogs();
    }, []);

    const fetchLogDetails = async (filename: string) => {
        try {
            const response = await fetch(`/api/logs/${filename}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            setSelectedLog(data);
            setError(null);
        } catch (e: any) {
            setError(e.message);
            setSelectedLog(null);
        }
    };

    return (
        <div>
            <h2>Remedy Journal</h2>
            {error && <p className="error">Error: {error}</p>}
            <div style={{ display: 'flex' }}>
                <div style={{ width: '30%', borderRight: '1px solid #ccc', paddingRight: '10px' }}>
                    <h3>Past Cognition Loops</h3>
                    <ul>
                        {logs.map(log => (
                            <li key={log.filename} onClick={() => fetchLogDetails(log.filename)} style={{ cursor: 'pointer' }}>
                                {log.timestamp} - {log.model}
                            </li>
                        ))}
                    </ul>
                </div>
                <div style={{ width: '70%', paddingLeft: '10px' }}>
                    {selectedLog ? (
                        <div>
                            <h3>Log Details</h3>
                            <pre>{JSON.stringify(selectedLog, null, 2)}</pre>
                        </div>
                    ) : (
                        <p>Select a log to view details.</p>
                    )}
                </div>
            </div>
        </div>
    );
};

export default RemedyJournal;
