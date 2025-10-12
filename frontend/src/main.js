import { CONSTANTS } from './constants.js';
import { appState, logAction, renderHistory, getInitialState } from './state.js';
import { showLoader, hideLoader, setStatus, download, extractTextFromPdf, updateSovereignLoopUI } from './utils.js';
import { handleThemeToggle, applySavedTheme } from './theme.js';
import { BillEndorsementModule } from './billEndorsement.js';
import { VehicleFinancingModule } from './vehicleFinancing.js';
import { CreditReportAnalysisModule } from './creditReportAnalysis.js';
import { FdcpaLogger } from './fdcpaLogger.js';
import { CreditorManagerModule } from './creditorManager.js';
import { UserProfileModule } from './userProfile.js';
import { KNOWLEDGE_BASE } from './knowledgeBase.js';

document.addEventListener('DOMContentLoaded', () => {
    // --- LIBRARIES ---
    

    // --- MODULE INSTANCES ---
    let billEndorsement, vehicleFinancing, creditReportAnalysis, fdcpaLogger, userProfile, creditorManager;

    // --- DOM ELEMENTS ---
    const resetAppBtn = document.getElementById('resetAppBtn');
    const trackInstrumentBtn = document.getElementById('trackInstrumentBtn');
    const customLogEntryInput = document.getElementById('customLogEntry');
    const themeToggle = document.getElementById('themeToggle');
    

    // --- EVENT HANDLERS ---
    function handleTrackInstrument() {
        const note = customLogEntryInput.value.trim();
        if (!note) {
            setStatus("Please enter a note for the log.", true);
            return;
        }
        logAction(`Custom Note: "${note}"`);
        customLogEntryInput.value = '';
        setStatus("Custom note added to log.", false);
    }

    function handleReset(clearFiles = true) {
        if (!confirm('Are you sure you want to reset all application data? This action cannot be undone.')) {
            return;
        }
        localStorage.removeItem(CONSTANTS.LOCAL_STORAGE.INSTRUMENT_HISTORY);
        localStorage.removeItem(CONSTANTS.LOCAL_STORAGE.FDCPA_LOG);
        localStorage.removeItem(CONSTANTS.LOCAL_STORAGE.CREDITORS);
        localStorage.removeItem(CONSTANTS.LOCAL_STORAGE.USER_PROFILE);

                let state = getInitialState();
        Object.assign(appState, state);
        billEndorsement.reset(clearFiles);
        vehicleFinancing.reset(clearFiles);
        creditReportAnalysis.reset();
        creditorManager.renderCreditorList();
        fdcpaLogger.reset();
        
        userProfile.loadProfile(); // Reloads the empty profile into the form
        customLogEntryInput.value = '';
        setStatus('');
        renderAllLogs();
        updateSovereignLoopUI();
    }

    function renderAllLogs() {
        renderHistory();
        fdcpaLogger.renderLog();
    }

    // --- INITIALIZATION ---
    const utils = {
        logAction,
        updateSovereignLoopUI,
        download,
        extractTextFromPdf,
        setStatus,
        showLoader,
        hideLoader
    };

    // Instantiate classes instead of calling .init() on modules.
    // Ensure your module files (e.g., vehicleFinancing.js) define these classes.
    billEndorsement = new BillEndorsementModule(appState, KNOWLEDGE_BASE, utils);
    vehicleFinancing = new VehicleFinancingModule(appState, KNOWLEDGE_BASE, utils);
    creditReportAnalysis = new CreditReportAnalysisModule(appState, KNOWLEDGE_BASE, utils);
    fdcpaLogger = new FdcpaLogger(appState, KNOWLEDGE_BASE, utils);
    creditorManager = new CreditorManagerModule(appState, utils);
    userProfile = new UserProfileModule(appState, utils);

    resetAppBtn.addEventListener('click', () => handleReset(true));
    trackInstrumentBtn.addEventListener('click', handleTrackInstrument);
    themeToggle.addEventListener('change', handleThemeToggle);

    applySavedTheme();
    renderAllLogs(); // Render logs loaded from localStorage
    updateSovereignLoopUI();
});
