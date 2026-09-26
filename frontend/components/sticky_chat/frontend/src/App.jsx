import React, { useState, useRef, useEffect } from "react";
import {
  Streamlit,
  withStreamlitConnection,
} from "streamlit-component-lib";

function App() {
  const [text, setText] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  useEffect(() => {
    Streamlit.setFrameHeight(82);
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
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
      });
      
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];
      
      mediaRecorder.ondataavailable = (e) => {
        chunksRef.current.push(e.data);
      };
      
      mediaRecorder.onstop = async () => {
        const blob = new Blob(chunksRef.current, {
          type: "audio/webm",
        });
        const arrayBuffer = await blob.arrayBuffer();
        const uint8Array = Array.from(new Uint8Array(arrayBuffer));
        
        // Send the value
        Streamlit.setComponentValue({
          type: "audio",
          data: uint8Array,
        });
        
        // Stop all tracks
        stream.getTracks().forEach(track => track.stop());
        setIsRecording(false);
      };
      
      mediaRecorder.start();
      setIsRecording(true);
      
      // Auto-stop after 5 seconds
      setTimeout(() => {
        if (mediaRecorder.state === "recording") {
          mediaRecorder.stop();
        }
      }, 5000);
    } catch (err) {
      console.error("Mic error:", err);
      alert("Microphone access denied");
    }
  };

  const stopRecording = () => {
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
        onChange={(e) => setText(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Share what is on your mind..."
        aria-label="Message MindCare AI"
      />
      
      <button
        className={`mic-btn ${isRecording ? 'recording' : ''}`}
        onClick={isRecording ? stopRecording : startRecording}
        title={isRecording ? "Stop Recording" : "Start Recording"}
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
    </div>
  );
}

export default withStreamlitConnection(App);
