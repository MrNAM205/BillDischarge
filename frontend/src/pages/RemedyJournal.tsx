
import React, { useEffect, useState } from 'react';

const RemedyJournal: React.FC = () => {
    const [logs, setLogs] = useState([]);

    useEffect(() => {
        fetch('http://localhost:8000/api/remedy_logs')
            .then(response => response.json())
            .then(data => setLogs(data));
    }, []);

    return (
        <div>
            <h2>Remedy Journal</h2>
            <table>
                <thead>
                    <tr>
                        <th>Action</th>
                        <th>Details</th>
                    </tr>
                </thead>
                <tbody>
                    {logs.map((log, index) => (
                        <tr key={index}>
                            <td>{log.action}</td>
                            <td><pre>{JSON.stringify(log.details, null, 2)}</pre></td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default RemedyJournal;
