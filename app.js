// ========================================
// COMMON MISCONCEPTIONS APP
// ========================================

// ===== Global State =====
let misconceptions_en = [];
let misconceptions_es = [];
let currentLanguage = 'en';
let currentMisconception = null;
let isTextExpanded = false;

// ===== DOM Elements =====
const misconceptionElement = document.getElementById('misconception');
const categoryBadge = document.getElementById('category-badge');
const progressFill = document.getElementById('progress-fill');
const factSource = document.getElementById('fact-source');
const sourceText = document.getElementById('source-text');
const countdownTimer = document.getElementById('countdown-timer');
const countdownLabel = document.getElementById('countdown-label');
const streakDisplay = document.getElementById('streak-display');
const languageFab = document.getElementById('language-fab');
const languageFabText = document.getElementById('language-fab-text');
const shareButton = document.getElementById('share-button');
const shareIcon = document.getElementById('share-icon');
const shareModal = document.getElementById('share-modal');
const shareModalTitle = document.getElementById('share-modal-title');
const closeModal = document.getElementById('close-modal');
const copyText = document.getElementById('copy-text');
const sourceLink = document.getElementById('source-link');
const logoText = document.getElementById('logo-text');
const themeToggle = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-icon');
const readMoreBtn = document.getElementById('read-more-btn');
const supportText = document.getElementById('support-text');

// ===== Storage Manager (with error handling) =====
const StorageManager = {
    get(key, fallback = null) {
        try {
            const data = localStorage.getItem(key);
            return data ? JSON.parse(data) : fallback;
        } catch (e) {
            console.warn('localStorage get failed:', e);
            return fallback;
        }
    },

    set(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch (e) {
            console.warn('localStorage set failed:', e);
            return false;
        }
    },

    remove(key) {
        try {
            localStorage.removeItem(key);
            return true;
        } catch (e) {
            console.warn('localStorage remove failed:', e);
            return false;
        }
    }
};

// ===== Theme Management =====
function loadTheme() {
    const savedTheme = StorageManager.get('theme', 'light');
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    StorageManager.set('theme', newTheme);
    updateThemeIcon(newTheme);
}

function updateThemeIcon(theme) {
    themeIcon.textContent = theme === 'dark' ? '◑' : '◐';
}

// ===== Language Detection =====
function detectUserLanguage() {
    const navLang = navigator.language || navigator.userLanguage || 'en';
    // Check if it's any Spanish variant
    if (navLang.toLowerCase().startsWith('es')) {
        return 'es';
    }
    return 'en';
}

// ===== Data Loading =====
async function loadMisconceptionsData() {
    try {
        const [enData, esData] = await Promise.all([
            fetch('data/misconceptions_en.json').then(r => {
                if (!r.ok) throw new Error('Failed to load English data');
                return r.json();
            }),
            fetch('data/misconceptions_es.json').then(r => {
                if (!r.ok) throw new Error('Failed to load Spanish data');
                return r.json();
            })
        ]);

        misconceptions_en = enData;
        misconceptions_es = esData;

        console.log(`Loaded ${misconceptions_en.length} English and ${misconceptions_es.length} Spanish misconceptions`);
        return true;
    } catch (error) {
        console.error('Failed to load misconceptions data:', error);
        misconceptionElement.textContent = 'Failed to load misconceptions. Please refresh the page or check if you\'re running from a web server.';
        misconceptionElement.style.opacity = '1';
        return false;
    }
}

// ===== Helper Functions =====
function getMisconceptions(lang) {
    return lang === 'en' ? misconceptions_en : misconceptions_es;
}

function getTodayDateString() {
    return new Date().toLocaleDateString();
}

function getDailyData(lang) {
    return StorageManager.get(`daily_data_${lang}`, { id: -1, date: null });
}

function setDailyData(lang, id) {
    const data = { id, date: getTodayDateString() };
    StorageManager.set(`daily_data_${lang}`, data);
}

function getAlreadyShown(lang) {
    return StorageManager.get(`shown_${lang}`, []);
}

function setAlreadyShown(lang, shown) {
    StorageManager.set(`shown_${lang}`, shown);
}

function getRandomUnshownIndex(misconceptions, shownIds) {
    const availableIndices = misconceptions
        .map((_, index) => index)
        .filter(index => !shownIds.includes(misconceptions[index].id));

    if (availableIndices.length === 0) {
        return null;
    }

    const randomIndex = Math.floor(Math.random() * availableIndices.length);
    return availableIndices[randomIndex];
}

