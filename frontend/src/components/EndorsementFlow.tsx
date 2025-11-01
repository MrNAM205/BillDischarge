
import React, { useState, useEffect } from 'react';

const EndorsementFlow = () => {
    const [billFile, setBillFile] = useState(null);
    const [parsedData, setParsedData] = useState(null);
    const [endorsementTemplates, setEndorsementTemplates] = useState([]);
    const [selectedTemplate, setSelectedTemplate] = useState('');
    const [endorsedPdf, setEndorsedPdf] = useState(null);

    useEffect(() => {
        // Fetch endorsement templates from the API
        fetch('http://localhost:8000/api/endorsement-templates')
            .then(response => response.json())
            .then(data => setEndorsementTemplates(data))
            .catch(error => console.error('Error fetching endorsement templates:', error));
    }, []);

    const handleFileChange = (event) => {
        setBillFile(event.target.files[0]);
    };

    const handleUpload = () => {
        if (!billFile) return;

        const formData = new FormData();
        formData.append('file', billFile);

        // Upload the bill for parsing
        fetch('http://localhost:8000/upload', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json()) // Assuming the parsing API returns JSON
        .then(data => setParsedData(data))
        .catch(error => console.error('Error uploading or parsing bill:', error));
    };

    const handleEndorse = () => {
        if (!parsedData || !selectedTemplate) return;

        // Send the parsed data and selected template to the backend for endorsement
        fetch('http://localhost:8000/api/endorse', { // Assuming an /api/endorse endpoint
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                bill_data: parsedData, 
                endorsement_template: selectedTemplate 
            }),
        })
        .then(response => response.blob()) // Assuming the backend returns the endorsed PDF
        .then(blob => {
            const url = URL.createObjectURL(blob);
            setEndorsedPdf(url);
        })
        .catch(error => console.error('Error endorsing document:', error));
    };

    return (
        <div>
            <h2>Endorsement Workflow</h2>

            <div>
                <h3>1. Upload Bill</h3>
                <input type="file" onChange={handleFileChange} accept=".pdf" />
                <button onClick={handleUpload}>Upload and Parse</button>
            </div>

            {parsedData && (
                <div>
                    <h3>2. Verify Parsed Data</h3>
                    <pre>{JSON.stringify(parsedData, null, 2)}</pre>
                    {/* Add editable fields for data correction here */}
                </div>
            )}

            {parsedData && (
                <div>
                    <h3>3. Select Endorsement</h3>
                    <select onChange={(e) => setSelectedTemplate(e.target.value)} value={selectedTemplate}>
                        <option value="">Select a template</option>
                        {Object.entries(endorsementTemplates).map(([name, text]) => (
                            <option key={name} value={name}>{name}</option>
                        ))}
                    </select>
                </div>
            )}

            {parsedData && selectedTemplate && (
                <div>
                    <h3>4. Apply Endorsement</h3>
                    <button onClick={handleEndorse}>Endorse Document</button>
                </div>
            )}

            {endorsedPdf && (
                <div>
                    <h3>5. Download Endorsed PDF</h3>
                    <a href={endorsedPdf} download="endorsed_bill.pdf">Download PDF</a>
                </div>
            )}
        </div>
    );
};

export default EndorsementFlow;
