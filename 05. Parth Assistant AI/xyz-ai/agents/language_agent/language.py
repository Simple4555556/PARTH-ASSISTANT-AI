"""
Language Agent — Multilingual processing across 11 Indian Languages + Hinglish
"""

from typing import Dict, Any, Optional

SUPPORTED_LANGUAGES = {
    "en": {"name": "English", "script": "Latin"},
    "hi": {"name": "Hindi", "script": "Devanagari"},
    "ta": {"name": "Tamil", "script": "Tamil"},
    "te": {"name": "Telugu", "script": "Telugu"},
    "mr": {"name": "Marathi", "script": "Devanagari"},
    "bn": {"name": "Bengali", "script": "Bengali"},
    "gu": {"name": "Gujarati", "script": "Gujarati"},
    "pa": {"name": "Punjabi", "script": "Gurmukhi"},
    "kn": {"name": "Kannada", "script": "Kannada"},
    "ml": {"name": "Malayalam", "script": "Malayalam"},
    "ur": {"name": "Urdu", "script": "Perso-Arabic"}
}


class LanguageAgent:
    def detect_language_details(self, text: str, user_preference: Optional[str] = None) -> Dict[str, Any]:
        """Detects language script/keywords and returns detailed language metadata."""
        if user_preference and user_preference in SUPPORTED_LANGUAGES and user_preference != "en":
            meta = SUPPORTED_LANGUAGES[user_preference]
            return {
                "language": user_preference,
                "language_name": meta["name"],
                "confidence": 1.0,
                "script": meta["script"]
            }

        # Script-based detection from input text
        for char in text:
            code = ord(char)
            if 0x0900 <= code <= 0x097F:
                return {"language": "hi", "language_name": "Hindi", "confidence": 0.98, "script": "Devanagari"}
            if 0x0B80 <= code <= 0x0BFF:
                return {"language": "ta", "language_name": "Tamil", "confidence": 0.98, "script": "Tamil"}
            if 0x0C00 <= code <= 0x0C7F:
                return {"language": "te", "language_name": "Telugu", "confidence": 0.98, "script": "Telugu"}
            if 0x0980 <= code <= 0x09FF:
                return {"language": "bn", "language_name": "Bengali", "confidence": 0.98, "script": "Bengali"}
            if 0x0A80 <= code <= 0x0AFF:
                return {"language": "gu", "language_name": "Gujarati", "confidence": 0.98, "script": "Gujarati"}
            if 0x0A00 <= code <= 0x0A7F:
                return {"language": "pa", "language_name": "Punjabi", "confidence": 0.98, "script": "Gurmukhi"}
            if 0x0C80 <= code <= 0x0CFF:
                return {"language": "kn", "language_name": "Kannada", "confidence": 0.98, "script": "Kannada"}
            if 0x0D00 <= code <= 0x0D7F:
                return {"language": "ml", "language_name": "Malayalam", "confidence": 0.98, "script": "Malayalam"}
            if 0x0600 <= code <= 0x06FF:
                return {"language": "ur", "language_name": "Urdu", "confidence": 0.98, "script": "Perso-Arabic"}

        # Check Hinglish keywords
        text_lower = text.lower()
        if any(w in text_lower for w in ["karo", "batao", "dekhni", "hai", "bhej", "ki", "kitni", "kaun"]):
            return {"language": "hi", "language_name": "Hindi", "confidence": 0.90, "script": "Latin/Hinglish"}

        lang = user_preference if user_preference in SUPPORTED_LANGUAGES else "en"
        meta = SUPPORTED_LANGUAGES[lang]
        return {
            "language": lang,
            "language_name": meta["name"],
            "confidence": 0.95,
            "script": meta["script"]
        }

    def detect_language(self, text: str, user_preference: Optional[str] = None) -> str:
        return self.detect_language_details(text, user_preference)["language"]

    def translate_response(self, text: str, lang: str, persona: Dict[str, Any], intent: str) -> str:
        if lang == "en":
            return text

        # Multilingual templates across all 11 supported languages
        if intent == "VIEW_OWN_ATTENDANCE":
            translations = {
                "hi": "आपकी वर्तमान attendance 87.5% है।",
                "ta": "உங்கள் தற்போதைய attendance 87.5% ஆகும்.",
                "te": "మీ ప్రస్తుత attendance 87.5% ఉంది.",
                "mr": "तुमची सध्याची attendance 87.5% आहे.",
                "bn": "আপনার বর্তমান attendance 87.5%।",
                "gu": "તમારી વર્તમાન attendance 87.5% છે.",
                "pa": "ਤੁਹਾਡੀ ਮੌਜੂਦਾ attendance 87.5% ਹੈ।",
                "kn": "ನಿಮ್ಮ ಪ್ರಸ್ತುತ attendance 87.5% ಇದೆ.",
                "ml": "നിങ്ങളുടെ നിലവിലെ attendance 87.5% ആണ്.",
                "ur": "آپ کی موجودہ حاضری 87.5 فیصد ہے۔"
            }
            return translations.get(lang, text)

        if intent == "VIEW_CHILD_ATTENDANCE":
            translations = {
                "hi": "राहुल की वर्तमान attendance 91.2% है।",
                "ta": "ராகுலின் தற்போதைய attendance 91.2% ஆகும்.",
                "te": "రాహుల్ యొక్క ప్రస్తుత attendance 91.2% ఉంది.",
                "mr": "राहुलची सध्याची attendance 91.2% आहे.",
                "bn": "রাহুলের বর্তমান attendance ৯১.২%।",
                "gu": "રાહુલની વર્તમાન attendance 91.2% છે.",
                "pa": "ਰਾਹੁਲ ਦੀ ਮੌਜੂਦਾ attendance 91.2% ਹੈ।",
                "kn": "ರಾಹುಲ್ ಅವರ ಪ್ರಸ್ತುತ attendance 91.2% ಆಗಿದೆ.",
                "ml": "രാഹുലിന്റെ നിലവിലെ attendance 91.2% ആണ്.",
                "ur": "راہول کی موجودہ حاضری 91.2 فیصد ہے۔"
            }
            return translations.get(lang, text)

        if intent == "MARK_ATTENDANCE":
            translations = {
                "hi": "राहुल को आज अनुपस्थित दर्ज कर दिया गया है।",
                "ta": "ராகுல் இன்று வருகை பெறவில்லை எனப் பதிவு செய்யப்பட்டுள்ளது.",
                "te": "రాహుల్ ఈరోజు గైర్హాజరైనట్లు నమోదు చేయబడింది.",
                "mr": "राहुलला आज गैरहजर नोंदवले गेले आहे.",
                "bn": "রাহুলকে আজ অনুপস্থিত হিসেবে চিহ্নিত করা হয়েছে।",
                "gu": "રાહુલને આજે ગેરહાજર નોંધવામાં આવ્યો છે.",
                "pa": "ਰਾਹੁਲ ਨੂੰ ਅੱਜ ਗ਼ੈਰ-ਹਾਜ਼ਰ ਦਰਜ ਕੀਤਾ ਗਿਆ ਹੈ।",
                "kn": "ರಾಹುಲ್ ಅವರನ್ನು ಇಂದು ಗೈರುಹಾಜರೆಂದು ದಾಖಲಿಸಲಾಗಿದೆ.",
                "ml": "രാഹുലിനെ ഇന്ന് ഗൈർഹാജരായി രേഖപ്പെടുത്തി.",
                "ur": "راہول کو آج غیر حاضر درج کر دیا گیا ہے۔"
            }
            return translations.get(lang, text)

        if intent == "VIEW_SCHOOL_ANALYTICS":
            translations = {
                "hi": "इस महीने विद्यालय की कुल उपस्थिति 92.4% है।",
                "ta": "இந்த மாதத்தில் பள்ளியின் மொத்த வருகை 92.4% ஆகும்.",
                "te": "ఈ నెలలో పాఠశాల మొత్తం హాజరు 92.4%గా ఉంది.",
                "mr": "या महिन्यात शाळेची एकूण उपस्थिती 92.4% आहे.",
                "bn": "এই মাসে বিদ্যালয়ের মোট উপস্থিতি ৯২.৪%।",
                "gu": "આ મહિને શાળાની કુલ હાજરી 92.4% છે.",
                "pa": "ਇਸ ਮਹੀਨੇ ਸਕੂਲ ਦੀ ਕੁੱਲ ਹਾਜ਼ਰੀ 92.4% ਹੈ।",
                "kn": "ಈ ತಿಂಗಳು ಶಾಲೆಯ ಒಟ್ಟು ಹಾಜರಾತಿ 92.4% ಆಗಿದೆ.",
                "ml": "ഈ മാസത്തെ സ്‌കൂളിന്റെ മൊത്തം ഹാജർ 92.4% ആണ്.",
                "ur": "اس مہینے اسکول کی کل حاضری 92.4 فیصد ہے۔"
            }
            return translations.get(lang, text)

        if intent in ["DATABASE_ACCESS", "VIEW_DATABASE"]:
            if "sorry" in text.lower() or "don't have permission" in text.lower() or "permission" in text.lower():
                translations = {
                    "hi": "मुझे खेद है, आपको डेटाबेस देखने की अनुमति नहीं है।",
                    "ta": "மன்னிக்கவும், உங்களுக்கு தரவுத்தளத்தை அணுக அனுமதி இல்லை.",
                    "te": "క్షమించండి, మీకు డేటాబేస్ ప్రాప్యత అనుమతి లేదు.",
                    "mr": "माफ करा, तुम्हाला डेटाबेस पाहण्याची परवानगी नाही.",
                    "bn": "দুঃখিত, আপনার ডেটাবেস অ্যাক্সেস করার অনুমতি নেই।",
                    "gu": "દિલગીર છું, તમને ડેટાબેઝ ઍક્સેસ કરવાની પરવાનગી નથી.",
                    "pa": "ਮੁਆਫ਼ ਕਰਨਾ, ਤੁਹਾਡੇ ਕੋਲ ਡੇਟਾਬੇਸ ਤੱਕ ਪਹੁੰਚ ਦੀ ਇਜਾਜ਼ਤ ਨਹੀਂ ਹੈ।",
                    "kn": "ಕ್ಷಮಿಸಿ, ನಿಮಗೆ ಡೇಟಾಬೇಸ್ ವೀಕ್ಷಿಸಲು ಅನುಮತಿಯಿಲ್ಲ.",
                    "ml": "ക്ഷമിക്കണം, നിങ്ങൾക്ക് ഡാറ്റാബേസ് ആക്സസ് ചെയ്യാൻ അനുമതിയില്ല.",
                    "ur": "معذرت، آپ کو ڈیٹا بیس تک رسائی کی اجازت نہیں ہے۔"
                }
                return translations.get(lang, text)
            else:
                translations = {
                    "hi": "विद्यालय डेटाबेस ओवरव्यू खोला जा रहा है।",
                    "ta": "பள்ளி தரவுத்தளப் பக்கம் திறக்கப்படுகிறது.",
                    "te": "పాఠశాల డేటాబేస్ తెరువబడుతోంది.",
                    "mr": "शाळेचे डेटाबेस उघडले जात आहे.",
                    "bn": "বিদ্যালয়ের ডেটাবেস খোলা হচ্ছে।",
                    "gu": "શાળાનું ડેટાબેઝ ખોલવામાં આવી રહ્યું છે.",
                    "pa": "ਸਕੂਲ ਦਾ ਡੇਟਾਬੇਸ ਖੋਲ੍ਹਿਆ ਜਾ ਰਿਹਾ ਹੈ।",
                    "kn": "ಶಾಲೆಯ ಡೇಟಾಬೇಸ್ ತೆರೆಯಲಾಗುತ್ತಿದೆ.",
                    "ml": "സ്‌കൂൾ ഡാറ്റാബേസ് തുറക്കുന്നു.",
                    "ur": "اسکول کا ڈیٹا بیس کھولا جا رہا ہے۔"
                }
                return translations.get(lang, text)

        if intent in ["PROMPT_INJECTION", "SECURITY_DENIED"]:
            translations = {
                "hi": "सुरक्षा कारणों से यह अनुरोध स्वीकार नहीं किया जा सकता।",
                "ta": "பாதுகாப்பு காரணங்களால் இந்த கோரிக்கை நிராகரிக்கப்பட்டது.",
                "te": "భద్రతా కారణాల వల్ల ఈ అభ్యర్థన నిరాకరించబడింది.",
                "mr": "सुरक्षेच्या कारणास्तव ही विनंती नाकारण्यात आली आहे.",
                "bn": "সুরক্ষাজনিত কারণে এই অনুরোধটি প্রত্যাখ্যান করা হয়েছে।",
                "gu": "સુરક્ષા કારણોસર આ વિનંતી અસ્વીકાર કરવામાં આવી છે.",
                "pa": "ਸੁਰੱਖਿਆ ਕਾਰਨਾਂ ਕਰਕੇ ਇਹ ਬੇਨਤੀ ਰੱਦ ਕੀਤੀ ਗਈ ਹੈ।",
                "kn": "ಸುರಕ್ಷತಾ ಕಾರಣಗಳಿಂದ ಈ ವಿನಂತಿಯನ್ನು ತಿರಸ್ಕರಿಸಲಾಗಿದೆ.",
                "ml": "സുരക്ഷാ കാരണങ്ങളാൽ ഈ അഭ്യർത്ഥന നിരസിച്ചു.",
                "ur": "سیکیورٹی وجوہات کی بناء پر یہ درخواست مسترد کر دی گئی ہے۔"
            }
            return translations.get(lang, text)

        # Fallback formatting for general messages
        if lang == "hi" and "sorry" in text.lower():
            return "मुझे खेद है, आप केवल अपने खाते से जुड़ी जानकारी ही देख सकते हैं।"
        if lang == "ta" and "sorry" in text.lower():
            return "மன்னிக்கவும், உங்கள் கணக்கு தொடர்பான தகவல்களை மட்டுமே நீங்கள் அணுக முடியும்."
        if lang == "te" and "sorry" in text.lower():
            return "క్షమించండి, మీరు మీ ఖాతాకు సంబంధించిన సమాచారాన్ని మాత్రమే ప్రాప్యత చేయగలరు."
        if lang == "ur" and "sorry" in text.lower():
            return "معذرت، آپ صرف اپنے اکاؤنٹ سے متعلق معلومات تک رسائی حاصل کر سکتے ہیں۔"

        return text


language_agent = LanguageAgent()
