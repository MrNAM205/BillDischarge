import { appState } from './state.js';

/**
 * Creates a text file from a string and triggers a browser download.
 * @param {string} content The text content of the file.
 * @param {string} filename The desired name for the downloaded file.
 */
export function generateDownload(content, filename) {
    try {
        const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
        setStatus(`File "${filename}" downloaded successfully.`, false, true);
    } catch (error) {
        console.error('Error generating download:', error);
        setStatus('Failed to generate download link.', true);
    }
}

/**
 * Copies a string to the user's clipboard.
 * @param {string} content The text to copy.
 * @param {string} successMessage The message to display on success.
 */
export function copyToClipboard(content, successMessage) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(content).then(() => {
            setStatus(successMessage || 'Text copied to clipboard.', false, true);
        }).catch(err => {
            console.error('Failed to copy text: ', err);
            setStatus('Failed to copy text to clipboard.', true);
        });
    } else {
        setStatus('Clipboard API not available in this browser.', true);
    }
}

// DOM Elements (moved from script.js)
const globalLoader = document.getElementById('global-loader');

// LOADER UTILITIES (moved from script.js)
export function showLoader() { globalLoader.classList.remove('hidden'); }
export function hideLoader() { globalLoader.classList.add('hidden'); }

// UTILITY FUNCTIONS (moved from script.js)


export function setStatus(message, isError = false) {
    const statusEl = document.getElementById('endorsementStatus');
    statusEl.textContent = message;
    if (isError) {
        statusEl.style.color = 'var(--status-error-color)';
    } else if (message) {
        statusEl.style.color = 'var(--status-info-color)';
    } else {
        statusEl.style.color = 'var(--text-color)';
    }
}

export function download(data, filename, type) {
    const blob = new Blob([data], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

export async function extractTextFromPdf(file) {
    showLoader();
    setStatus('Extracting text from PDF...', false);
    try {
        const arrayBuffer = await file.arrayBuffer();
        const typedarray = new Uint8Array(arrayBuffer);
        const pdf = await pdfjsLib.getDocument(typedarray).promise;
        let fullText = '';
        for (let i = 1; i <= pdf.numPages; i++) {
            const page = await pdf.getPage(i);
            const textContent = await page.getTextContent();
            fullText += textContent.items.map(item => item.str).join(' ');
        }
        setStatus('Text extracted successfully.', false);
        return fullText;
    } catch (error) {
        console.error("Error extracting text from PDF:", error);
        setStatus('Failed to process PDF. It may be corrupted or encrypted.', true);
        return null; // Return null to indicate failure
    } finally {
        hideLoader(); // Ensure loader is always hidden
    }
}

export function updateSovereignLoopUI() {
    const states = ['intake', 'validate', 'remedy', 'log', 'reflect'];
    states.forEach(state => {
        const el = document.getElementById(`loop-${state}`);
        if (el) {
            el.classList.toggle('active', state === appState.loopState);
        }
    });
}

export function identifyCoupons(text) {
    const coupons = [];
    const couponKeywords = /(coupon|voucher|discount|promo code|rebate|certificate|interest payment|dividend)/gi;
    const financialKeywords = /(bond|note|security|interest|dividend|payable|bearer|order|amount)/gi;

    let match;
    while ((match = couponKeywords.exec(text)) !== null) {
        // Basic identification: look for keywords
        const snippet = text.substring(Math.max(0, match.index - 50), Math.min(text.length, match.index + 50));
        let type = 'General';

        if (financialKeywords.test(snippet)) {
            type = 'Financial';
        } else if (/food|benefit|assistance/i.test(snippet)) {
            type = 'Benefit';
        }

        coupons.push({
            keyword: match[0],
            type: type,
            snippet: snippet.trim()
        });
    }
    return coupons;
}
