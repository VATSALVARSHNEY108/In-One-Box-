import streamlit as st
import json
import requests
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from utils.common import create_tool_header, show_progress_bar, add_to_recent, create_favorite_button
from utils.ai_client import ai_client
import urllib.parse


def display_tools():
    """Display news and events tools"""
    create_tool_header("News & Events Tools", "Stay updated with real-time news and current events", "📰")

    # Add to recent tools
    add_to_recent("News & Events Tools")

    # Tool categories
    tool_categories = {
        "Breaking News": [
            "Live News Feed",
            "Trending Topics",
            "News by Category"
        ],
        "Events & Updates": [
            "Technology News",
            "Business Updates",
            "Weather Updates"
        ],
        "News Analysis": [
            "News Sentiment Analysis",
            "News Summarizer",
            "Fact Checker"
        ],
        "Search & Tools": [
            "Keyword News Search"
        ]
    }

    # Display tool categories
    for category, tools in tool_categories.items():
        with st.expander(f"📂 {category}", expanded=True):
            cols = st.columns(2)
            for i, tool in enumerate(tools):
                with cols[i % 2]:
                    if st.button(f"🔧 {tool}", key=f"news_{tool}", use_container_width=True):
                        display_news_tool(tool)


def display_news_tool(tool_name: str):
    """Display specific news tool"""
    st.markdown("---")

    # Create favorite button
    create_favorite_button(tool_name, "News & Events Tools", "news_tools")

    if tool_name == "Live News Feed":
        display_live_news_feed()
    elif tool_name == "Trending Topics":
        display_trending_topics()
    elif tool_name == "News by Category":
        display_news_by_category()
    elif tool_name == "Technology News":
        display_technology_news()
    elif tool_name == "Business Updates":
        display_business_updates()
    elif tool_name == "News Sentiment Analysis":
        display_news_sentiment_analysis()
    elif tool_name == "News Summarizer":
        display_news_summarizer()
    elif tool_name == "Keyword News Search":
        display_keyword_news_search()
    elif tool_name == "Weather Updates":
        display_weather_updates()
    elif tool_name == "Sports News":
        display_sports_news()
    elif tool_name == "Fact Checker":
        display_fact_checker()
    elif tool_name == "News Comparison":
        display_news_comparison()
    else:
        st.info(f"🚧 {tool_name} is coming soon! This feature is currently under development.")


def get_news_with_gemini(query: str, category: str = "general") -> List[Dict]:
    """Get real-time news using Gemini web search capabilities"""
    try:
        # Import the enhanced RAG for web search capabilities
        from enhanced_rag import enhanced_rag

        # Use the web search functionality from enhanced RAG
        web_result = enhanced_rag.search_web_with_gemini(f"latest {category} news {query} today")

        news_items = []
        if web_result and web_result.get('response'):
            # Parse the web search response into structured news items
            content = web_result['response']

            # Split content into logical sections (by paragraphs or sentences)
            sections = content.split('\n\n') if '\n\n' in content else content.split('. ')

            for i, section in enumerate(sections[:5]):  # Limit to 5 news items
                if section.strip() and len(section.strip()) > 50:  # Filter out very short sections
                    # Extract title from the first sentence or use a default
                    lines = section.strip().split('\n')
                    title = lines[0] if lines else f"Breaking: {category.title()} News"
                    if len(title) > 100:
                        title = title[:97] + "..."

                    news_items.append({
                        'title': title,
                        'content': section.strip(),
                        'source': 'Gemini Web Search',
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'category': category,
                        'is_real_time': True
                    })

            # If we got good structured data, return it
            if news_items:
                return news_items

        # Fallback: use direct news search with specific prompting
        news_prompt = f"""
        Search for and provide current real-time news about: {query}
        Category: {category}

        Please find the latest, most recent news stories from today or this week.
        Include specific details like:
        - Company names, dates, numbers, and facts
        - Recent developments and announcements  
        - Current market movements or events
        - Breaking news or trending stories

        Structure each news item with clear headlines and factual details.
        Focus on accuracy and recency - only include information you are confident is current.
        """

        response = ai_client.generate_text(news_prompt, model="gemini", max_tokens=1200)

        # Parse response into structured news items
        if response:
            # Try to identify news headlines and content
            lines = response.split('\n')
            current_item = None

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Check if this looks like a headline (starts with number, bullet, or is short)
                if (line.startswith(('1.', '2.', '3.', '4.', '5.', '-', '•')) or
                        (len(line) < 120 and line.endswith((':')) and len(news_items) < 5)):

                    # Save previous item if exists
                    if current_item:
                        news_items.append(current_item)

                    # Start new item
                    clean_title = line.lstrip('12345.-• ').rstrip(':')
                    current_item = {
                        'title': clean_title,
                        'content': '',
                        'source': 'Gemini News Search',
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'category': category,
                        'is_real_time': True
                    }
                else:
                    # Add to content of current item
                    if current_item:
                        current_item['content'] += ' ' + line if current_item['content'] else line

            # Don't forget the last item
            if current_item and current_item['content']:
                news_items.append(current_item)

        return news_items[:5]  # Limit to 5 items

    except Exception as e:
        st.error(f"Error fetching real-time news: {e}")
        return get_fallback_news(category)


