
import React, { useState, useEffect } from 'react';

const AgentVoices = {
  GREETING: "Awaiting instrument for cognitive scaffolding.",
  ANNOTATING: "Instrument received. Applying semantic annotation layer...",
  ANNOTATED: "Annotation complete. Ready for contradiction analysis.",
  SCANNING: "Scanning for jurisdictional and logical contradictions...",
  NO_CONTRADICTION: "Scan complete. No overt contradictions found. Proceed with caution.",
  CONTRADICTION_FOUND: "CRITICAL: Contradiction detected. Instrument may be void. Review log.",
  EXECUTING_REMEDY: "Contradiction confirmed. Initiating AutoTender discharge protocol...",
  REMEDY_STEP_1: "Step 1: Generating Sovereign Endorsement...",
  REMEDY_STEP_2: "Step 2: Assembling Digital Apostille...",
  REMEDY_STEP_3: "Step 3: Logging transaction with LocalAgentCore...",
  REMEDY_COMPLETE: "Discharge remedy logged. Monitor for response.",
};

const mockInstrument = `
TO: JOHN DOE
123 MAIN STREET, ANYTOWN, USA

FROM: MEGA CORP
456 FINANCE BLVD, SUITE 100
FINANCE CITY, USA

DATE: 2025-10-15
INVOICE #: 12345
AMOUNT DUE: $100.00

NOTICE: This is a demand for payment. Failure to remit payment will result in further action.
This instrument is a presentment from a corporation and may be VOID against a sovereign.
`;

const BillDischargeCockpit = () => {
  const [instrumentText, setInstrumentText] = useState(mockInstrument);
  const [isAnnotated, setIsAnnotated] = useState(false);
  const [contradictionFound, setContradictionFound] = useState(null);
  const [remedyLog, setRemedyLog] = useState([]);
  const [agentStatus, setAgentStatus] = useState(AgentVoices.GREETING);

  const log = (message) => {
    const timestamp = new Date().toISOString();
    setRemedyLog(prevLog => [...prevLog, `[${timestamp}] ${message}`]);
  };

  const handleClassify = () => {
    setAgentStatus(AgentVoices.ANNOTATING);
    log("Initiating Instrument Annotation...");
    setTimeout(() => {
      setIsAnnotated(true);
      setAgentStatus(AgentVoices.ANNOTATED);
      log("Instrument Classified: Type 'INVOICE', Issuer 'MEGA CORP'");
    }, 1500);
  };

  const handleScan = () => {
    setAgentStatus(AgentVoices.SCANNING);
    log("Performing Contradiction Scan...");
    setTimeout(() => {
      const hasContradiction = /VOID|FRAUD|PROTEST/i.test(instrumentText);
      setContradictionFound(hasContradiction);
      if (hasContradiction) {
        setAgentStatus(AgentVoices.CONTRADICTION_FOUND);
        log("CONTRADICTION: Found keyword 'VOID'. Instrument integrity compromised.");
      } else {
        setAgentStatus(AgentVoices.NO_CONTRADICTION);
        log("SCAN COMPLETE: No obvious keywords for contradiction found.");
      }
    }, 2000);
  };

  const executeRemedyStep = (step, voice, delay) => {
    return new Promise(resolve => {
      setTimeout(() => {
        setAgentStatus(voice);
        log(voice);
        resolve();
      }, delay);
    });
  };

  const handleExecuteRemedy = async () => {
    setAgentStatus(AgentVoices.EXECUTING_REMEDY);
    log("Executing Remedy Protocol...");
    await executeRemedyStep(1, AgentVoices.REMEDY_STEP_1, 1500);
    await executeRemedyStep(2, AgentVoices.REMEDY_STEP_2, 2000);
    await executeRemedyStep(3, AgentVoices.REMEDY_STEP_3, 1500);
    setAgentStatus(AgentVoices.REMEDY_COMPLETE);
    log("Protocol complete. Standing by.");
  };

  return (
    <div className="bg-gray-900 text-white min-h-screen font-mono p-4 flex flex-col md:flex-row">
      {/* Main Cockpit Interface */}
      <div className="flex-grow md:mr-4">
        <h1 className="text-2xl text-teal-400 font-bold mb-2">SOVEREIGN COGNITION AGENT</h1>
        <p className="text-sm text-gray-400 mb-4">OmniVisionaryBeing Cockpit Interface</p>

        {/* Agent Status */}
        <div className="bg-black p-3 rounded-lg mb-4 border border-teal-500">
          <h2 className="text-lg text-teal-400">AGENT STATUS:</h2>
          <p className="text-green-400 animate-pulse">{agentStatus}</p>
        </div>

        {/* Instrument Input */}
        <div className="mb-4">
          <h2 className="text-lg text-teal-400 mb-2">1. INSTRUMENT INPUT</h2>
          <textarea
            className="w-full h-64 bg-gray-800 border border-gray-600 rounded-lg p-2 text-sm text-gray-300 focus:outline-none focus:border-teal-400"
            value={instrumentText}
            onChange={(e) => setInstrumentText(e.target.value)}
          />
        </div>

        {/* Control Panel */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button
            onClick={handleClassify}
            className="bg-blue-600 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded-lg transition duration-300 disabled:opacity-50"
          >
            2. InstrumentAnnotator: CLASSIFY
          </button>
          <button
            onClick={handleScan}
            disabled={!isAnnotated}
            className="bg-yellow-600 hover:bg-yellow-500 text-white font-bold py-2 px-4 rounded-lg transition duration-300 disabled:opacity-50"
          >
            3. LocalAgentCore: CONTRADICTION SCAN
          </button>
          <button
            onClick={handleExecuteRemedy}
            disabled={contradictionFound === null || !contradictionFound}
            className="bg-red-600 hover:bg-red-500 text-white font-bold py-2 px-4 rounded-lg transition duration-300 disabled:opacity-50"
          >
            4. AutoTender/Discharge: EXECUTE REMEDY
          </button>
        </div>
      </div>

      {/* Remedy Log Panel */}
      <div className="w-full md:w-1/3 mt-4 md:mt-0 bg-black p-4 rounded-lg border border-gray-700">
        <h2 className="text-lg text-teal-400 mb-2">NARRATABLE LINEAGE: REMEDY LOG</h2>
        <div className="h-full bg-gray-800 p-2 rounded overflow-y-auto text-xs text-gray-300" style={{maxHeight: 'calc(100vh - 10rem)'}}>
          {remedyLog.map((entry, index) => (
            <p key={index}>{entry}</p>
          ))}
        </div>
      </div>
    </div>
  );
};

export default BillDischargeCockpit;
