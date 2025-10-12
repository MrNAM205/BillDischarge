import { useState } from 'react';

function CognitionCockpit() {
    const [command, setCommand] = useState('');
    const [response, setResponse] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setResponse(null);

        try {
            const res = await fetch('/api/execute-command', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ command }),
            });

            const data = await res.json();
            setResponse(data);

        } catch (error) {
            setResponse({ status: 'error', message: 'An error occurred while sending the command.' });
        }
    };

    return (
        <div className="cognition-cockpit">
            <h2>Cognition Cockpit</h2>
            <p>Issue commands to the Sovereign Cognition Engine.</p>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="command">Command:</label>
                    <input
                        type="text"
                        id="command"
                        value={command}
                        onChange={(e) => setCommand(e.target.value)}
                        placeholder="e.g., ls -l /home"
                    />
                </div>
                <button type="submit">Execute</button>
            </form>
            {response && (
                <div className={`response-message ${response.status}`}>
                    <p>{response.message}</p>
                </div>
            )}
        </div>
    );
}

export default CognitionCockpit;
