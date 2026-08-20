# Voice AI Documentation — PARTH ASSISTANT AI (Phase 4)

## Architecture Pipeline

```
User Speaks
    │
    ▼
[Browser Web Speech API] ──► STT Transcription in selected BCP-47 locale (e.g. hi-IN)
    │
    ▼
[POST /api/ai/voice] ──► JWT Authenticated, Rate Limited voice endpoint
    │
    ▼
[VoiceService] ──► STT Normalization → SupervisorAgent → TTS Synthesis
    │
    ▼
[SupervisorAgent] ──► SAME FULL PIPELINE as /api/ai/chat
    │     ├── Safety & Security Guard
    │     ├── ML Intent Classification
    │     ├── Entity Extraction
    │     ├── Context Memory Resolution
    │     ├── RBAC Authorization
    │     └── ERP Tool Execution
    │
    ▼
[TTS Response] ──► BrowserTTSProvider → window.speechSynthesis plays response
```

---

## Voice States

| State | Description |
| :--- | :--- |
| `IDLE` | Ready to listen |
| `LISTENING` | 🔴 Web Speech API actively capturing speech |
| `PROCESSING` | ⏳ Transcript sent to AI brain pipeline |
| `SPEAKING` | 🔊 TTS playing AI response |
| `ERROR` | ⚠️ Graceful error shown, text input fallback available |

---

## Push-to-Talk Interaction

1. User taps microphone button.
2. Browser requests microphone permission (first use).
3. User speaks in selected language.
4. Speech detected → transcript generated.
5. Transcript submitted to `POST /api/ai/voice`.
6. AI response returned → displayed in chat bubble.
7. TTS speaks response aloud via `window.speechSynthesis`.
8. User can stop speech at any time with **Stop** button.
9. User can replay last response with **Replay** button.

---

## Hybrid Text + Voice Mode

Text and voice messages share the same `conversation_id`, preserving multi-turn context:

```
Voice: "How much attendance does Rahul have?"
AI: "Rahul currently has 91.2% attendance."
Text: "What about last month?"
AI: Uses prior context → VIEW_RECENT_ATTENDANCE
```

---

## Multilingual Voice Support

| Language | BCP-47 Locale (STT/TTS) |
| :--- | :--- |
| English | `en-IN` |
| Hindi | `hi-IN` |
| Tamil | `ta-IN` |
| Telugu | `te-IN` |
| Marathi | `mr-IN` |
| Bengali | `bn-IN` |
| Gujarati | `gu-IN` |
| Punjabi | `pa-IN` |
| Kannada | `kn-IN` |
| Malayalam | `ml-IN` |
| Urdu | `ur-IN` |

---

## Privacy Policy

- Raw audio is never stored to disk or database.
- Browser Web Speech API processes audio locally; only the text transcript is sent to the backend.
- Audit logs record `transcript`, `user_id`, `intent`, and `latency` — never raw audio.
- Temporary audio buffers are discarded by the browser after transcription.

---

## Provider Abstraction

STT and TTS are provider-abstracted. To replace Web Speech API with a server-side provider:

1. Create a new class implementing `SpeechToTextProvider` (from `voice/stt/base.py`).
2. Swap `stt_provider` in `voice/voice_service.py`.
3. Update `STT_PROVIDER` and `STT_API_KEY` in `.env`.

---

## Actual Latency Metrics (Example)

```json
{
  "stt_ms": 0.1,
  "ai_ms": 45.2,
  "api_ms": 38.7,
  "tts_ms": 0.05,
  "total_ms": 47.3
}
```

*Note: Browser STT/TTS latency is handled client-side and not measured server-side. Server metrics reflect normalization and AI pipeline time only.*

---

## Error Handling

| Error Condition | Behavior |
| :--- | :--- |
| Microphone permission denied | Alert shown, text input still works |
| No speech detected | "No speech was detected. Please try again." |
| Browser STT unavailable | "Voice input is not supported in this browser. Please use text input." |
| Network failure | Error bubble in chat, no crash |
| TTS unavailable | Response text displayed in chat, no crash |
| Empty transcript | HTTP 400 with clear message |