def get_fallback_news(category: str = "general") -> List[Dict]:
    """Get fallback news data when APIs are unavailable"""
    return [
        {
            'title': f"Latest {category.title()} Updates",
            'content': f"Real-time {category} news would appear here. This is a demonstration of the news feed functionality.",
            'source': 'Demo News Source',
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'category': category
        },
        {
            'title': "Breaking News Alert",
            'content': "Stay informed with the latest developments in your chosen categories. The news feed updates automatically.",
            'source': 'Live News Feed',
            'timestamp': (datetime.now() - timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S"),
            'category': category
        }
    ]


def display_live_news_feed():
    """Display live news feed"""
    st.subheader("📡 Live News Feed")
    st.markdown("Get real-time news updates from multiple sources")

    # News source selection
    col1, col2 = st.columns([2, 1])
    with col1:
        categories = ["general", "technology", "business", "sports", "health", "entertainment", "science"]
        selected_category = st.selectbox("Select News Category:", categories)

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Refresh News", type="primary"):
            st.session_state.news_refresh = True

    # Auto-refresh option and cache management
    auto_refresh = st.checkbox("🔄 Auto-refresh every 5 minutes")

    # Check if we need to refresh based on session state
    should_refresh = (
            st.session_state.get('news_refresh', False) or
            auto_refresh or
            f'news_cache_{selected_category}' not in st.session_state or
            time.time() - st.session_state.get(f'news_cache_time_{selected_category}', 0) > 300  # 5 minutes
    )

    if auto_refresh:
        st.info("🔄 Auto-refresh enabled. News updates every 5 minutes.")

    # Reset refresh flag
    if st.session_state.get('news_refresh', False):
        st.session_state.news_refresh = False

    st.markdown("---")

    # Get and display news with caching
    if should_refresh:
        with st.spinner("🔍 Fetching latest news..."):
            news_items = get_news_with_gemini(f"latest {selected_category} news today", selected_category)

            if not news_items:
                news_items = get_fallback_news(selected_category)

            # Cache the results
            st.session_state[f'news_cache_{selected_category}'] = news_items
            st.session_state[f'news_cache_time_{selected_category}'] = time.time()
    else:
        # Use cached news if available
        news_items = st.session_state.get(f'news_cache_{selected_category}', get_fallback_news(selected_category))

    # Display news items
    for i, item in enumerate(news_items):
        with st.container():
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, rgba(168, 200, 255, 0.1), rgba(196, 167, 255, 0.1));
                padding: 1.5rem; 
                border-radius: 10px; 
                margin: 1rem 0;
                border-left: 4px solid #4A90E2;
            ">
                <h4 style="margin: 0; color: #4A90E2;">📰 {item['title']}</h4>
                <p style="margin: 0.5rem 0; opacity: 0.7; font-size: 0.8rem;">
                    🕒 {item['timestamp']} | 📍 {item['source']} | 📁 {item['category'].title()}
                </p>
                <p style="margin: 0.5rem 0;">{item['content']}</p>
            </div>
            """, unsafe_allow_html=True)

            # Action buttons for each news item
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button("📊 Analyze", key=f"analyze_{i}"):
                    analyze_news_sentiment(item['content'])
            with col2:
                if st.button("📝 Summarize", key=f"summarize_{i}"):
                    summarize_news_item(item['content'])
            with col3:
                st.markdown("")  # Spacer


def display_trending_topics():
    """Display trending topics"""
    st.subheader("🔥 Trending Topics")
    st.markdown("Discover what's trending right now")

    # Time range selection
    time_range = st.selectbox("Time Range:", ["Last Hour", "Last 24 Hours", "Last Week"])

    with st.spinner("🔍 Finding trending topics..."):
        trending_query = f"trending topics and viral news in the {time_range.lower()}"
        trending_items = get_news_with_gemini(trending_query, "trending")

        if not trending_items:
            trending_items = get_fallback_news("trending")

    # Display trending items
    for i, item in enumerate(trending_items, 1):
        with st.expander(f"🔥 Trending #{i}: {item['title']}", expanded=i <= 2):
            st.write(item['content'])
            st.caption(f"📍 {item['source']} • 🕒 {item['timestamp']}")


def display_news_by_category():
    """Display news by specific category"""
    st.subheader("📂 News by Category")
    st.markdown("Browse news from specific categories")

    # Category grid
    categories = {
        "Technology": "💻",
        "Business": "💼",
        "Sports": "⚽",
        "Health": "🏥",
        "Science": "🔬",
        "Entertainment": "🎬",
        "Politics": "🏛️",
        "Environment": "🌍"
    }

    cols = st.columns(4)
    selected_categories = []

    for i, (category, icon) in enumerate(categories.items()):
        with cols[i % 4]:
            if st.button(f"{icon} {category}", key=f"cat_{category}", use_container_width=True):
                selected_categories.append(category.lower())

    if selected_categories:
        for category in selected_categories:
            st.markdown(f"### {categories[category.title()]} {category.title()} News")

            with st.spinner(f"Loading {category} news..."):
                news_items = get_news_with_gemini(f"latest {category} news", category)

                if not news_items:
                    news_items = get_fallback_news(category)

            for item in news_items[:3]:  # Show top 3 items per category
                with st.container():
                    st.markdown(f"**📰 {item['title']}**")
                    st.write(item['content'])
                    st.caption(f"📍 {item['source']} • 🕒 {item['timestamp']}")
                    st.markdown("---")


def display_technology_news():
    """Display technology-specific news"""
    st.subheader("💻 Technology News")
    st.markdown("Latest updates from the tech world")

    # Tech subcategories
    tech_topics = st.multiselect(
        "Select Technology Topics:",
        ["AI & Machine Learning", "Software Development", "Hardware", "Startups", "Cybersecurity", "Mobile Tech"],
        default=["AI & Machine Learning", "Software Development"]
    )

    if tech_topics:
        query = " and ".join(tech_topics)
        with st.spinner("🔍 Fetching technology news..."):
            tech_news = get_news_with_gemini(f"latest technology news about {query}", "technology")

            if not tech_news:
                tech_news = get_fallback_news("technology")

        for item in tech_news:
            with st.expander(f"💻 {item['title']}", expanded=True):
                st.write(item['content'])
                st.caption(f"📍 {item['source']} • 🕒 {item['timestamp']}")


def display_business_updates():
    """Display business news and updates"""
    st.subheader("💼 Business Updates")
    st.markdown("Stay informed about business and financial news")

    # Business categories
    business_cat = st.selectbox(
        "Business Category:",
        ["Markets & Finance", "Startups & Funding", "Corporate News", "Economic Indicators", "Global Business"]
    )

    with st.spinner("📈 Loading business updates..."):
        business_news = get_news_with_gemini(f"latest business news about {business_cat}", "business")

        if not business_news:
            business_news = get_fallback_news("business")

    for item in business_news:
        st.markdown(f"### 📈 {item['title']}")
        st.write(item['content'])
        st.caption(f"📍 {item['source']} • 🕒 {item['timestamp']}")
        st.markdown("---")


def display_news_sentiment_analysis():
    """Analyze sentiment of news articles"""
    st.subheader("📊 News Sentiment Analysis")
    st.markdown("Analyze the emotional tone of news content")

    # Input methods
    input_method = st.radio("Choose input method:", ["Paste News Text", "Fetch Latest News"])

    if input_method == "Paste News Text":
        news_text = st.text_area("Paste news article text:", height=200)

        if news_text and st.button("📊 Analyze Sentiment"):
            analyze_news_sentiment(news_text)

    else:
        category = st.selectbox("News Category:", ["general", "technology", "business", "sports"])

        if st.button("🔍 Fetch & Analyze Latest News"):
            with st.spinner("Fetching and analyzing news..."):
                news_items = get_news_with_gemini(f"latest {category} news", category)

                if news_items:
                    for item in news_items[:3]:
                        st.markdown(f"### 📰 {item['title']}")
                        analyze_news_sentiment(item['content'])
                        st.markdown("---")


def analyze_news_sentiment(text: str):
    """Analyze sentiment of given text"""
    try:
        sentiment_prompt = f"""
        Analyze the emotional tone and sentiment of this news text:

        Text: {text}

        Provide:
        1. Overall sentiment (Positive, Negative, or Neutral)
        2. Confidence score (0-100%)
        3. Key emotional indicators
        4. Brief explanation of the sentiment analysis

        Be precise and factual in your analysis.
        """

        analysis = ai_client.generate_text(sentiment_prompt, model="gemini", max_tokens=300)

        st.markdown("#### 📊 Sentiment Analysis Results:")
        st.write(analysis)

    except Exception as e:
        st.error(f"Error analyzing sentiment: {e}")


def display_news_summarizer():
    """Summarize news articles"""
    st.subheader("📝 News Summarizer")
    st.markdown("Get concise summaries of long news articles")

    # Input options
    col1, col2 = st.columns(2)
    with col1:
        summary_length = st.selectbox("Summary Length:",
                                      ["Brief (1-2 sentences)", "Medium (1 paragraph)", "Detailed (2-3 paragraphs)"])
    with col2:
        focus_area = st.selectbox("Focus On:", ["Key Facts", "Impact & Consequences", "Timeline", "People Involved"])

    news_text = st.text_area("Paste news article or URL:", height=200)

    if news_text and st.button("📝 Generate Summary"):
        summarize_news_item(news_text, summary_length, focus_area)


def summarize_news_item(text: str, length: str = "Medium", focus: str = "Key Facts"):
    """Summarize a news item"""
    try:
        summary_prompt = f"""
        Summarize this news article with the following requirements:

        Text: {text}

        Length: {length}
        Focus: {focus}

        Provide a clear, concise summary that captures the most important information.
        """

        summary = ai_client.generate_text(summary_prompt, model="gemini", max_tokens=400)

        st.markdown("#### 📝 News Summary:")
        st.info(summary)

    except Exception as e:
        st.error(f"Error summarizing news: {e}")


def display_keyword_news_search():
    """Search news by keywords"""
    st.subheader("🔍 Keyword News Search")
    st.markdown("Search for news articles using specific keywords")

    # Search configuration
    col1, col2 = st.columns(2)
    with col1:
        keywords = st.text_input("Enter keywords (comma-separated):")
    with col2:
        search_period = st.selectbox("Time Period:", ["Today", "This Week", "This Month", "All Time"])

    # Advanced filters
    with st.expander("🔧 Advanced Filters"):
        col1, col2 = st.columns(2)
        with col1:
            language = st.selectbox("Language:", ["English", "All Languages"])
            source_type = st.selectbox("Source Type:", ["All Sources", "Major News", "Tech Blogs", "Financial News"])
        with col2:
            sort_by = st.selectbox("Sort By:", ["Relevance", "Date", "Popularity"])
            max_results = st.slider("Max Results:", 1, 20, 10)

    if keywords and st.button("🔍 Search News"):
        with st.spinner("🔍 Searching for news..."):
            search_query = f"news about {keywords} in {search_period.lower()}"
            search_results = get_news_with_gemini(search_query, "search")

            if not search_results:
                search_results = get_fallback_news("search")

        st.markdown(f"### 🔍 Search Results for: {keywords}")

        for i, item in enumerate(search_results[:max_results], 1):
            with st.expander(f"📰 Result {i}: {item['title']}", expanded=i <= 3):
                st.write(item['content'])
                st.caption(f"📍 {item['source']} • 🕒 {item['timestamp']}")


def display_weather_updates():
    """Display weather updates and alerts"""
    st.subheader("🌤️ Weather Updates")
    st.markdown("Current weather conditions and forecasts")

    location = st.text_input("Enter location (city, country):", value="New York, USA")

    if location and st.button("🌤️ Get Weather Update"):
        with st.spinner("🌤️ Fetching weather information..."):
            weather_query = f"current weather and forecast for {location}"
            weather_info = get_news_with_gemini(weather_query, "weather")

            if weather_info:
                for item in weather_info:
                    st.markdown(f"### 🌤️ Weather for {location}")
                    st.write(item['content'])
                    st.caption(f"📍 {item['source']} • 🕒 {item['timestamp']}")
            else:
                st.info("Weather information is currently unavailable. Please try again later.")


def display_sports_news():
    """Display sports news and updates"""
    st.subheader("⚽ Sports News")
    st.markdown("Latest sports updates and scores")

    sports = st.multiselect(
        "Select Sports:",
        ["Football", "Basketball", "Soccer", "Baseball", "Tennis", "Golf", "Hockey", "Olympics"],
        default=["Football", "Basketball"]
    )

    if sports and st.button("⚽ Get Sports Updates"):
        for sport in sports:
            with st.spinner(f"🏆 Loading {sport} news..."):
                sports_query = f"latest {sport} news, scores and updates"
                sports_news = get_news_with_gemini(sports_query, "sports")

                if sports_news:
                    st.markdown(f"### 🏆 {sport} Updates")
                    for item in sports_news[:2]:  # Show top 2 items per sport
                        st.write(item['content'])
                        st.caption(f"📍 {item['source']} • 🕒 {item['timestamp']}")
                    st.markdown("---")


def display_fact_checker():
    """Fact-checking tool for news claims"""
    st.subheader("✅ Fact Checker")
    st.markdown("Verify claims and check facts from news sources")

    claim = st.text_area("Enter the claim or statement to fact-check:", height=100)

    if claim and st.button("✅ Check Facts"):
        with st.spinner("🔍 Fact-checking claim..."):
            fact_check_prompt = f"""
            Fact-check this claim or statement:

            Claim: {claim}

            Provide:
            1. Verification status (True, False, Partially True, Unverified)
            2. Supporting evidence or sources
            3. Context and explanation
            4. Any important caveats or nuances

            Be thorough and objective in your fact-checking analysis.
            """

            fact_check = ai_client.generate_text(fact_check_prompt, model="gemini", max_tokens=500)

            st.markdown("#### ✅ Fact-Check Results:")
            st.write(fact_check)


def display_news_comparison():
    """Compare news coverage from different sources"""
    st.subheader("📊 News Comparison")
    st.markdown("Compare how different sources cover the same story")

    topic = st.text_input("Enter news topic to compare:")

    if topic and st.button("📊 Compare Coverage"):
        with st.spinner("🔍 Analyzing coverage from multiple sources..."):
            comparison_query = f"how different news sources cover {topic}, compare perspectives and coverage"
            comparison_result = get_news_with_gemini(comparison_query, "comparison")

            if comparison_result:
                st.markdown(f"### 📊 Coverage Comparison: {topic}")
                for item in comparison_result:
                    st.write(item['content'])
                    st.caption(f"📍 {item['source']} • 🕒 {item['timestamp']}")
            else:
                st.info("Comparison analysis is currently unavailable. Please try again later.")