const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const langSelect = document.getElementById('lang-select');
const profileContainer = document.getElementById('profile-container');
const detectedLangTag = document.getElementById('detected-lang');
const clearChatBtn = document.getElementById('clear-chat');
const quickBtns = document.querySelectorAll('.quick-btn');

let sessionId = null;
let currentLang = 'en';

const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? 'http://localhost:8000' 
    : 'https://vidhyapath.onrender.com';

console.log('🚀 VidyaPath v1.1.6 - Profile Accuracy Fix');
window.__VIDYAPATH_VERSION__ = '1.1.6';

// Local translation dictionary for UI labels (Offline support)
const UI_TRANSLATIONS = {
    'ta': { // Tamil
        'Select Language': 'மொழியைத் தேர்ந்தெடுக்கவும்',
        'Try asking': 'கேட்டுப் பாருங்கள்',
        'What can I study after 12th?': '12 ஆம் வகுப்பிற்குப் பிறகு நான் என்ன படிக்கலாம்?',
        'Schemes for women entrepreneurs?': 'பெண் தொழில்முனைவோருக்கான திட்டங்கள்?',
        'Best job portals for freshers?': 'ஆரம்பநிலையினருக்கான சிறந்த வேலைவாய்ப்பு இணையதளங்கள்?',
        'Scholarships for Class 10?': '10 ஆம் வகுப்பு மாணவர்களுக்கான உதவித்தொகை?',
        'Clear Chat History': 'அரட்டை வரலாற்றை அழிக்கவும்',
        'AI Career Co-pilot': 'AI தொழில் வழிகாட்டி',
        'Online': 'ஆன்லைனில்',
        'Student Profile': 'மாணவர் சுயவிவரம்',
        'Chat with me to build your profile!': 'உங்கள் சுயவிவரத்தை உருவாக்க என்னுடன் அரட்டையடிக்கவும்!',
        'Type your question here...': 'உங்கள் கேள்வியை இங்கே தட்டச்சு செய்யவும்...',
        'Send': 'அனுப்பு',
        '👋 Namaste! I\'m VidyaPath. I can help you with career guidance, scholarships, and government schemes. What\'s on your mind today?': '👋 நமஸ்தே! நான் வித்யாபாத். தொழில் வழிகாட்டுதல், உதவித்தொகை மற்றும் அரசு திட்டங்களுக்கு நான் உங்களுக்கு உதவ முடியும். இன்று உங்கள் மனதில் என்ன இருக்கிறது?',
        'History cleared. How can I help you today?': 'வரலாறு அழிக்கப்பட்டது. இன்று நான் உங்களுக்கு எப்படி உதவ முடியும்?'
    },
    'te': { // Telugu
        'Select Language': 'భాషను ఎంచుకోండి',
        'Try asking': 'అడిగి చూడండి',
        'What can I study after 12th?': '12వ తరగతి తర్వాత నేను ఏమి చదవగలను?',
        'Schemes for women entrepreneurs?': 'మహిళా పారిశ్రామికవేత్తల కోసం పథకాలు?',
        'Best job portals for freshers?': 'ఫ్రెషర్స్ కోసం ఉత్తమ ఉద్యోగ పోర్టల్స్?',
        'Scholarships for Class 10?': '10వ తరగతికి స్కాలర్‌షిప్‌లు?',
        'Clear Chat History': 'చాట్ చరిత్రను క్లియర్ చేయండి',
        'AI Career Co-pilot': 'AI కెరీర్ కో-పైలట్',
        'Online': 'ఆన్‌లైన్',
        'Student Profile': 'విద్యార్థి ప్రొఫైల్',
        'Chat with me to build your profile!': 'మీ ప్రొఫైల్‌ను రూపొందించడానికి నాతో చాట్ చేయండి!',
        'Type your question here...': 'మీ ప్రశ్నను ఇక్కడ టైప్ చేయండి...',
        'Send': 'పంపండి',
        '👋 Namaste! I\'m VidyaPath. I can help you with career guidance, scholarships, and government schemes. What\'s on your mind today?': '👋 నమస్తే! నేను విద్యాపథ్. నేను మీకు కెరీర్ మార్గదర్శకత్వం, స్కాలర్‌షిప్‌లు మరియు ప్రభుత్వ పథకాలలో సహాయం చేయగలను. ఈరోజు మీ మనసులో ఏముంది?',
        'History cleared. How can I help you today?': 'చరిత్ర క్లియర్ చేయబడింది. ఈరోజు నేను మీకు ఎలా సహాయం చేయగలను?'
    },
    'hi': { // Hindi
        'Select Language': 'भाषा चुनें',
        'Try asking': 'पूछने का प्रयास करें',
        'What can I study after 12th?': 'मैं 12वीं के बाद क्या पढ़ सकता हूँ?',
        'Schemes for women entrepreneurs?': 'महिला उद्यमियों के लिए योजनाएं?',
        'Best job portals for freshers?': 'नए लोगों के लिए सर्वश्रेष्ठ जॉब पोर्टल?',
        'Scholarships for Class 10?': 'कक्षा 10 के लिए छात्रवृत्ति?',
        'Clear Chat History': 'चैट इतिहास मिटाएं',
        'AI Career Co-pilot': 'AI करियर को-पायलट',
        'Online': 'ऑनलाइन',
        'Student Profile': 'छात्र प्रोफ़ाइल',
        'Chat with me to build your profile!': 'अपनी प्रोफ़ाइल बनाने के लिए मुझसे चैट करें!',
        'Type your question here...': 'अपना प्रश्न यहाँ टाइप करें...',
        'Send': 'भेजें',
        '👋 Namaste! I\'m VidyaPath. I can help you with career guidance, scholarships, and government schemes. What\'s on your mind today?': '👋 नमस्ते! मैं विद्यापथ हूँ। मैं करियर मार्गदर्शन, छात्रवृत्ति और सरकारी योजनाओं में आपकी मदद कर सकता हूँ। आज आपके मन में क्या है?',
        'History cleared. How can I help you today?': 'इतिहास साफ़ कर दिया गया। आज मैं आपकी कैसे मदद कर सकता हूँ?'
    },
    'kn': { // Kannada
        'Select Language': 'ಭಾಷೆಯನ್ನು ಆರಿಸಿ',
        'Try asking': 'ಕೇಳಲು ಪ್ರಯತ್ನಿಸಿ',
        'What can I study after 12th?': '12 ನೇ ತರಗತಿಯ ನಂತರ ನಾನು ಏನು ಓದಬಹುದು?',
        'Schemes for women entrepreneurs?': 'ಮಹಿಳಾ ಉದ್ಯಮಿಗಳಿಗಾಗಿ ಯೋಜನೆಗಳು?',
        'Best job portals for freshers?': 'ಹೊಸಬರಿಗಾಗಿ ಅತ್ಯುತ್ತಮ ಉದ್ಯೋಗ ಪೋರ್ಟಲ್‌ಗಳು?',
        'Scholarships for Class 10?': '10 ನೇ ತರಗತಿಗೆ ವಿದ್ಯಾರ್ಥಿವೇತನಗಳು?',
        'Clear Chat History': 'ಚಾಟ್ ಹಿಸ್ಟರಿ ಅಳಿಸಿ',
        'AI Career Co-pilot': 'AI ವೃತ್ತಿಜೀವನದ ಸಹ-ಪೈಲಟ್',
        'Online': 'ಆನ್‌ಲೈನ್',
        'Student Profile': 'ವಿದ್ಯಾರ್ಥಿ ವಿವರ',
        'Chat with me to build your profile!': 'ನಿಮ್ಮ ಪ್ರೊಫೈಲ್ ನಿರ್ಮಿಸಲು ನನ್ನೊಂದಿಗೆ ಚಾಟ್ ಮಾಡಿ!',
        'Type your question here...': 'ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಇಲ್ಲಿ ಟೈಪ್ ಮಾಡಿ...',
        'Send': 'ಕಳುಹಿಸಿ',
        '👋 Namaste! I\'m VidyaPath. I can help you with career guidance, scholarships, and government schemes. What\'s on your mind today?': '👋 ನಮಸ್ತೆ! ನಾನು ವಿದ್ಯಾಪತ್. ವೃತ್ತಿ ಮಾರ್ಗದರ್ಶನ, ವಿದ್ಯಾರ್ಥಿವೇತನಗಳು ಮತ್ತು ಸರ್ಕಾರಿ ಯೋಜನೆಗಳಲ್ಲಿ ನಾನು ನಿಮಗೆ ಸಹಾಯ ಮಾಡಬಲ್ಲೆ. ಇಂದು ನಿಮ್ಮ ಮನಸ್ಸಿನಲ್ಲಿ ಏನಿದೆ?',
        'History cleared. How can I help you today?': 'ಇತಿಹಾಸವನ್ನು ಅಳಿಸಲಾಗಿದೆ. ಇಂದು ನಾನು ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಲ್ಲೆ?'
    },
    'mr': { // Marathi
        'Select Language': 'भाषा निवडा',
        'Try asking': 'विचारण्याचा प्रयत्न करा',
        'What can I study after 12th?': 'मी १२ वी नंतर काय अभ्यास करू शकतो?',
        'Schemes for women entrepreneurs?': 'महिला उद्योजकांसाठी योजना?',
        'Best job portals for freshers?': 'फ्रेशर्ससाठी सर्वोत्तम जॉब पोर्टल्स?',
        'Scholarships for Class 10?': '१० वी साठी शिष्यवृत्ती?',
        'Clear Chat History': 'चॅट इतिहास साफ करा',
        'AI Career Co-pilot': 'AI करिअर को-पायलट',
        'Online': 'ऑनलाइन',
        'Student Profile': 'विद्यार्थी प्रोफाइल',
        'Chat with me to build your profile!': 'तुमची प्रोफाइल तयार करण्यासाठी माझ्याशी चॅट करा!',
        'Type your question here...': 'तुमचा ಪ್ರಶ್ನ येथे टाइप करा...',
        'Send': 'पाठवा',
        '👋 Namaste! I\'m VidyaPath. I can help you with career guidance, scholarships, and government schemes. What\'s on your mind today?': '👋 नमस्ते! मी विद्यापथ आहे. मी तुम्हाला करिअर मार्गदर्शन, शिष्यवृत्ती आणि सरकारी योजनांमध्ये मदत करू शकतो. आज तुमच्या मनात काय आहे?',
        'History cleared. How can I help you today?': 'इतिहास साफ केला. आज मी तुम्हाला कशी मदत करू शकतो?'
    },
    'ml': { // Malayalam
        'Select Language': 'ഭാഷ തിരഞ്ഞെടുക്കുക',
        'Try asking': 'ചോദിച്ചു നോക്കൂ',
        'What can I study after 12th?': '12-ാം ക്ലാസിന് ശേഷം എനിക്ക് എന്ത് പഠിക്കാം?',
        'Schemes for women entrepreneurs?': 'വനിതാ സംരംഭകർക്കുള്ള പദ്ധതികൾ?',
        'Best job portals for freshers?': 'ഫ്രഷേഴ്സിനായി മികച്ച തൊഴിൽ പോർട്ടലുകൾ?',
        'Scholarships for Class 10?': '10-ാം ക്ലാസ്സുകാർക്കുള്ള സ്കോളർഷിപ്പുകൾ?',
        'Clear Chat History': 'ചാറ്റ് ഹിസ്റ്ററി ക്ലിയർ ചെയ്യുക',
        'AI Career Co-pilot': 'AI കരിയർ കോ-പൈലറ്റ്',
        'Online': 'ഓൺലൈൻ',
        'Student Profile': 'സ്റ്റുഡന്റ് പ്രൊഫൈൽ',
        'Chat with me to build your profile!': 'നിങ്ങളുടെ പ്രൊഫൈൽ നിർമ്മിക്കാൻ എന്നോട് ചാറ്റ് ചെയ്യുക!',
        'Type your question here...': 'നിങ്ങളുടെ ചോദ്യം ഇവിടെ ടൈപ്പ് ചെയ്യുക...',
        'Send': 'അയയ്ക്കുക',
        '👋 Namaste! I\'m VidyaPath. I can help you with career guidance, scholarships, and government schemes. What\'s on your mind today?': '👋 നമസ്തേ! ഞാൻ വിദ്യാപാഥ്. കരിയർ ഗൈഡൻസ്, സ്കോളർഷിപ്പുകൾ, സർക്കാർ പദ്ധതികൾ എന്നിവയിൽ എനിക്ക് നിങ്ങളെ സഹായിക്കാനാകും. ഇന്ന് നിങ്ങളുടെ മനസ്സിൽ എന്താണുള്ളത്?',
        'History cleared. How can I help you today?': 'ചരിത്രം നീക്കം ചെയ്തു. ഇന്ന് എനിക്ക് നിങ്ങളെ എങ്ങനെ സഹായിക്കാനാകും?'
    }
};

