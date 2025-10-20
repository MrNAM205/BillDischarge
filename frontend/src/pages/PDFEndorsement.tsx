
import React, { useState } from 'react';

const PDFEndorsement: React.FC = () => {
    const [file, setFile] = useState<File | null>(null);
    const [endorsementText, setEndorsementText] = useState('Conditional Acceptance for Value - UCC 1-308');
    const [fontName, setFontName] = useState('Helvetica');
    const [fontSize, setFontSize] = useState(12);
    const [inkColor, setInkColor] = useState('blue');
    const [endorsedFile, setEndorsedFile] = useState<string | null>(null);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            setFile(e.target.files[0]);
        }
    };

    const handleEndorse = () => {
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        const options = {
            endorsement_text: endorsementText,
            font_name: fontName,
            font_size: fontSize,
            ink_color: inkColor,
        };

        fetch(`http://localhost:8000/api/endorse-bill/?${new URLSearchParams(options as any)}`, {
            method: 'POST',
            body: formData,
        })
            .then(response => response.blob())
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                setEndorsedFile(url);
            });
    };

    return (
        <div>
            <h2>Endorse PDF</h2>
            <div>
                <label>PDF File:</label>
                <input type="file" accept=".pdf" onChange={handleFileChange} />
            </div>
            <div>
                <label>Endorsement Text:</label>
                <input type="text" value={endorsementText} onChange={e => setEndorsementText(e.target.value)} />
            </div>
            <div>
                <label>Font Name:</label>
                <input type="text" value={fontName} onChange={e => setFontName(e.target.value)} />
            </div>
            <div>
                <label>Font Size:</label>
                <input type="number" value={fontSize} onChange={e => setFontSize(parseInt(e.target.value, 10))} />
            </div>
            <div>
                <label>Ink Color:</label>
                <input type="text" value={inkColor} onChange={e => setInkColor(e.target.value)} />
            </div>
            <button onClick={handleEndorse}>Endorse</button>
            {endorsedFile && (
                <div>
                    <h3>Endorsed PDF</h3>
                    <a href={endorsedFile} download="endorsed.pdf">Download Endorsed PDF</a>
                </div>
            )}
        </div>
    );
};

export default PDFEndorsement;
