export class BillEndorsementModule {
    constructor(appState, knowledgeBase, utils) {
        this.appState = appState;
        this.knowledgeBase = knowledgeBase;
        this.utils = utils;

        // DOM Elements
        this.billUploadInput = document.getElementById('billUpload');
        this.renderPreviewBtn = document.getElementById('renderPreview');
        this.canvas = document.getElementById('previewCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.loader = document.getElementById('loader');
        this.endorsementFieldset = document.getElementById('endorsement-fieldset');
        this.endorsementText = document.getElementById('endorsementText');
        this.qualifierSelect = document.getElementById('qualifier');
        this.qualifierTooltip = document.getElementById('qualifier-tooltip');
        this.saveBtn = document.getElementById('saveEndorsementBtn');
        this.validateNegoBtn = document.getElementById('validateNegotiabilityBtn');
        this.nonNegoBtn = document.getElementById('generateNonNegotiableNoticeBtn');

        this.init();
    }

    init() {
        this.renderPreviewBtn.addEventListener('click', () => this.renderPdfPreview());
        this.validateNegoBtn.addEventListener('click', () => this.validateNegotiability());
        // The save button now triggers the backend processing workflow
        this.saveBtn.addEventListener('click', () => this.processBillOnBackend());
        this.nonNegoBtn.addEventListener('click', () => this.generateNonNegotiableNotice());
        document.getElementById('generateTenderLetterBtn').addEventListener('click', () => this.generateTenderLetter());

        this.billUploadInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                this.appState.billFile = e.target.files[0];
                this.utils.logAction('Bill/instrument uploaded.');
                this.endorsementFieldset.disabled = false;
                this.resetEndorsementState();
            }
        });

        // Add tooltip event listeners
        this.qualifierSelect.addEventListener('mouseover', () => this.showQualifierTooltip());
        this.qualifierSelect.addEventListener('mouseout', () => this.hideQualifierTooltip());
        this.qualifierSelect.addEventListener('mousemove', (e) => this.moveQualifierTooltip(e));
        this.qualifierSelect.addEventListener('change', () => this.showQualifierTooltip()); // Update tooltip on change
    }

    // --- Tooltip Methods ---
    showQualifierTooltip() {
        const selectedOption = this.qualifierSelect.options[this.qualifierSelect.selectedIndex];
        const kbKey = selectedOption.dataset.kbKey;

        if (kbKey && this.knowledgeBase.Endorsements && this.knowledgeBase.Endorsements[kbKey]) {
            const info = this.knowledgeBase.Endorsements[kbKey];
            this.qualifierTooltip.innerHTML = `<strong>${info.summary}</strong><p>${info.detail}</p>`;
            this.qualifierTooltip.classList.remove('hidden');
        }
    }

    hideQualifierTooltip() {
        this.qualifierTooltip.classList.add('hidden');
    }

    moveQualifierTooltip(e) {
        // Position tooltip near the cursor
        this.qualifierTooltip.style.left = `${e.pageX + 15}px`;
        this.qualifierTooltip.style.top = `${e.pageY + 15}px`;
    }

    // --- Core Module Methods ---
    async renderPdfPreview() {
        if (!this.appState.billFile) {
            this.utils.setStatus('Please upload a bill/instrument first.', true);
            return;
        }

        this.loader.classList.remove('hidden');
        this.canvas.classList.add('hidden');

        try {
            const arrayBuffer = await this.appState.billFile.arrayBuffer();
            const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
            const page = await pdf.getPage(1);
            
            this.appState.pdfPage = page;
            const viewport = page.getViewport({ scale: this.canvas.width / page.getViewport({ scale: 1.0 }).width });
            this.appState.pdfViewport = viewport;

            this.canvas.height = viewport.height;
            const renderContext = { canvasContext: this.ctx, viewport: viewport };
            await page.render(renderContext).promise;
            this.utils.setStatus('Preview rendered. Click on the preview to place your endorsement.', false);
            this.utils.logAction('PDF preview rendered.');

            const billText = await this._getPDFText(this.appState.billFile);
            if (this.appState.identifiedCoupons.length > 0) {
                this.utils.logAction(`Identified ${this.appState.identifiedCoupons.length} potential coupons.`);
            }

            this.resetEndorsementState();
        } catch (error) {
            console.error("Error rendering PDF:", error);
            this.utils.setStatus('Failed to render PDF. It might be corrupted or in an unsupported format.', true);
        } finally {
            this.loader.classList.add('hidden');
            this.canvas.classList.remove('hidden');
        }
    }

    async processBillOnBackend() {
        if (!this.appState.billFile) {
            this.utils.setStatus('Please upload a bill/instrument first.', true);
            return;
        }

        this.utils.showLoader();
        this.utils.setStatus('Processing bill on the server...', false);

        const formData = new FormData();
        formData.append('bill', this.appState.billFile);

        try {
            const response = await fetch('/endorse-bill', {
                method: 'POST',
                body: formData,
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'An unknown error occurred.');
            }

            this.utils.setStatus(result.message || 'Bill processed successfully!', false);
            this.utils.logAction('Backend processing complete.');
            
            // Optionally, provide download links for the endorsed files
            if (result.endorsed_files && result.endorsed_files.length > 0) {
                this.utils.logAction(`Endorsed files created: ${result.endorsed_files.join(', ')}`);
                // Here you could add logic to display download links to the user
            }

        } catch (error) {
            console.error('Error processing bill:', error);
            this.utils.setStatus(`Error: ${error.message}`, true);
        } finally {
            this.utils.hideLoader();
        }
    }

    async _getPDFText(file) {
        if (!file) return '';
        const arrayBuffer = await file.arrayBuffer();
        const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
        let fullText = '';
        for (let i = 1; i <= pdf.numPages; i++) {
            const page = await pdf.getPage(i);
            const textContent = await page.getTextContent();
            fullText += textContent.items.map(item => item.str).join(' ');
        }
        return fullText.toLowerCase();
    }

    async validateNegotiability() {
        if (!this.appState.billFile) {
            this.utils.setStatus('Please upload a bill/instrument first.', true);
            return;
        }

        this.utils.showLoader();
        this.utils.setStatus('Validating negotiability...', false);

        try {
            const billText = await this._getPDFText(this.appState.billFile);
            const results = [];
            for (const key in this.knowledgeBase.UCC) {
                const item = this.knowledgeBase.UCC[key];
                const passed = item.test(billText);
                results.push({
                    label: item.label,
                    passed,
                    citation: item.citation,
                    remedy: passed ? null : item.remedyHint
                });
            }

            this.appState.uccValidationResults = results;
            const failures = results.filter(r => !r.passed);
            if (failures.length > 0) {
                this.utils.setStatus('Instrument may not be negotiable. See log for details.', true);
                this.utils.logAction(`Negotiability check failed: ${failures.map(f => f.label).join(', ')}`)
                this.nonNegoBtn.classList.remove('hidden');
            } else {
                this.utils.setStatus('Instrument appears to be negotiable.', false);
                this.utils.logAction('Negotiability check passed.');
                this.nonNegoBtn.classList.add('hidden');
            }

            this.saveBtn.disabled = false;
            document.getElementById('generateTenderLetterBtn').disabled = false;

        } catch (error) {
            console.error("Error validating negotiability:", error);
            this.utils.setStatus('Failed to validate negotiability.', true);
        } finally {
            this.utils.hideLoader();
        }
    }

    generateNonNegotiableNotice() {
        const failures = this.appState.uccValidationResults.filter(r => !r.passed);
        if (failures.length === 0) {
            this.utils.setStatus('No negotiability failures found.', false);
            return;
        }

        let notice = 'NOTICE OF NON-NEGOTIABILITY\n\n';
        notice += `This instrument is non-negotiable for the following reasons:\n\n`;
        failures.forEach(failure => {
            notice += `- ${failure.label}: ${failure.remedy} (${failure.citation})\n`;
        });

        this.utils.generateDownload(notice, 'Non-Negotiable_Notice.txt');
    }

    generateTenderLetter() {
        this.utils.setStatus('Generating tender letter... (not implemented yet)', false);
    }

    resetEndorsementState() {
        this.saveBtn.disabled = true;
        delete this.appState.endorsementCoords;
        delete this.appState.pdfPage;
        delete this.appState.pdfViewport;
        delete this.appState.negotiabilityFailures;
    }

    reset(clearFiles = true) {
        if (clearFiles) {
            this.billUploadInput.value = '';
            this.appState.billFile = null;
        }
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.endorsementFieldset.disabled = true;
        this.nonNegoBtn.classList.add('hidden');
        this.resetEndorsementState();
    }
}