__author__ = "VATSAL VARSHNEY"

import streamlit as st
import sys
from pathlib import Path
import streamlit.components.v1 as components

# Add project root to Python path for local development
project_root = Path(__file__).parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from utils.common import (init_session_state, display_tool_grid, search_tools, navigate_to_tool, 
                         get_search_suggestions, display_favorites_section, display_recent_tools_section)

# Configure page
st.set_page_config(
    page_title="Ultimate All-in-One Digital Toolkit",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
init_session_state()

# Tool categories configuration with lazy loading
TOOL_CATEGORIES = {
    "AI Tools": {"icon": "🤖", "description": "Artificial intelligence and machine learning tools", "module": "ai_tools",
                 "color": "#FFFFFF", "background-color": "#000000"},
    "Audio/Video Tools": {"icon": "🎵", "description": "Media processing and editing tools", "module": "audio_video_tools",
                          "color": "#FFFFFF", "background-color": "#000000"},
    "Coding Tools": {"icon": "💻", "description": "Programming utilities and development tools", "module": "coding_tools",
                     "color": "#FFFFFF", "background-color": "#000000"},
    "Color Tools": {"icon": "🌈", "description": "Color palettes, converters, and design tools", "module": "color_tools",
                    "color": "#FFFFFF", "background-color": "#000000"},
    "CSS Tools": {"icon": "🎨", "description": "CSS generators, validators, and design tools", "module": "css_tools",
                  "color": "#FFFFFF", "background-color": "#000000"},
    "Data Tools": {"icon": "📊", "description": "Data analysis and visualization tools", "module": "data_tools",
                   "color": "#FFFFFF", "background-color": "#000000"},
    "File Tools": {"icon": "📁", "description": "File management and conversion utilities", "module": "file_tools",
                   "color": "#FFFFFF", "background-color": "#000000"},
    "Image Tools": {"icon": "🖼️", "description": "Image editing, conversion, and analysis tools", "module": "image_tools",
                    "color": "#FFFFFF", "background-color": "#000000"},
    "Science/Math Tools": {"icon": "🧮", "description": "Scientific calculators and mathematical tools",
                           "module": "science_math_tools", "color": "#FFFFFF", "background-color": "#000000"},
    "Security/Privacy Tools": {"icon": "🔒", "description": "Cybersecurity, privacy, and encryption tools",
                               "module": "security_tools", "color": "#FFFFFF", "background-color": "#000000"},
    "Social Media Tools": {"icon": "📱", "description": "Social media management and analytics",
                           "module": "social_media_tools", "color": "#FFFFFF", "background-color": "#000000"},
    "SEO/Marketing Tools": {"icon": "📈", "description": "Search optimization and marketing analytics",
                            "module": "seo_marketing_tools", "color": "#FFFFFF", "background-color": "#000000"},
    "Text Tools": {"icon": "📝", "description": "Text processing, analysis, and manipulation tools",
                   "module": "text_tools", "color": "#FFFFFF", "background-color": "#000000"},
    "Web Developer Tools": {"icon": "🌐", "description": "Web development and testing utilities",
                            "module": "web_dev_tools", "color": "#FFFFFF", "background-color": "#000000"},
    "News & Events Tools": {"icon": "📰", "description": "Real-time news, events, and current updates",
                           "module": "news_tools", "color": "#FFFFFF", "background-color": "#000000"},
    "Portfolio": {"icon": "📁", "description": "Portfolio and project showcase", "module": "connect",
                  "color": "#FFFFFF", "background-color": "#000000"}
}

def lazy_import_module(module_name):
    """Lazy import modules only when needed"""
    if module_name == "connect":
        from connect import display_connect_page
        return type('obj', (object,), {'display_tools': display_connect_page})()
    elif module_name == "ai_assistant":
        from ai_assistant import display_ai_assistant  
        return type('obj', (object,), {'display_tools': display_ai_assistant})()
    else:
        import importlib
        return importlib.import_module(f'tools.{module_name}')


def main():
    # Header with better spacing
    st.markdown("<div style='padding: 2rem 0 1rem 0;'></div>", unsafe_allow_html=True)
    
    col_left, col_center, col_right = st.columns([1, 3, 1])
    with col_center:
        st.markdown("""
        <div style="text-align: center;">
            <h1 style="font-size: 3rem; margin-bottom: 0.5rem; font-weight: 700;">🛠️ In One Box</h1>
            <p style="font-size: 1rem; opacity: 0.8; margin-bottom: 1rem;">वत्सल वार्ष्णेय</p>
            <p style="font-size: 1.1rem; line-height: 1.6; opacity: 0.9; max-width: 800px; margin: 0 auto;">
                A comprehensive digital workspace that brings together essential tools for developers, designers, 
                content creators, and professionals. Access 500+ Tools of specialized tools - all from one place.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='padding: 1.5rem 0;'></div>", unsafe_allow_html=True)
    
    # Navigation with better layout
    with st.container():
        nav_col1, nav_col2 = st.columns([3, 1])
        
        with nav_col1:
            search_query = st.text_input("🔍 Search Tools", placeholder="Type to search for tools...", 
                                        key="search_tools", label_visibility="collapsed")
            search_filter = "All"
        
        with nav_col2:
            button_col1, button_col2 = st.columns(2)
            with button_col1:
                if st.button("Vatsal Your Assistant", type="primary", use_container_width=True):
                    selected_category = "AI Assistant"
            with button_col2:
                if st.button("📁 Portfolio", type="secondary", use_container_width=True):
                    selected_category = "Portfolio"
    
    # Category selector with cleaner design
    selected_category = st.selectbox(
        "Select a category to explore",
        ["Dashboard", "AI Assistant", "Admin Feedback"] + list(TOOL_CATEGORIES.keys()),
        index=0 if 'selected_category' not in st.session_state else
        (["Dashboard", "AI Assistant", "Admin Feedback"] + list(TOOL_CATEGORIES.keys())).index(
            st.session_state.selected_category) if st.session_state.selected_category in (
                ["Dashboard", "AI Assistant", "Admin Feedback"] + list(TOOL_CATEGORIES.keys())) else 0,
        label_visibility="collapsed"
    )

    # Search functionality
    if search_query:
        if len(search_query) >= 1:
            suggestions = get_search_suggestions(search_query)
            if suggestions and len(search_query) < 4:
                st.caption("💡 Suggestions: " + " • ".join([f"`{s}`" for s in suggestions]))

        search_results = search_tools(search_query, TOOL_CATEGORIES, search_filter)
        if search_results:
            total_results = sum(len(tools) for tools in search_results.values())
            st.markdown(f"### 🔍 Search Results ({total_results} tools found)")
            if search_filter != "All":
                st.info(f"🔍 Filtered by: **{search_filter}**")

            for category, tools in search_results.items():
                with st.expander(f"📂 {category} ({len(tools)} tools found)", expanded=True):
                    cols = st.columns(2)
                    for i, tool in enumerate(tools):
                        with cols[i % 2]:
                            st.markdown(f"**{tool['name']}**")
                            st.caption(f"📁 {tool.get('subcategory', 'General')} • Score: {tool.get('score', 0):.2f}")
                            if st.button(f"Open {tool['name']}", key=f"search_{tool['id']}", type="secondary"):
                                navigate_to_tool(category, tool['name'])
                            st.markdown("---")
        else:
            if len(search_query) >= 2:
                st.warning(f"🔍 No tools found for '{search_query}'" + (
                    f" in {search_filter}" if search_filter != "All" else ""))
                st.info("💡 Try using different keywords or remove the category filter")
        st.markdown("---")

    if selected_category != "Dashboard":
        st.session_state.selected_category = selected_category

    st.markdown("<div style='padding: 1rem 0;'></div>", unsafe_allow_html=True)

    # Main content with better spacing
    if selected_category == "Portfolio":
        with st.container():
            from connect import display_connect_page
            display_connect_page()
    elif selected_category == "Admin Feedback":
        with st.container():
            from ai_assistant import display_ai_assistant
            display_ai_assistant()
    elif selected_category == "AI Assistant":
        with st.container():
            from ai_assistant import display_ai_assistant
            display_ai_assistant()
    elif selected_category == "Dashboard" or 'selected_category' not in st.session_state:
        # Welcome banner with better design
        with st.container():
            st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(168, 200, 255, 0.15), rgba(196, 167, 255, 0.15)); 
                        padding: 2rem; border-radius: 12px; margin: 1rem 0 2rem 0; text-align: center;
                        border: 1px solid rgba(255, 255, 255, 0.1);">
                <h2 style="margin: 0 0 0.5rem 0;">✨ Welcome to Your Digital Toolkit</h2>
                <p style="margin: 0; opacity: 0.85; font-size: 1.05rem;">
                    Select a category below to explore specialized tools designed for your workflow
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Favorites and recent tools with better spacing
        with st.container():
            col1, col2 = st.columns(2, gap="large")
            
            with col1:
                display_favorites_section()
                
            with col2:
                display_recent_tools_section()
        
        st.markdown("<div style='padding: 2rem 0 1rem 0;'></div>", unsafe_allow_html=True)
        
        # Tool categories section
        with st.container():
            st.markdown("<h2 style='text-align: center; margin-bottom: 2rem;'>🛠️ Explore Tool Categories</h2>", 
                       unsafe_allow_html=True)
            display_tool_grid(TOOL_CATEGORIES)
    else:
        # Back button with better styling
        col1, col2, col3 = st.columns([2, 6, 2])
        with col1:
            if st.button("← Dashboard", type="secondary", use_container_width=True):
                if 'selected_category' in st.session_state:
                    del st.session_state.selected_category
                st.rerun()

        st.markdown("<div style='padding: 1rem 0;'></div>", unsafe_allow_html=True)

        # Category content with better container
        with st.container():
            category_info = TOOL_CATEGORIES[st.session_state.selected_category]
            st.markdown(f"<h1 style='text-align: center;'>{category_info['icon']} {st.session_state.selected_category}</h1>", 
                       unsafe_allow_html=True)
            st.markdown("<div style='padding: 1rem 0;'></div>", unsafe_allow_html=True)
            try:
                module = lazy_import_module(category_info['module'])
                module.display_tools()
            except Exception as e:
                st.error(f"⚠️ Unable to load {st.session_state.selected_category}")
                st.info("💡 Try refreshing the page or selecting a different category")
                with st.expander("Technical Details"):
                    st.code(str(e))


if __name__ == "__main__":
    main()
