import streamlit as st
import time
from enhanced_rag import enhanced_rag
from api_tools import display_api_tools


def display_ai_assistant():
    # Header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1>🤖 Vatsal - Your Personal Toolkit Guide</h1>
        <div style="background: linear-gradient(45deg, #a8c8ff, #c4a7ff); 
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                    background-clip: text; font-size: 1.2rem; font-weight: 500;">
            ✨ Ask me anything about the 500+ tools - I'll help you find what you need! ✨
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Chat interface container
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(168, 200, 255, 0.1), rgba(196, 167, 255, 0.1)); 
                padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem;
                border: 1px solid rgba(255, 255, 255, 0.2);">
    """, unsafe_allow_html=True)

    # Initialize chat history
    if 'ai_chat_messages' not in st.session_state:
        st.session_state.ai_chat_messages = [
            {
                "role": "assistant",
                "content": "👋 **Hi! I'm Vatsal AI - Your Personal Toolkit Guide**\n\n* Created by Vatsal Varshney*\n\n**I'll help you find the perfect tool from our 500+ collection!**\n\nJust tell me what you need:\n- 🎨 \"I want to edit images\" → I'll show you Image Tools\n- 🤖 \"I need AI tools\" → I'll guide you to AI features\n- 📝 \"Help with text\" → I'll find Text Tools for you\n- 📊 \"Analyze data\" → I'll show Data Tools\n\n**💡 Try asking me anything below, or click a suggestion:**",
                "suggestions": [
                    "Show me AI tools",
                    "I need to edit images",
                    "Help with text processing",
                    "Data analysis tools",
                    "View Vatsal's portfolio"
                ]
            }
        ]

    # Display chat messages
    for i, message in enumerate(st.session_state.ai_chat_messages):
        with st.chat_message(message["role"]):
            st.write(message["content"])

            # Display suggestion buttons for assistant messages
            if message["role"] == "assistant" and "suggestions" in message:
                st.markdown("**💡 Quick suggestions:**")
                cols = st.columns(min(3, len(message["suggestions"])))
                for j, suggestion in enumerate(message["suggestions"]):
                    with cols[j % 3]:
                        if st.button(suggestion, key=f"suggestion_{i}_{j}", use_container_width=True):
                            handle_user_input(suggestion)

    # Chat input with improved prompt
    st.markdown("---")
    st.markdown("### 💬 Ask Vatsal AI Assistant")
    if prompt := st.chat_input("💡 What tool are you looking for? Ask me anything... (e.g., 'I need to resize images' or 'Show me AI tools')"):
        handle_user_input(prompt)

    st.markdown("</div>", unsafe_allow_html=True)

    # Quick action buttons
    st.markdown("### 🚀 Quick Category Navigation")

    quick_col1, quick_col2, quick_col3, quick_col4 = st.columns(4)

    with quick_col1:
        if st.button("🤖 AI Tools", use_container_width=True, type="secondary"):
            navigate_to_category("AI Tools")

    with quick_col2:
        if st.button("📝 Text Tools", use_container_width=True, type="secondary"):
            navigate_to_category("Text Tools")

    with quick_col3:
        if st.button("🖼️ Image Tools", use_container_width=True, type="secondary"):
            navigate_to_category("Image Tools")

    with quick_col4:
        if st.button("📊 Data Tools", use_container_width=True, type="secondary"):
            navigate_to_category("Data Tools")

    # Second row of quick actions
    quick_col5, quick_col6, quick_col7, quick_col8 = st.columns(4)

    with quick_col5:
        if st.button("💻 Coding Tools", use_container_width=True, type="secondary"):
            navigate_to_category("Coding Tools")

    with quick_col6:
        if st.button("🔒 Security Tools", use_container_width=True, type="secondary"):
            navigate_to_category("Security/Privacy Tools")

    with quick_col7:
        if st.button("🌐 Web Dev Tools", use_container_width=True, type="secondary"):
            navigate_to_category("Web Developer Tools")

    with quick_col8:
        if st.button("👨‍💻 Creator Portfolio", use_container_width=True, type="primary"):
            navigate_to_category("Portfolio")

    # API Tools section
    st.markdown("---")
    st.markdown("### 🔌 API Tools")

    if st.button("🧪 Open API Testing Tools", type="secondary", use_container_width=True):
        st.session_state.show_api_tools = True

    # Display API tools if requested
    if st.session_state.get('show_api_tools', False):
        with st.expander("🔌 API Tools Suite", expanded=True):
            # Pass the selected tool to auto-select it
            selected_tool = st.session_state.get('selected_api_tool', None)
            display_api_tools(auto_select_tool=selected_tool if selected_tool else "")
            if st.button("❌ Close API Tools"):
                st.session_state.show_api_tools = False
                st.session_state.selected_api_tool = None
                st.rerun()

    # Clear chat and help sections
    st.markdown("---")

    clear_col, help_col = st.columns(2)

    with clear_col:
        if st.button("🗑️ Clear Chat History", type="secondary", use_container_width=True):
            st.session_state.ai_chat_messages = st.session_state.ai_chat_messages[:1]  # Keep initial message
            st.rerun()

    with help_col:
        if st.button("❓ Show Help Examples", type="secondary", use_container_width=True):
            show_help_examples()

    # Help section
    with st.expander("💡 How to use the AI Assistant"):
        st.markdown("""
        **Examples of what you can ask:**

        🔍 **Finding tools:**
        - "I need to resize images"
        - "How do I generate secure passwords?"
        - "Show me text analysis tools"
        - "What tools help with data visualization?"

        🎯 **Getting help:**
        - "How do I convert file formats?"
        - "What coding tools are available?"
        - "Help me with SEO optimization"
        - "Show me all AI-powered features"

        💡 **Exploring features:**
        - "What can the security tools do?"
        - "Show me all image editing options"
        - "What's available for web development?"
        - "Help me understand the text tools"

        The AI assistant understands natural language and will guide you to exactly what you need!
        """)


def handle_user_input(prompt: str):
    """Handle user input and generate AI response"""

    # Add user message to chat
    st.session_state.ai_chat_messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.write(prompt)

    # Generate and display AI response
    with st.chat_message("Vatsal"):
        with st.spinner("🤔 Thinking..."):
            try:
                # Get response from enhanced RAG system with web search
                result = enhanced_rag.search_and_respond_enhanced(prompt)
                response = result["response"]
                navigation_targets = result["navigation_targets"]

                st.write(response)

                # Add specific tool navigation buttons
                if navigation_targets:
                    st.markdown("**🎯 Direct Tool Access:**")
                    nav_cols = st.columns(min(3, len(navigation_targets)))
                    for i, target in enumerate(navigation_targets[:3]):
                        with nav_cols[i]:
                            button_text = target["tool"] if target["tool"] else target["category"]
                            if st.button(f"Open {button_text}", key=f"nav_{len(st.session_state.ai_chat_messages)}_{i}",
                                         use_container_width=True):
                                if target["tool"]:
                                    navigate_to_specific_tool(target["category"], target["tool"])
                                else:
                                    navigate_to_category(target["category"])

                # Add to chat history
                assistant_message = {
                    "role": "assistant",
                    "content": response
                }

                if navigation_targets:
                    assistant_message["navigation_targets"] = navigation_targets

                st.session_state.ai_chat_messages.append(assistant_message)

            except Exception as e:
                error_message = "I apologize, but I encountered an issue processing your request. Please try rephrasing your question or use the category buttons to navigate directly to the tools you need."
                st.write(error_message)
                st.session_state.ai_chat_messages.append({"role": "assistant", "content": error_message})


def navigate_to_category(category_name: str):
    """Navigate to a specific tool category"""
    st.session_state.selected_category = category_name
    st.success(f"✅ Navigating to {category_name}...")
    time.sleep(0.5)
    st.rerun()


def navigate_to_specific_tool(category_name: str, tool_name: str):
    """Navigate to a specific tool within a category"""
    st.session_state.selected_category = category_name

    # Handle API tools specifically - auto-open them
    if tool_name in ["API Tester", "JSON Formatter", "Webhook Tester", "API Response Analyzer"]:
        st.session_state.show_api_tools = True
        st.session_state.selected_api_tool = tool_name

    # Store the specific tool to highlight/open in other categories
    st.session_state.target_tool = tool_name
    st.success(f"✅ Opening {tool_name} in {category_name}...")
    time.sleep(0.5)
    st.rerun()


def show_help_examples():
    examples = [
        "Show me AI tools for content creation",
        "I need help with image editing",
        "What security tools do you have?",
        "Help me analyze data and create charts"
    ]

    st.session_state.ai_chat_messages.append({
        "role": "assistant",
        "content": "**Here are some example questions you can ask:**\n\n" + "\n".join(
            [f"• {ex}" for ex in examples]) + "\n\n**Try any of these or ask your own question!**",
        "suggestions": examples
    })
    st.rerun()