async function fetchTranslation(text, targetLang) {
    if (targetLang === 'en') return text;
    
    // Check local dictionary first
    if (UI_TRANSLATIONS[targetLang] && UI_TRANSLATIONS[targetLang][text]) {
        return UI_TRANSLATIONS[targetLang][text];
    }

    try {
        const response = await fetch(`${API_URL}/translate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, target_lang: targetLang })
        });
        const data = await response.json();
        return data.translated_text || text;
    } catch (e) {
        console.error('Translation error:', e);
        return UI_TRANSLATIONS[targetLang] ? UI_TRANSLATIONS[targetLang][text] || text : text;
    }
}

async function translateUI(targetLang) {
    const elements = document.querySelectorAll('[data-i18n]');
    const promises = Array.from(elements).map(async (el) => {
        const originalText = el.getAttribute('data-i18n');
        const translatedText = await fetchTranslation(originalText, targetLang);
        if (el.tagName === 'INPUT') {
            el.placeholder = translatedText;
        } else {
            el.innerHTML = translatedText;
        }
    });

    // Special handling for chat input placeholder
    const placeholderText = await fetchTranslation("Type your question here...", targetLang);
    chatInput.placeholder = placeholderText;

    await Promise.all(promises);
}

async function sendMessage(text) {
    if (!text.trim()) return;

    addMessageToUI('user', text);
    chatInput.value = '';

    // Add "Thinking..." indicator
    const thinkingMsgId = 'thinking-' + Date.now();
    const thinkingDiv = document.createElement('div');
    thinkingDiv.className = 'message bot thinking';
    thinkingDiv.id = thinkingMsgId;
    thinkingDiv.innerHTML = '<em>Thinking...</em>';
    chatMessages.appendChild(thinkingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
        console.log(`📡 Sending request to ${API_URL}/chat...`);
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: sessionId,
                message: text,
                target_lang: currentLang
            })
        });

        // Remove "Thinking..." indicator
        const thinkingEl = document.getElementById(thinkingMsgId);
        if (thinkingEl) thinkingEl.remove();

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Server responded with ${response.status}: ${errorText}`);
        }

        const data = await response.json();
        
        if (data.error) {
            addMessageToUI('bot', `❌ Error: ${data.error}`);
            return;
        }

        sessionId = data.session_id;
        updateUI(data);

    } catch (error) {
        // Remove "Thinking..." indicator on error too
        const thinkingEl = document.getElementById(thinkingMsgId);
        if (thinkingEl) thinkingEl.remove();

        console.error('Fetch error:', error);
        addMessageToUI('bot', `❌ Connection Error: ${error.message}. Please check if the server is awake.`);
    }
}

