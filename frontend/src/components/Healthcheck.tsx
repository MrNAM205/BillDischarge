
import React, { useEffect, useState } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const Healthcheck: React.FC = () => {
    const [backendStatus, setBackendStatus] = useState('checking');

    useEffect(() => {
        const interval = setInterval(() => {
            fetch('http://localhost:8000/healthcheck')
                .then(response => {
                    if (response.ok) {
                        setBackendStatus('ok');
                    } else {
                        setBackendStatus('error');
                    }
                })
                .catch(() => {
                    setBackendStatus('error');
                });
        }, 5000);

        return () => clearInterval(interval);
    }, []);

    useEffect(() => {
        if (backendStatus === 'ok') {
            toast.success('Backend is online');
        } else if (backendStatus === 'error') {
            toast.error('Backend is offline');
        }
    }, [backendStatus]);

    return (
        <div>
            <ToastContainer />
            <p>Backend Status: {backendStatus}</p>
        </div>
    );
};

export default Healthcheck;
