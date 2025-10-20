import React, { useState } from 'react';

const RemedyScaffolder: React.FC = () => {
    const [input, setInput] = useState('');
    const [response, setResponse] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);
        setResponse(null);

        try {
            const res = await fetch('/api/remedy', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ input }),
            });

            if (!res.ok) {
                throw new Error(`HTTP error! status: ${res.status}`);
            }

            const data = await res.json();
            setResponse(data);
        } catch (e: any) {
            setError(e.message);
        }
    };

    return (
        <div>
            <h2>Scaffold Remedy Protocol</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Enter your remedy request:</label>
                    <textarea value={input} onChange={(e) => setInput(e.target.value)} required />
                </div>
                <button type="submit">Scaffold Protocol</button>
            </form>

            {error && <p className="error">Error: {error}</p>}

            {response && (
                <div className="remedy-output">
                    <h3>Remedy Protocol</h3>
                    <pre>{response.protocol}</pre>

                    <h4>Omni2’s Cognition</h4>
                    <pre>{response.thoughts}</pre>

                    <p><strong>Model Used:</strong> {response.model}</p>
                </div>
            )}
        </div>
    );
};

export default RemedyScaffolder;
