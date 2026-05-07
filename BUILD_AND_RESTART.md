# Build and Restart Instructions

## Step 1: Rebuild React Component

Open CMD and run:

```cmd
cd C:\Users\HP\Desktop\Mental-Health-Chatbot\frontend\components\sticky_chat\frontend
npm run build
```

## Step 2: Restart Streamlit

```cmd
cd C:\Users\HP\Desktop\Mental-Health-Chatbot\frontend
streamlit run app.py
```

## What Was Fixed:

### 1. Infinite Loop Issue ✅
- Component now clears its value after sending
- Added `setTimeout` to set value to `null` after 100ms
- Prevents same message from being sent repeatedly

### 2. Sticky Positioning ✅
- Added CSS to make component fixed at bottom
- Component adjusts for sidebar automatically
- Messages area is scrollable

## Expected Behavior After Fix:

1. **Type message and press Enter**
   - Message sends once
   - Input clears
   - No loop/repetition

2. **Click mic button**
   - Records for 5 seconds
   - Sends once
   - No loop/repetition

3. **Chat bar position**
   - Fixed at bottom
   - Never scrolls away
   - Visible at all times

4. **Messages**
   - Scroll up/down in chat area
   - Chat bar stays at bottom

## If Still Not Working:

### Clear Browser Cache:
- Press `Ctrl + Shift + R` (hard refresh)
- Or clear cache manually

### Check Component Built:
- Verify `dist/` folder exists in:
  `frontend/components/sticky_chat/frontend/dist/`

### Check Console:
- Open browser DevTools (F12)
- Check Console tab for errors
- Check Network tab to see if component loads

## Testing Checklist:

- [ ] Type "hi" and press Enter - sends once only
- [ ] Type another message - sends once only  
- [ ] Click mic button - records and sends once
- [ ] Chat bar stays at bottom when scrolling
- [ ] Sidebar open/close - chat bar adjusts
- [ ] No infinite loops or repeated messages

If issues persist, share the error from browser console (F12).
