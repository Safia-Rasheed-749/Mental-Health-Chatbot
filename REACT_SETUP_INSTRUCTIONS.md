# React Chat Component Setup Instructions

## Prerequisites
1. Install Node.js from: https://nodejs.org/ (LTS version recommended)
2. Verify installation:
   ```bash
   node --version
   npm --version
   ```

## Step-by-Step Setup

### 1. Navigate to Component Directory
```bash
cd frontend/components/sticky_chat/frontend
```

### 2. Install Dependencies
```bash
npm install
```

This will install:
- React 18.2.0
- React DOM 18.2.0
- Streamlit Component Lib 2.0.0
- Vite 4.3.9 (build tool)
- @vitejs/plugin-react 4.0.0

### 3. Build the Component
```bash
npm run build
```

This creates a `dist/` folder with the compiled component.

### 4. Verify Build
Check that `frontend/components/sticky_chat/frontend/dist/` folder exists with:
- `index.html`
- `assets/` folder with JS and CSS files

## Integration with Streamlit

The component is already integrated! After building, just use it in your chat.py:

```python
from components.sticky_chat import sticky_chat_bar

# Use the component
user_input = sticky_chat_bar(key="chat_input")

# Handle the response
if user_input:
    if user_input["type"] == "text":
        text = user_input["data"]
        # Process text message
        
    elif user_input["type"] == "audio":
        audio_bytes = bytes(user_input["data"])
        # Process audio recording
```

## Features

✅ **Sticky at bottom** - Always visible
✅ **Enter key works** - Press Enter to send
✅ **Mic inline** - Green mic button on left
✅ **Voice recording** - Click to record (5 sec max)
✅ **Responsive** - Adjusts with sidebar
✅ **Professional UI** - Gradient buttons, animations

## Troubleshooting

### If npm command not found:
- Restart terminal after installing Node.js
- Add Node.js to PATH manually

### If build fails:
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run build
```

### If component doesn't show:
- Check that `dist/` folder exists
- Verify `__init__.py` has `_RELEASE = True`
- Restart Streamlit app

## Development Mode (Optional)

For live development with hot reload:

1. Start Vite dev server:
   ```bash
   npm run dev
   ```

2. In `__init__.py`, set:
   ```python
   _RELEASE = False
   ```

3. Component will load from http://localhost:5173

## File Structure

```
frontend/components/sticky_chat/
├── __init__.py                 # Python wrapper
└── frontend/
    ├── src/
    │   ├── App.jsx            # React component
    │   ├── index.css          # Styles
    │   └── main.jsx           # Entry point
    ├── index.html             # HTML template
    ├── package.json           # Dependencies
    ├── vite.config.js         # Build config
    └── dist/                  # Built files (after npm run build)
        ├── index.html
        └── assets/
```

## Next Steps

After building, update `chat.py` to use the custom component instead of `st.chat_input()` and `mic_recorder()`.

See `CHAT_INTEGRATION_GUIDE.md` for detailed integration instructions.
