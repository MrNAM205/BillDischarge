import { CONSTANTS } from './constants.js';

export function handleThemeToggle() {
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle.checked) {
        document.body.classList.add('dark-mode');
        localStorage.setItem(CONSTANTS.LOCAL_STORAGE.THEME, 'dark');
    } else {
        document.body.classList.remove('dark-mode');
        localStorage.setItem(CONSTANTS.LOCAL_STORAGE.THEME, 'light');
    }
}

export function applySavedTheme() {
    const themeToggle = document.getElementById('themeToggle');
    const savedTheme = localStorage.getItem(CONSTANTS.LOCAL_STORAGE.THEME);
    if (savedTheme) {
        themeToggle.checked = savedTheme === 'dark';
    }
    handleThemeToggle();
}