// ===== Streak Tracking =====
function updateStreak() {
    const today = getTodayDateString();
    const streakData = StorageManager.get('streak_data', {
        lastVisit: null,
        currentStreak: 0
    });

    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    const yesterdayString = yesterday.toLocaleDateString();

    if (streakData.lastVisit === today) {
        return streakData.currentStreak;
    } else if (streakData.lastVisit === yesterdayString) {
        streakData.currentStreak += 1;
    } else if (streakData.lastVisit === null) {
        streakData.currentStreak = 1;
    } else {
        streakData.currentStreak = 1;
    }

    streakData.lastVisit = today;
    StorageManager.set('streak_data', streakData);

    return streakData.currentStreak;
}


// ===== Main Display Function =====
async function showDailyMisconception() {
    const misconceptions = getMisconceptions(currentLanguage);

    if (misconceptions.length === 0) {
        await loadMisconceptionsData();
        return showDailyMisconception();
    }

    const today = getTodayDateString();
    let dailyData = getDailyData(currentLanguage);

    if (dailyData.date !== today) {
        let shown = getAlreadyShown(currentLanguage);

        if (shown.length >= misconceptions.length) {
            shown = [];
        }

        const randomIndex = getRandomUnshownIndex(misconceptions, shown);

        if (randomIndex === null) {
            dailyData = { id: misconceptions[0].id, date: today };
        } else {
            const selectedMisconception = misconceptions[randomIndex];
            shown.push(selectedMisconception.id);
            setAlreadyShown(currentLanguage, shown);
            dailyData = { id: selectedMisconception.id, date: today };
        }

        setDailyData(currentLanguage, dailyData.id);
    }

    const misconception = misconceptions.find(m => m.id === dailyData.id) || misconceptions[0];
    displayMisconception(misconception);
}

function displayMisconception(misconception) {
    currentMisconception = misconception;
    isTextExpanded = false;

    // Display text
    misconceptionElement.textContent = misconception.text;
    misconceptionElement.classList.remove('fade-in');

    // Trigger reflow
    void misconceptionElement.offsetWidth;

    misconceptionElement.classList.add('fade-in');

    // Handle long text
    const textLength = misconception.text.length;
    if (textLength > 400) {
        misconceptionElement.classList.add('clamped');
        readMoreBtn.style.display = 'block';
        readMoreBtn.textContent = currentLanguage === 'en' ? 'Read More' : 'Leer Más';
    } else {
        misconceptionElement.classList.remove('clamped');
        readMoreBtn.style.display = 'none';
    }

    // Update category badge
    categoryBadge.textContent = misconception.category;

    // Update progress bar (visual only, no text)
    const shown = getAlreadyShown(currentLanguage);
    const total = getMisconceptions(currentLanguage).length;
    const percentage = Math.round((shown.length / total) * 100);
    progressFill.style.width = `${percentage}%`;

    // Update fact source link
    factSource.href = misconception.source_url;

    // Update streak display
    const streak = updateStreak();
    if (streak > 0) {
        streakDisplay.style.display = 'block';
        const streakText = currentLanguage === 'en'
            ? `${streak} day${streak > 1 ? 's' : ''} streak 🔥`
            : `Racha de ${streak} día${streak > 1 ? 's' : ''} 🔥`;
        streakDisplay.textContent = streakText;
    }
}

function toggleReadMore() {
    isTextExpanded = !isTextExpanded;

    if (isTextExpanded) {
        misconceptionElement.classList.remove('clamped');
        readMoreBtn.textContent = currentLanguage === 'en' ? 'Read Less' : 'Leer Menos';
    } else {
        misconceptionElement.classList.add('clamped');
        readMoreBtn.textContent = currentLanguage === 'en' ? 'Read More' : 'Leer Más';
    }
}

// ===== Language Toggle =====
function toggleLanguage() {
    misconceptionElement.classList.remove('fade-in');
    setTimeout(() => {
        currentLanguage = currentLanguage === 'en' ? 'es' : 'en';
        updateUILanguage();
        showDailyMisconception();
    }, 300);
}

function updateUILanguage() {
    if (currentLanguage === 'en') {
        languageFabText.textContent = 'ES';
        sourceLink.href = 'https://en.wikipedia.org/wiki/List_of_common_misconceptions';
        document.documentElement.lang = 'en';
        document.title = 'Not Like That - Daily Misconceptions';
        countdownLabel.textContent = 'Next misconception in:';
        sourceText.textContent = 'View Source';
        logoText.textContent = 'Not Like That';
        supportText.textContent = 'Buy me a coffee';
    } else {
        languageFabText.textContent = 'EN';
        sourceLink.href = 'https://es.wikipedia.org/wiki/Anexo:Falsos_mitos';
        document.documentElement.lang = 'es';
        document.title = 'No Es Así - Mitos Diarios';
        countdownLabel.textContent = 'Próximo mito en:';
        sourceText.textContent = 'Ver Fuente';
        logoText.textContent = 'No Es Así';
        supportText.textContent = 'Invítame un café';
    }
}

