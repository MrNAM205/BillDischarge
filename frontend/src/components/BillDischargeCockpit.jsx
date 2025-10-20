import React, { useState, useEffect } from 'react';

// AgentVoices: Dialogic Overlay messages
const AgentVoices = {
    idle: "Awaiting instrument data, sovereign...",
    classifying: "Analyzing instrument, flagging key terms...",
    scanning: "Detecting contradictions, stand by...",
    executing: "Executing lawful remedy workflow...",
    tendering: "Tendering payment and claim...",
    discharging: "Discharging obligation, preparing final documents...",
    completed: "Remedy sequence complete. Stand in your power.",
};

function BillDischargeCockpit() {
    // Instrument Input
    const [instrumentText, setInstrumentText] = useState("INSTRUMENT OF PAYMENT\nIssuer: United States Treasury\nPayee: John Q. Public\nAmount: $10,000.00\nDate: 2023-07-15\nEndorsement: Accepted for Value\nJurisdiction: Federal Reserve District 12\nRouting Number: 123456789\nAccount Number: 987654321\nInstrument Type: Promissory Note\nNotes: This instrument is tendered in discharge of obligation under UCC 3-603.");

    // States for UI and process
    const [isAnnotated, setIsAnnotated] = useState(false);
    const [hasContradictions, setHasContradictions] = useState(false);
    const [remedyLog, setRemedyLog] = useState([]);
    const [agentStatus, setAgentStatus] = useState(AgentVoices.idle);

    // InstrumentAnnotator: CLASSIFY
    const classifyInstrument = () => {
        setAgentStatus(AgentVoices.classifying);
        setRemedyLog(prevLog => [...prevLog, { step: 'CLASSIFY', message: 'Instrument analysis initiated.' }]);
        
        // Simulate data extraction (mock parsing)
        setTimeout(() => {
            setIsAnnotated(true);
            setAgentStatus(AgentVoices.scanning);
            setRemedyLog(prevLog => [...prevLog, { step: 'CLASSIFY', message: 'Data extracted and set.' }]);
        }, 1500);
    };

    // LocalAgentCore: CONTRADICTION SCAN
    const scanForContradictions = () => {
        setAgentStatus(AgentVoices.scanning);
        setRemedyLog(prevLog => [...prevLog, { step: 'CONTRADICTION SCAN', message: 'Scanning instrument for contradictions.' }]);
        
        // Mock contradiction detection
        setTimeout(() => {
            const found = instrumentText.toUpperCase().includes('VOID') || instrumentText.toUpperCase().includes('FRAUD') || instrumentText.toUpperCase().includes('PROTEST');
            setHasContradictions(found);
            setAgentStatus(AgentVoices.executing);
            setRemedyLog(prevLog => [...prevLog, { step: 'CONTRADICTION SCAN', message: found ? 'Contradictions flagged.. Remedy sequence armed.' : 'No contradictions detected, sovereign.' }]);
        }, 2000);
    };

    // AutoTender/Discharge: EXECUTE REMEDY
    const executeRemedy = () => {
        setAgentStatus(AgentVoices.executing);
        setRemedyLog(prevLog => [...prevLog, { step: 'EXECUTE REMEDY', message: 'Remedy sequence initiated.' }]);

        // Simulate multi-step remedy workflow
        setTimeout(() => {
            setAgentStatus(AgentVoices.tendering);
            setRemedyLog(prevLog => [...prevLog, { step: 'EXECUTE REMEDY', message: 'Payment tendered and claim registered.' }]);
        }, 1000);

        setTimeout(() => {
            setAgentStatus(AgentVoices.discharging);
            setRemedyLog(prevLog => [...prevLog, { step: 'EXECUTE REMEDY', message: 'Obligation discharged. Preparing final documents.' }]);
        }, 3000);

        setTimeout(() => {
            setAgentStatus(AgentVoices.completed);
            setRemedyLog(prevLog => [...prevLog, { step: 'EXECUTE REMEDY', message: 'Remedy sequence complete. Stand in your power.' }]);
        }, 5000);
    };

    // Clear button
    const clearOutput = () => {
        setRemedyLog([]);
        setAgentStatus(AgentVoices.idle);
        setIsAnnotated(false);
        setHasContradictions(false);
    };

    // Verbose console outputs
    useEffect(() => {
        console.log("Agent Status:", agentStatus);
    }, [agentStatus]);

    return (
        <div className="flex h-screen bg-gray-900 text-teal-400 font-mono">

            {/* Left Panel: Instrument Input & Controls */}
            <div className="w-1/2 p-4">
                <h2 className="text-2xl font-bold mb-4 font-inter">Instrument Input</h2>
                <textarea
                    className="w-full h-64 p-3 bg-gray-800 text-white rounded font-mono resize-none"
                    value={instrumentText}
                    onChange={(e) => setInstrumentText(e.target.value)}
                    placeholder="Paste instrument data here..."
                />

                <div className="mt-4 flex space-x-4">
                    <button className="px-6 py-2 bg-teal-600 text-white rounded font-inter hover:bg-teal-500" onClick={classifyInstrument} disabled={isAnnotated}> {isAnnotated ? 'CLASSIFIED' : 'CLASSIFY'} </button>
                    <button className="px-6 py-2 bg-blue-600 text-white rounded font-inter hover:bg-blue-500" onClick={scanForContradictions} disabled={!isAnnotated}> CONTRADICTION SCAN </button>
                    <button className="px-6 py-2 bg-green-600 text-white rounded font-inter hover:bg-green-500" onClick={executeRemedy} disabled={!hasContradictions}> EXECUTE REMEDY </button>
                    <button className="px-6 py-2 bg-gray-500 text-white rounded font-inter hover:bg-gray-400" onClick={clearOutput}> CLEAR </button>
                </div>

                {/* Dialogic Overlay: Agent Status */}
                <div className="mt-6 p-3 bg-gray-800 text-sm rounded font-inter">
                    <span className="text-sm text-gray-500">Agent Status:</span>
                    <p className="text-md">{agentStatus}</p>
                </div>
            </div>

            {/* Right Panel: Remedy Log */}
            <div className="w-1/2 p-4 border-l border-gray-700">
                <h2 className="text-2xl font-bold mb-4 font-inter">Remedy Log</h2>
                <div className="h-full overflow-y-auto">
                    {remedyLog.map((log, index) => (
                        <div key={index} className="mb-2 p-3 bg-gray-800 rounded font-mono text-sm">
                            <span className="text-teal-200">{log.step}:</span> {log.message}
                        </div>
                    ))}
                </div>
            </div>

        </div>
    );
}

export default BillDischargeCockpit;