function addMessageToUI(sender, text, emotion = null) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}`;
    
    let content = text;
    if (sender === 'bot' && emotion) {
        const emojiMap = {
            'confident': '✨',
            'hesitant': '🤔',
            'uncertain': '❓',
            'neutral': '💬',
            'frustrated': '😤'
        };
        const emoji = emojiMap[emotion] || '';
        content += `<br><span class="emotion-tag emotion-${emotion}">${emoji} ${emotion}</span>`;
    }
    
    msgDiv.innerHTML = content;
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function updateUI(data) {
    addMessageToUI('bot', data.response, data.emotion);
    detectedLangTag.textContent = data.detected_language;
    updateProfile(data.student_profile);
}

function updateProfile(profile) {
    if (!profile || Object.keys(profile).length === 0) return;
    
    const labels = {
        grade: '🎓 Grade',
        degree: '🎓 Degree',
        stream: '📚 Stream',
        location: '📍 Location',
        gender: '⚧ Gender',
        category: '🏷️ Category',
        family_income: '💰 Income',
        interests: '❤️ Interests',
        constraints: '⚠️ Constraints'
    };

    let html = '';
    for (const [key, label] of Object.entries(labels)) {
        const value = profile[key];
        if (value && (Array.isArray(value) ? value.length > 0 : true)) {
            const displayValue = Array.isArray(value) ? value.join(', ') : value;
            html += `
                <div class="profile-item">
                    <span>${label}</span>
                    ${displayValue}
                </div>
            `;
        }
    }

    if (html) {
        profileContainer.innerHTML = html;
    } else {
        profileContainer.innerHTML = `<p style="font-size: 0.85rem; color: var(--text-muted); text-align: center; margin-top: 2rem;" data-i18n="Chat with me to build your profile!">Chat with me to build your profile!</p>`;
    }
}

// Event Listeners
sendBtn.addEventListener('click', () => sendMessage(chatInput.value));
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage(chatInput.value);
});

langSelect.addEventListener('change', async (e) => {
    const selectedLang = e.target.value;
    console.log('🌐 Language changed to:', selectedLang);
    currentLang = selectedLang;
    document.body.style.opacity = '0.7';
    try {
        await translateUI(currentLang);
        console.log('✅ UI Translation completed for:', currentLang);
    } catch (err) {
        console.error('❌ UI Translation failed:', err);
    }
    document.body.style.opacity = '1';
});

quickBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const query = btn.getAttribute('data-query');
        if (query) sendMessage(query);
    });
});

clearChatBtn.addEventListener('click', async () => {
    if (sessionId) {
        try {
            await fetch(`${API_URL}/session/${sessionId}`, { method: 'DELETE' });
        } catch (e) {}
    }
    sessionId = null;
    chatMessages.innerHTML = '';
    const resetMsg = await fetchTranslation("History cleared. How can I help you today?", currentLang);
    addMessageToUI('bot', resetMsg);
    profileContainer.innerHTML = `<p style="font-size: 0.85rem; color: var(--text-muted); text-align: center; margin-top: 2rem;" data-i18n="Chat with me to build your profile!">Chat with me to build your profile!</p>`;
});