// ===== Countdown Timer =====
function updateCountdownDisplay() {
    const now = new Date();
    const tomorrow = new Date(now);
    tomorrow.setDate(tomorrow.getDate() + 1);
    tomorrow.setHours(0, 0, 0, 0);

    const timeUntilMidnight = tomorrow - now;

    const hours = Math.floor(timeUntilMidnight / (1000 * 60 * 60));
    const minutes = Math.floor((timeUntilMidnight % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((timeUntilMidnight % (1000 * 60)) / 1000);

    const formatted = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    countdownTimer.textContent = formatted;
}


// ===== Social Sharing =====
function openShareModal() {
    shareModal.style.display = 'flex';
    updateShareLinks();
    updateSharePreview();

    if (currentLanguage === 'en') {
        shareModalTitle.textContent = 'Share this misconception';
    } else {
        shareModalTitle.textContent = 'Compartir este mito';
    }
}

function updateSharePreview() {
    if (currentMisconception) {
        document.getElementById('share-preview-category').textContent = currentMisconception.category;
        document.getElementById('share-preview-text').textContent = currentMisconception.text;
        document.getElementById('share-preview-logo').textContent =
            currentLanguage === 'en' ? 'Not Like That' : 'No Es Así';
    }
}

function closeShareModal() {
    shareModal.style.display = 'none';
}

function updateShareLinks() {
    const text = currentMisconception ? currentMisconception.text : misconceptionElement.textContent;
    const url = window.location.href;
    const encodedText = encodeURIComponent(text.substring(0, 280)); // Twitter limit
    const encodedUrl = encodeURIComponent(url);

    document.getElementById('share-twitter').href =
        `https://twitter.com/intent/tweet?text=${encodedText}&url=${encodedUrl}`;

    document.getElementById('share-facebook').href =
        `https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}&quote=${encodedText}`;

    document.getElementById('share-whatsapp').href =
        `https://wa.me/?text=${encodedText}%20${encodedUrl}`;

    document.getElementById('share-reddit').href =
        `https://reddit.com/submit?url=${encodedUrl}&title=${encodedText}`;

    document.getElementById('share-mastodon').href =
        `https://mastodon.social/share?text=${encodedText}%20${encodedUrl}`;
}

async function copyLinkToClipboard() {
    try {
        await navigator.clipboard.writeText(window.location.href);
        const copyButton = document.getElementById('copy-link');
        const originalHTML = copyButton.innerHTML;
        copyButton.innerHTML = currentLanguage === 'en' ? '✓ Copied!' : '✓ ¡Copiado!';
        setTimeout(() => {
            copyButton.innerHTML = originalHTML;
        }, 2000);
    } catch (err) {
        console.error('Failed to copy link:', err);
    }
}

async function tryNativeShare() {
    if (navigator.share) {
        try {
            await navigator.share({
                title: document.title,
                text: currentMisconception ? currentMisconception.text : misconceptionElement.textContent,
                url: window.location.href
            });
            return true;
        } catch (err) {
            if (err.name !== 'AbortError') {
                console.error('Share failed:', err);
            }
            return false;
        }
    }
    return false;
}

function handleShare() {
    openShareModal();
}

// ===== Event Listeners =====
languageFab.addEventListener('click', toggleLanguage);
shareButton.addEventListener('click', handleShare);
closeModal.addEventListener('click', closeShareModal);
document.getElementById('copy-link').addEventListener('click', copyLinkToClipboard);
document.getElementById('native-share').addEventListener('click', tryNativeShare);
themeToggle.addEventListener('click', toggleTheme);
readMoreBtn.addEventListener('click', toggleReadMore);

shareModal.addEventListener('click', (e) => {
    if (e.target === shareModal) {
        closeShareModal();
    }
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && shareModal.style.display === 'flex') {
        closeShareModal();
    }
});

// ===== Initial Setup =====
async function initialize() {
    // Load theme first
    loadTheme();

    // Detect user language
    currentLanguage = detectUserLanguage();

    // Update UI
    updateUILanguage();

    // Load misconceptions data
    const loaded = await loadMisconceptionsData();

    if (loaded) {
        // Show daily misconception
        await showDailyMisconception();

        // Start countdown timer
        updateCountdownDisplay();
        setInterval(updateCountdownDisplay, 1000);
    }
}

// Start the app
initialize();
