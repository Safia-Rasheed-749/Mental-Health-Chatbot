import streamlit.components.v1 as components
import os

# Set to True for production (using built files)
# Set to False for development (using dev server)
_RELEASE = True

if _RELEASE:
    # Production: use built files from dist folder
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/dist")
    _component_func = components.declare_component(
        "sticky_chat",
        path=build_dir
    )
else:
    # Development: use Vite dev server
    _component_func = components.declare_component(
        "sticky_chat",
        url="http://localhost:5173"
    )

def sticky_chat_bar(key=None):
    """
    Custom sticky chat bar component with mic and Enter key support.
    
    Returns:
        dict or None: 
            - {"type": "text", "data": str} when user sends text
            - {"type": "audio", "data": list[int]} when user records audio
            - None when no input
    """
    component_value = _component_func(key=key, default=None)
    
    # Clear the component value after reading to prevent infinite loop
    if component_value is not None:
        # Return the value once, then it will be None on next render
        return component_value
    
    return None
