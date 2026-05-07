# Chat Integration Guide - React Component

## After Building React Component

Once you've run `npm run build` successfully, follow these steps:

## Step 1: Update chat.py

Replace the current input section with the React component:

### Remove These Lines:
```python
# Remove mic_recorder import
from streamlit_mic_recorder import mic_recorder

# Remove these lines from show_chat():
audio = mic_recorder(...)
user_input = st.chat_input(...)
```

### Add These Lines:
```python
# At top of file, add:
from components.sticky_chat import sticky_chat_bar

# In show_chat(), replace input section with:
user_input = sticky_chat_bar(key=f"chat_input_{cid if cid else 'new'}")
```

## Step 2: Handle Component Output

The component returns data in this format:

```python
{
    "type": "text",      # or "audio"
    "data": "message"    # or [audio bytes array]
}
```

### Update Message Handling:

```python
# Replace current text input handling with:
if user_input:
    # Create conversation on first message
    if not cid:
        cid = create_conversation(user_id)
        st.session_state["conversation_id"] = cid
        st.session_state["last_loaded_chat"] = cid
    
    # Handle TEXT message
    if user_input["type"] == "text":
        text = user_input["data"]
        
        st.session_state["chat_history"].append(("user", text))
        add_message(user_id, "user", text, cid)
        
        # Log activity
        try:
            log_user_activity(user_id, "Send Message", "Chat", f"Message: {text[:50]}...")
        except Exception as e:
            print(f"Activity logging error: {e}")

        # Get response from AI
        response = generate_response(text, st.session_state["chat_history"][-5:])
        
        # Save to session and database
        st.session_state["chat_history"].append(("assistant", response))
        add_message(user_id, "assistant", response, cid)
        
        st.rerun()
    
    # Handle AUDIO message
    elif user_input["type"] == "audio":
        audio_bytes = bytes(user_input["data"])
        
        # Use existing voice processing code
        recognizer = sr.Recognizer()
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
                tmp.write(audio_bytes)
                webm_path = tmp.name
            
            wav_path = webm_path.replace(".webm", ".wav")
            audio_segment = AudioSegment.from_file(webm_path, format="webm")
            audio_segment.export(wav_path, format="wav")
            
            with sr.AudioFile(wav_path) as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio_data = recognizer.record(source)
                voice_text = recognizer.recognize_google(audio_data)
            
            if voice_text.strip():
                # Add user message
                st.session_state["chat_history"].append(("user", voice_text))
                add_message(user_id, "user", voice_text, cid)
                
                # Generate response
                response = generate_response(voice_text, st.session_state["chat_history"][-5:])
                
                # Add assistant response
                st.session_state["chat_history"].append(("assistant", response))
                add_message(user_id, "assistant", response, cid)
                
                # Speak with auto-play
                speak_and_auto_play(response)
                
                # Cleanup
                try:
                    os.unlink(webm_path)
                    os.unlink(wav_path)
                except:
                    pass
                
                st.rerun()
                
        except sr.UnknownValueError:
            st.warning("Sorry, I couldn't understand that. Please speak clearly.")
        except Exception as e:
            st.error(f"Voice error: {str(e)}")
```

## Step 3: Remove Old CSS

Remove these CSS sections from chat.py:

```python
# Remove:
# - [data-testid="stChatInput"] styles
# - div[data-testid="stCustomComponentV1"] styles (mic button)
# - .chat-input-container styles
```

The React component has its own styling built-in!

## Step 4: Update Layout

The component is self-contained and handles:
- Sticky positioning
- Mic button inline
- Enter key functionality
- Responsive design

Just place it where you want the input to appear:

```python
# At the end of show_chat(), after messages:
st.markdown('</div>', unsafe_allow_html=True)  # Close chat-area

# Add the component
user_input = sticky_chat_bar(key=f"chat_input_{cid if cid else 'new'}")
```

## Complete Updated chat.py Structure

```python
def show_chat(user_id):
    apply_clean_layout(hide_header_completely=False)
    
    # CSS (remove input-related styles)
    st.markdown("""<style>...</style>""", unsafe_allow_html=True)
    
    # Header
    st.markdown("""<div class="chat-header">...</div>""", unsafe_allow_html=True)
    
    # Load conversation
    cid = st.session_state.get("conversation_id")
    if cid and st.session_state["last_loaded_chat"] != cid:
        st.session_state["chat_history"] = get_messages_by_conversation(cid)
        st.session_state["last_loaded_chat"] = cid
    
    # Messages area
    st.markdown('<div class="chat-area" id="chat-messages">', unsafe_allow_html=True)
    
    if not st.session_state["chat_history"]:
        # Empty state
        st.markdown("""<div class="empty-state">...</div>""", unsafe_allow_html=True)
    else:
        # Display messages
        for role, msg in st.session_state["chat_history"]:
            # ... message bubbles ...
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Auto-scroll script
    st.markdown("""<script>...</script>""", unsafe_allow_html=True)
    
    # ===== REACT COMPONENT =====
    user_input = sticky_chat_bar(key=f"chat_input_{cid if cid else 'new'}")
    
    # ===== HANDLE INPUT =====
    if user_input:
        if not cid:
            cid = create_conversation(user_id)
            st.session_state["conversation_id"] = cid
            st.session_state["last_loaded_chat"] = cid
        
        if user_input["type"] == "text":
            # Handle text (see above)
            pass
        elif user_input["type"] == "audio":
            # Handle audio (see above)
            pass
```

## Benefits of React Component

✅ **No Streamlit limitations** - Full control over UI
✅ **Better performance** - No iframe issues
✅ **Proper sticky positioning** - Works perfectly
✅ **Native browser recording** - More reliable
✅ **Professional animations** - Smooth transitions
✅ **Responsive design** - Adapts to sidebar automatically

## Testing

1. Build component: `npm run build`
2. Restart Streamlit: `streamlit run app.py`
3. Test:
   - Type message and press Enter
   - Click mic button to record
   - Check responsive behavior with sidebar
   - Verify sticky positioning

## Troubleshooting

### Component not showing:
- Check `dist/` folder exists
- Verify `_RELEASE = True` in `__init__.py`
- Check browser console for errors

### Mic not working:
- Allow microphone permissions in browser
- Check HTTPS (required for mic access)
- Test in different browser

### Enter key not working:
- Should work by default
- Check browser console for JavaScript errors

## Next Steps

After successful integration:
1. Remove `streamlit_mic_recorder` from requirements.txt
2. Test all functionality
3. Deploy to production

Your chat interface will be production-ready! 🚀
