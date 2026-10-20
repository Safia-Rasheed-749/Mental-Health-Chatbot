import React, { useState, useRef, useEffect } from "react";
import {
  Streamlit,
  withStreamlitConnection,
} from "streamlit-component-lib";

function App() {
  const [text, setText] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [voiceConsent, setVoiceConsent] = useState(false);
  const [voiceError, setVoiceError] = useState("");
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const streamRef = useRef(null);
  const recordingTimerRef = useRef(null);
  const discardRecordingRef = useRef(false);
  const isUrduInput = /[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]/.test(text);

  useEffect(() => {
    Streamlit.setFrameHeight(104);
    return () => {
      if (recordingTimerRef.current) clearTimeout(recordingTimerRef.current);
      if (mediaRecorderRef.current?.state === "recording") {
        discardRecordingRef.current = true;
        mediaRecorderRef.current.stop();
      }
      streamRef.current?.getTracks().forEach((track) => track.stop());
    };
  }, []);

  // SEND TEXT
  const sendText = () => {
    if (!text.trim()) return;
    
    // Send the value
    Streamlit.setComponentValue({
      type: "text",
      data: text,
    });
    
    // Clear input immediately
    setText("");
  };

  // Handle Enter key
  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendText();
    }
  };

  // RECORD AUDIO
  const startRecording = async () => {
    if (!voiceConsent) {
      setVoiceError("Please review and accept the voice-processing notice before recording.");
      return;
    }
    try {
      setVoiceError("");
      if (!navigator.mediaDevices?.getUserMedia || typeof MediaRecorder === "undefined") {
        throw new Error("Voice recording is not supported by this browser.");
      }
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
      });
      streamRef.current = stream;
      
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];
      
      mediaRecorder.ondataavailable = (e) => {
        chunksRef.current.push(e.data);
      };
      
      mediaRecorder.onstop = async () => {
        if (recordingTimerRef.current) clearTimeout(recordingTimerRef.current);
        const blob = new Blob(chunksRef.current, {
          type: mediaRecorder.mimeType || "audio/webm",
        });
        chunksRef.current = [];
        try {
          if (discardRecordingRef.current) return;
          if (!blob.size) throw new Error("No audio was recorded. Please try again.");
          const arrayBuffer = await blob.arrayBuffer();
          const uint8Array = Array.from(new Uint8Array(arrayBuffer));
          Streamlit.setComponentValue({
            type: "audio",
            data: uint8Array,
            mime_type: blob.type,
            consent: true,
          });
        } catch (err) {
          setVoiceError(err.message || "Could not prepare this recording.");
        } finally {
          discardRecordingRef.current = false;
          stream.getTracks().forEach(track => track.stop());
          streamRef.current = null;
          setIsRecording(false);
        }
      };
      
      mediaRecorder.start();
      setIsRecording(true);
      
      // Auto-stop after 5 seconds
      recordingTimerRef.current = setTimeout(() => {
        if (mediaRecorder.state === "recording") {
          mediaRecorder.stop();
        }
      }, 5000);
    } catch (err) {
      console.error("Mic error:", err);
      streamRef.current?.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
      setIsRecording(false);
      setVoiceError(err.message || "Microphone access was denied.");
    }
  };

  const stopRecording = () => {
    if (recordingTimerRef.current) clearTimeout(recordingTimerRef.current);
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === "recording") {
      mediaRecorderRef.current.stop();
    }
  };
  /*To change this placeholder text, firstly run npm build in   components\sticky_chat/frontend*/
  return (
    <div className="sticky-bar">
      <input
        type="text"
        value={text}
        dir={isUrduInput ? "rtl" : "ltr"}
        className={isUrduInput ? "urdu-input" : "ltr-input"}
        onChange={(e) => setText(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Share what is on your mind..."
        aria-label="Message MindCare AI"
      />
      
      <label className="voice-consent" title="Microphone audio is sent to this app for local Whisper transcription; the transcript is sent as chat text and saved with chat history. Optional spoken replies use an online speech provider. Temporary audio files are deleted after processing.">
        <input
          type="checkbox"
          checked={voiceConsent}
          onChange={(event) => {
            setVoiceConsent(event.target.checked);
            setVoiceError("");
            if (!event.target.checked && mediaRecorderRef.current?.state === "recording") {
              discardRecordingRef.current = true;
              stopRecording();
            }
          }}
          aria-label="I consent to voice processing"
        />
        <span>I consent to voice processing (audio transcription; transcript saved as chat; optional reply audio uses online speech services).</span>
      </label>
      <button
        className={`mic-btn ${isRecording ? 'recording' : ''}`}
        onClick={isRecording ? stopRecording : startRecording}
        disabled={!voiceConsent && !isRecording}
        title={isRecording ? "Stop Recording" : "Start Recording"}
        aria-label={isRecording ? "Stop recording" : "Start voice recording"}
      >
        {isRecording ? (
          <svg viewBox="0 0 24 24" aria-hidden="true"><rect x="8" y="8" width="8" height="8" rx="1.5" /></svg>
        ) : (
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 14.5a3.5 3.5 0 0 0 3.5-3.5V7a3.5 3.5 0 0 0-7 0v4a3.5 3.5 0 0 0 3.5 3.5Z" /><path d="M5 11a7 7 0 0 0 14 0M12 18v3M9 21h6" /></svg>
        )}
      </button>
      
      <button
        className="send-btn"
        onClick={sendText}
        title="Send Message"
      >
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="m21 3-7.4 18-3.8-7.8L2 9.4 21 3Z" /><path d="M10 13 21 3" /></svg>
      </button>
      {voiceError && <span className="voice-error" role="alert">{voiceError}</span>}
    </div>
  );
}

export default withStreamlitConnection(App);
