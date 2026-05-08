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
    Streamlit.setFrameHeight(80);
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

  return (
    <div className="sticky-bar">
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Share what's on your mind..."
      />
      
      <button
        className={`mic-btn ${isRecording ? 'recording' : ''}`}
        onClick={isRecording ? stopRecording : startRecording}
        title={isRecording ? "Stop Recording" : "Start Recording"}
      >
        {isRecording ? "⏹️" : "🎤"}
      </button>
      
      <button
        className="send-btn"
        onClick={sendText}
        title="Send Message"
      >
        ➤
      </button>
    </div>
  );
}

export default withStreamlitConnection(App);
