# Voice pipeline verification

**Status:** Consent guard and audio cleanup are implemented. Physical microphone → transcription → response → playback has **not** been executed in this environment; do not describe the complete voice workflow as verified yet.

## Implemented controls

- `frontend/components/sticky_chat/frontend/src/App.jsx` requires an explicit unchecked-by-default consent checkbox before requesting browser microphone access. The notice describes transcription, chat transcript persistence, optional online TTS, and temporary audio cleanup.
- Browser microphone tracks are stopped on completion, denial, component unmount, and stop action. Recording chunks are cleared after packaging; empty recordings are rejected.
- If consent is withdrawn during recording, the recording is discarded (not uploaded) and the browser tracks are stopped.
- The component includes a consent flag. `frontend/ui/chat.py` rejects audio payloads without `consent: true` before processing.
- Temporary WebM/WAV files are removed in a `finally` block whether transcription succeeds or raises. Transcripts are saved through the existing chat message path.
- Assistant speech is generated only for voice-initiated turns and rendered with the existing audio player, requiring user playback interaction. Text-only chat does not trigger TTS.
- Development logging of transcript text was removed. Voice exceptions shown in the UI do not echo exception details that may contain sensitive content.

## Manual end-to-end acceptance run (required on target device)

Record date, OS/browser, app commit, model/runtime versions, and pass/fail for each item. Do not enter sensitive real-user data.

| Check | Expected result | Result/date |
|---|---|---|
| Open chat without opting into voice | Mic unavailable; text chat still works | Pending |
| Click mic without consent (including crafted component event) | No recording/transcription; consent error or server rejection | Pending |
| Accept disclosure and deny browser mic permission | Helpful error; no audio payload; app remains usable | Pending |
| Record a short harmless phrase and stop | Browser permission prompt appears; one audio payload is sent only after stop; track stops | Pending |
| Transcription succeeds | Transcript appears as user chat message and is sent through ordinary backend chat path | Pending |
| Generation succeeds | Assistant text response appears; only this voice turn requests speech output | Pending |
| Play response | Audio player contains generated response audio; playback works after user action | Pending |
| Transcription/conversion fails | Generic error; no transcript stored; temporary upload files are removed | Pending |
| Uncheck consent during recording / navigate away | Recording is stopped and browser microphone tracks are released | Pending |
| Inspect logs and temp directory after run | No transcript in app debug logs; no leftover WebM/WAV temporary files | Pending |
| Text-only message | No microphone request and no generated speech audio | Pending |

## Limitations and privacy

Whisper runs in the application process; chat text is persisted like other messages. Response speech synthesis uses Edge TTS with gTTS fallback, which are online services; provider-side retention and data processing were not verified. Transcript/audio deletion guarantees across session state, operating-system temp storage, backups, and third-party services have not been demonstrated. The consent checkbox is a user-facing product control, not legal consent advice or a substitute for a complete privacy policy. Keep voice labeled **experimental / not end-to-end verified** until the acceptance table is completed on a real device.
