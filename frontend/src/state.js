import { CONSTANTS } from './constants.js';
import { setStatus } from './utils.js';

export function getInitialState() {
    const savedCreditors = JSON.parse(localStorage.getItem(CONSTANTS.LOCAL_STORAGE.CREDITORS)) || [];
    const savedFdcpaLog = JSON.parse(localStorage.getItem(CONSTANTS.LOCAL_STORAGE.FDCPA_LOG)) || [];
    const savedHistory = JSON.parse(localStorage.getItem(CONSTANTS.LOCAL_STORAGE.INSTRUMENT_HISTORY)) || [];
    const savedProfile = JSON.parse(localStorage.getItem(CONSTANTS.LOCAL_STORAGE.USER_PROFILE)) || { name: '', address: '' };

    return {
        pdfPage: null,
        endorsement: { text: null, x: 0, y: 0 },
        userProfile: savedProfile,
        creditors: savedCreditors,
        history: savedHistory,
        loopState: 'intake', // intake, validate, remedy, log, reflect
        validationResults: { found: [], missing: [] },
        uccValidationResults: { passed: [], failed: [] },
        fdcpaLog: savedFdcpaLog,
        identifiedCoupons: []
    };
}

export let appState = getInitialState();

export function logAction(action) {
    const timestamp = new Date().toLocaleString();
    const id = Date.now(); // Add a unique ID
    appState.history.push({ id, timestamp, action });
    localStorage.setItem(CONSTANTS.LOCAL_STORAGE.INSTRUMENT_HISTORY, JSON.stringify(appState.history));
    renderHistory();
}



export function renderHistory() {
    const logEl = document.getElementById('instrumentLog');
    if (appState.history.length === 0) {
        logEl.innerHTML = '<p class="text-muted">No history yet.</p>';
        return;
    }
    appState.history.map(entry => `
        <li data-id="${entry.id}">
            <span class="log-text">${entry.timestamp}: ${entry.action}</span>
            <div class="log-actions">
                <button class="edit-log-btn" title="Edit entry">✏️</button>
                <button class="delete-log-btn" title="Delete entry">🗑️</button>
            </div>
        </li>
    `).join('');
    logEl.innerHTML = `<ul></ul>`;
}

export function deleteHistoryEntry(id) {
    if (!confirm('Are you sure you want to delete this log entry?')) {
        return;
    }
    appState.history = appState.history.filter(entry => entry.id !== id);
    localStorage.setItem(CONSTANTS.LOCAL_STORAGE.INSTRUMENT_HISTORY, JSON.stringify(appState.history));
    renderHistory();
    setStatus('Log entry deleted.', false);
}

export function editHistoryEntry(id, logItemElement) {
    // Prevent multiple edits at once
    if (document.querySelector('.edit-container')) {
        return;
    }

    const logTextSpan = logItemElement.querySelector('.log-text');
    const logActionsDiv = logItemElement.querySelector('.log-actions');
    const entry = appState.history.find(e => e.id === id);
    if (!entry) return;

    logTextSpan.style.display = 'none';
    logActionsDiv.style.display = 'none';

    const editContainer = document.createElement('div');
    editContainer.className = 'edit-container';
    editContainer.innerHTML = `
        <input type="text" class="edit-log-input" value="${entry.action}">
        <button class="save-log-btn">Save</button>
        <button class="cancel-log-btn">Cancel</button>
    `;

    logItemElement.appendChild(editContainer);
    const input = editContainer.querySelector('input');
    input.focus();
    input.select();

    const saveHandler = () => {
        const newAction = input.value.trim();
        if (newAction) {
            entry.action = newAction;
            localStorage.setItem(CONSTANTS.LOCAL_STORAGE.INSTRUMENT_HISTORY, JSON.stringify(appState.history));
            setStatus('Log entry updated.', false);
        }
        renderHistory(); // Re-render to show updated state and remove edit UI
    };

    const cancelHandler = () => {
        renderHistory(); // Just re-render to cancel
    };

    editContainer.querySelector('.save-log-btn').addEventListener('click', saveHandler);
    editContainer.querySelector('.cancel-log-btn').addEventListener('click', cancelHandler);
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') saveHandler();
        if (e.key === 'Escape') cancelHandler();
    });
}

export function handleHistoryAction(e) {
    const target = e.target;
    const logItem = target.closest('li[data-id]');
    if (!logItem) return;

    const logId = Number(logItem.dataset.id);

    if (target.classList.contains('delete-log-btn')) {
        deleteHistoryEntry(logId);
    } else if (target.classList.contains('edit-log-btn')) {
        editHistoryEntry(logId, logItem);
    }
}