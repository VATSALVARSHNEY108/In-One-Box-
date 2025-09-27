import streamlit as st
import re
import json
import time
import urllib.parse
import urllib.request
from typing import List, Dict, Any, Optional
from collections import Counter
from utils.ai_client import ai_client


class EnhancedRAG:
    """Enhanced RAG system with comprehensive tool knowledge and direct tool navigation"""

    def __init__(self):
        self.knowledge_base = self._build_comprehensive_knowledge_base()
        self.tool_synonyms = self._build_synonyms_map()
        self.search_cache = {}  # Web search cache

    def _build_comprehensive_knowledge_base(self) -> List[Dict[str, Any]]:
        """Build detailed knowledge base with specific tools and their navigation paths"""
        knowledge = []

        # Website overview and creator info
        knowledge.extend([
            {
                "content": "InOneBox is a comprehensive digital toolkit with 500+ professional tools across 13+ categories created by Vatsal Varshney, an AI/ML Engineer. Navigate using search, categories, or ask me to find specific tools.",
                "tool_name": "Website Overview",
                "category": "overview",
                "keywords": ["overview", "about", "what is", "help", "navigate", "how to use", "creator", "vatsal",
                             "varshney", "who made", "author"],
                "navigation_category": "Dashboard",
                "navigation_tool": None,
                "tool_description": "General information about the InOneBox platform"
            },
            {
                "content": "Vatsal Varshney is the creator of InOneBox - an AI/ML Engineer passionate about making technology accessible. His portfolio shows his projects, experience, and contact information.",
                "tool_name": "Creator Portfolio",
                "category": "creator_info",
                "keywords": ["vatsal", "varshney", "creator", "author", "developer", "portfolio", "profile", "contact",
                             "about creator", "who made this", "connect"],
                "navigation_category": "Portfolio",
                "navigation_tool": None,
                "tool_description": "Information about the toolkit creator and his professional background"
            }
        ])

        # AI Tools - Detailed tool information
        ai_tools = [
            {
                "content": "AI Text Generation creates human-like text using advanced AI models including Gemini, OpenAI-style, and Anthropic-style responses. Perfect for creative writing, content creation, blog posts, essays, and problem-solving.",
                "tool_name": "AI Text Generation",
                "category": "ai_tools",
                "keywords": ["text generation", "ai writing", "creative writing", "content creation", "chatbot", "gpt",
                             "gemini", "generate text", "write content", "essay", "blog", "article"],
                "navigation_category": "AI Tools",
                "navigation_tool": "AI Text Generation",
                "tool_description": "Generate intelligent text content using AI models"
            },
            {
                "content": "AI Image Generation creates stunning, high-quality images from text descriptions using Google Gemini. Customize art styles, moods, color palettes, lighting, and composition. Perfect for artwork, social media, presentations.",
                "tool_name": "AI Image Generation",
                "category": "ai_tools",
                "keywords": ["image generation", "ai art", "create images", "generate images", "gemini image",
                             "art creation", "dalle", "picture", "artwork", "digital art", "ai pictures"],
                "navigation_category": "AI Tools",
                "navigation_tool": "AI Image Generation",
                "tool_description": "Create custom images from text descriptions using AI"
            },
            {
                "content": "Sentiment Analysis analyzes emotional tone in text, providing detailed insights about positive, negative, or neutral sentiments with confidence scores and emotional indicators. Great for reviews, feedback, social media.",
                "tool_name": "Sentiment Analysis",
                "category": "ai_tools",
                "keywords": ["sentiment analysis", "emotion detection", "text analysis", "mood analysis", "feeling",
                             "emotion", "positive", "negative", "review analysis"],
                "navigation_category": "AI Tools",
                "navigation_tool": "Sentiment Analysis",
                "tool_description": "Analyze emotional tone and sentiment in text content"
            },
            {
                "content": "Language Detection automatically identifies languages in text with confidence scores and detailed information including script, family, and speaker statistics. Supports multilingual content analysis.",
                "tool_name": "Language Detection",
                "category": "ai_tools",
                "keywords": ["language detection", "identify language", "detect language", "multilingual",
                             "text language", "what language", "language identifier"],
                "navigation_category": "AI Tools",
                "navigation_tool": "Language Detection",
                "tool_description": "Detect and identify languages in text content"
            },
            {
                "content": "Text Translation translates text between different languages using AI. Supports multiple target languages with high accuracy. Perfect for international communication and content localization.",
                "tool_name": "Text Translation",
                "category": "ai_tools",
                "keywords": ["translation", "translate text", "language translation", "translate", "convert language",
                             "multilingual", "foreign language"],
                "navigation_category": "AI Tools",
                "navigation_tool": "Text Translation",
                "tool_description": "Translate text between different languages"
            },
            {
                "content": "Text Summarization creates concise summaries of long documents. Specify the number of sentences and get key insights from lengthy articles, reports, or documents. Saves time and extracts main points.",
                "tool_name": "Text Summarization",
                "category": "ai_tools",
                "keywords": ["text summarization", "summarize", "text summary", "content summary", "shorten text",
                             "key points", "condense", "brief"],
                "navigation_category": "AI Tools",
                "navigation_tool": "Text Summarization",
                "tool_description": "Create concise summaries of long text content"
            }
        ]
        knowledge.extend(ai_tools)

        # Text Tools - Specific implementations
        text_tools = [
            {
                "content": "Text Counter provides comprehensive analysis including character count (with/without spaces), word count, paragraph count, reading time estimation, and keyword frequency analysis. Essential for content creators and writers.",
                "tool_name": "Text Counter",
                "category": "text_tools",
                "keywords": ["text counter", "word count", "character count", "count words", "count characters",
                             "text analysis", "reading time", "text stats", "word counter"],
                "navigation_category": "Text Tools",
                "navigation_tool": "Text Counter",
                "tool_description": "Count words, characters, and analyze text statistics"
            },
            {
                "content": "Case Converter transforms text between different formats: uppercase, lowercase, title case, sentence case, camel case, pascal case, and snake case. Perfect for programming and formatting needs.",
                "tool_name": "Case Converter",
                "category": "text_tools",
                "keywords": ["case converter", "uppercase", "lowercase", "title case", "sentence case", "camel case",
                             "pascal case", "text formatting", "change case", "convert case"],
                "navigation_category": "Text Tools",
                "navigation_tool": "Case Converter",
                "tool_description": "Convert text between different case formats"
            },
            {
                "content": "Text Formatter provides advanced formatting including line spacing, paragraph formatting, indentation, text cleanup, remove extra spaces, and organize content structure.",
                "tool_name": "Text Formatter",
                "category": "text_tools",
                "keywords": ["text formatting", "text cleanup", "paragraph formatting", "line spacing", "format text",
                             "clean text", "organize text", "fix formatting"],
                "navigation_category": "Text Tools",
                "navigation_tool": "Text Formatter",
                "tool_description": "Format and clean up text with advanced options"
            },
            {
                "content": "Find and Replace searches for specific text patterns and replaces them with new content. Supports regex patterns, case sensitivity, and bulk replacements. Great for editing and content management.",
                "tool_name": "Find and Replace",
                "category": "text_tools",
                "keywords": ["find replace", "search replace", "text search", "regex", "bulk replace",
                             "pattern matching", "find text", "replace text", "substitute"],
                "navigation_category": "Text Tools",
                "navigation_tool": "Find and Replace",
                "tool_description": "Search and replace text patterns with advanced options"
            }
        ]
        knowledge.extend(text_tools)

        # Image Tools - Comprehensive list
        image_tools = [
            {
                "content": "Image Resizer allows resizing images to custom dimensions, maintaining aspect ratio, or using preset sizes (thumbnail, social media, print). Supports JPG, PNG, WebP, and other formats.",
                "tool_name": "Image Resizer",
                "category": "image_tools",
                "keywords": ["image resize", "resize photo", "resize image", "image dimensions", "scale image",
                             "change size", "shrink image", "enlarge image"],
                "navigation_category": "Image Tools",
                "navigation_tool": "Image Resizer",
                "tool_description": "Resize images to custom dimensions or preset sizes"
            },
            {
                "content": "Image Format Converter converts between formats including JPEG, PNG, WebP, BMP, TIFF, and GIF. Adjust quality settings and optimize file sizes for web or print use.",
                "tool_name": "Image Format Converter",
                "category": "image_tools",
                "keywords": ["image converter", "format conversion", "convert image", "jpeg", "png", "webp", "bmp",
                             "image format", "change format"],
                "navigation_category": "Image Tools",
                "navigation_tool": "Image Format Converter",
                "tool_description": "Convert images between different file formats"
            },
            {
                "content": "Image Filters applies visual effects including blur, sharpen, brightness, contrast, saturation, sepia, black & white, vintage, and artistic filters. Enhance photos with professional effects.",
                "tool_name": "Image Filters",
                "category": "image_tools",
                "keywords": ["image filters", "photo effects", "image editing", "blur", "sharpen", "brightness",
                             "contrast", "photo filters", "image effects"],
                "navigation_category": "Image Tools",
                "navigation_tool": "Image Filters",
                "tool_description": "Apply visual effects and filters to images"
            },
            {
                "content": "Background Remover automatically removes backgrounds from images using AI technology. Perfect for product photos, portraits, and creating transparent backgrounds for graphics.",
                "tool_name": "Background Remover",
                "category": "image_tools",
                "keywords": ["background remover", "remove background", "transparent background", "cutout",
                             "background removal", "extract subject", "isolate object"],
                "navigation_category": "Image Tools",
                "navigation_tool": "Background Remover",
                "tool_description": "Remove backgrounds from images automatically using AI"
            }
        ]
        knowledge.extend(image_tools)

        # Data Tools - Detailed specifications
        data_tools = [
            {
                "content": "Data Visualizer creates interactive charts from CSV data including bar charts, line charts, pie charts, scatter plots, histograms, and heatmaps. Customize colors, labels, and export charts.",
                "tool_name": "Data Visualizer",
                "category": "data_tools",
                "keywords": ["data visualization", "charts", "graphs", "csv", "data analysis", "plotting", "bar chart",
                             "line chart", "pie chart", "visualize data"],
                "navigation_category": "Data Tools",
                "navigation_tool": "Data Visualizer",
                "tool_description": "Create interactive charts and visualizations from data"
            },
            {
                "content": "CSV Editor provides spreadsheet interface for editing CSV files with sorting, filtering, adding/removing columns and rows, data validation, and export options.",
                "tool_name": "CSV Editor",
                "category": "data_tools",
                "keywords": ["csv editor", "spreadsheet", "data editing", "csv manipulation", "edit csv", "csv data",
                             "table editor", "data table"],
                "navigation_category": "Data Tools",
                "navigation_tool": "CSV Editor",
                "tool_description": "Edit and manipulate CSV files with spreadsheet interface"
            },
            {
                "content": "Statistical Calculator performs calculations including mean, median, mode, standard deviation, variance, correlation, regression analysis, and hypothesis testing on datasets.",
                "tool_name": "Statistical Calculator",
                "category": "data_tools",
                "keywords": ["statistics", "statistical analysis", "mean", "median", "mode", "standard deviation",
                             "correlation", "regression", "stats", "calculate statistics"],
                "navigation_category": "Data Tools",
                "navigation_tool": "Statistical Calculator",
                "tool_description": "Perform statistical calculations and analysis on data"
            }
        ]
        knowledge.extend(data_tools)

        # API and Web Development Tools
        api_tools = [
            {
                "content": "API Tester allows testing REST APIs by sending HTTP requests (GET, POST, PUT, DELETE) with custom headers, parameters, and body data. View formatted responses and status codes.",
                "tool_name": "API Tester",
                "category": "api_tools",
                "keywords": ["api tester", "test api", "http request", "rest api", "api testing", "postman", "curl",
                             "api call", "web service"],
                "navigation_category": "AI Assistant",
                "navigation_tool": "API Tester",
                "tool_description": "Test REST APIs with custom HTTP requests"
            },
            {
                "content": "JSON Formatter validates and beautifies JSON data with syntax highlighting, error detection, and tree view. Perfect for API response formatting and debugging.",
                "tool_name": "JSON Formatter",
                "category": "api_tools",
                "keywords": ["json formatter", "json validator", "format json", "json beautifier", "json syntax",
                             "api response", "json pretty print"],
                "navigation_category": "AI Assistant",
                "navigation_tool": "JSON Formatter",
                "tool_description": "Format and validate JSON data with syntax highlighting"
            },
            {
                "content": "API Documentation Generator creates comprehensive API documentation from endpoints with parameter details, request/response examples, and interactive testing interface.",
                "tool_name": "API Documentation Generator",
                "category": "api_tools",
                "keywords": ["api documentation", "api docs", "documentation generator", "api reference", "swagger",
                             "openapi", "api spec"],
                "navigation_category": "Coding Tools",
                "navigation_tool": "API Documentation Generator",
                "tool_description": "Generate comprehensive API documentation with examples"
            },
            {
                "content": "Webhook Tester helps test webhook payloads, validate JSON structures, and simulate webhook events with HMAC signature generation for development and testing purposes.",
                "tool_name": "Webhook Tester",
                "category": "api_tools",
                "keywords": ["webhook tester", "webhook testing", "webhook simulate", "webhook debugging",
                             "api webhook", "http webhook", "hmac signature"],
                "navigation_category": "AI Assistant",
                "navigation_tool": "Webhook Tester",
                "tool_description": "Test webhook payloads and simulate webhook events"
            }
        ]
        knowledge.extend(api_tools)

        # News and Events Tools
        news_tools = [
            {
                "content": "Live News Feed provides real-time news updates from multiple sources with customizable categories including technology, business, sports, health, entertainment, and science with auto-refresh capabilities.",
                "tool_name": "Live News Feed",
                "category": "news_tools",
                "keywords": ["live news", "news feed", "real time news", "current news", "breaking news",
                             "news updates", "latest news"],
                "navigation_category": "News & Events Tools",
                "navigation_tool": "Live News Feed",
                "tool_description": "Get real-time news updates from multiple sources"
            },
            {
                "content": "Trending Topics discovers what's trending right now with viral news and popular stories across different time ranges from the last hour to the last week.",
                "tool_name": "Trending Topics",
                "category": "news_tools",
                "keywords": ["trending", "viral news", "popular topics", "trending topics", "what's trending",
                             "hot topics", "trending news"],
                "navigation_category": "News & Events Tools",
                "navigation_tool": "Trending Topics",
                "tool_description": "Discover trending topics and viral news"
            },
            {
                "content": "Technology News provides the latest updates from the tech world including AI, machine learning, software development, hardware, startups, cybersecurity, and mobile technology.",
                "tool_name": "Technology News",
                "category": "news_tools",
                "keywords": ["tech news", "technology news", "ai news", "software news", "startup news",
                             "cybersecurity news", "mobile tech", "hardware news"],
                "navigation_category": "News & Events Tools",
                "navigation_tool": "Technology News",
                "tool_description": "Latest technology and tech industry updates"
            },
            {
                "content": "News Sentiment Analysis analyzes the emotional tone of news articles and content, providing sentiment scores, confidence levels, and emotional indicators for news text.",
                "tool_name": "News Sentiment Analysis",
                "category": "news_tools",
                "keywords": ["news sentiment", "news analysis", "sentiment analysis", "news tone", "emotional analysis",
                             "news mood"],
                "navigation_category": "News & Events Tools",
                "navigation_tool": "News Sentiment Analysis",
                "tool_description": "Analyze emotional tone and sentiment in news content"
            },
            {
                "content": "Keyword News Search allows searching for news articles using specific keywords with advanced filters for time period, language, source type, and sorting options.",
                "tool_name": "Keyword News Search",
                "category": "news_tools",
                "keywords": ["search news", "news search", "keyword search", "find news", "news by keyword",
                             "search articles"],
                "navigation_category": "News & Events Tools",
                "navigation_tool": "Keyword News Search",
                "tool_description": "Search news articles using specific keywords"
            },
            {
                "content": "Weather Updates provides current weather conditions, forecasts, and weather alerts for any location worldwide with detailed weather information.",
                "tool_name": "Weather Updates",
                "category": "news_tools",
                "keywords": ["weather", "weather forecast", "weather updates", "current weather", "weather alerts",
                             "weather conditions"],
                "navigation_category": "News & Events Tools",
                "navigation_tool": "Weather Updates",
                "tool_description": "Current weather conditions and forecasts"
            },
            {
                "content": "Fact Checker verifies claims and checks facts from news sources, providing verification status, supporting evidence, context, and important caveats for factual accuracy.",
                "tool_name": "Fact Checker",
                "category": "news_tools",
                "keywords": ["fact check", "verify news", "check facts", "fact checker", "verify claims",
                             "news verification", "truth check"],
                "navigation_category": "News & Events Tools",
                "navigation_tool": "Fact Checker",
                "tool_description": "Verify claims and check facts from news sources"
            }
        ]
        knowledge.extend(news_tools)

        # Additional categories with key tools
        other_tools = [
            {
                "content": "Password Generator creates strong, secure passwords with customizable length, character sets (uppercase, lowercase, numbers, symbols), and complexity requirements for enhanced security.",
                "tool_name": "Password Generator",
                "category": "security_tools",
                "keywords": ["password generator", "secure password", "strong password", "generate password",
                             "password security", "random password", "safe password"],
                "navigation_category": "Security/Privacy Tools",
                "navigation_tool": "Password Generator",
                "tool_description": "Generate strong and secure passwords"
            },
            {
                "content": "Code Formatter beautifies and formats code in multiple languages including Python, JavaScript, HTML, CSS, JSON, SQL, and more with proper indentation and syntax highlighting.",
                "tool_name": "Code Formatter",
                "category": "coding_tools",
                "keywords": ["code formatter", "code beautifier", "format code", "syntax highlighting", "python",
                             "javascript", "html", "css", "json", "beautify code"],
                "navigation_category": "Coding Tools",
                "navigation_tool": "Code Formatter",
                "tool_description": "Format and beautify code with syntax highlighting"
            },
            {
                "content": "URL Shortener creates shortened URLs for long web addresses with click tracking, analytics, custom aliases, and QR code generation for easy sharing.",
                "tool_name": "URL Shortener",
                "category": "web_tools",
                "keywords": ["url shortener", "short links", "shorten url", "link shortener", "tiny url", "short link",
                             "url compression"],
                "navigation_category": "Web Developer Tools",
                "navigation_tool": "URL Shortener",
                "tool_description": "Create shortened URLs with tracking capabilities"
            }
        ]
        knowledge.extend(other_tools)

        return knowledge

    def _build_synonyms_map(self) -> Dict[str, List[str]]:
        """Build synonym mappings for better search matching"""
        return {
            "resize": ["scale", "change size", "make bigger", "make smaller", "shrink", "enlarge"],
            "convert": ["change", "transform", "turn into", "switch"],
            "generate": ["create", "make", "produce", "build"],
            "remove": ["delete", "erase", "take out", "eliminate"],
            "edit": ["modify", "change", "update", "fix"],
            "analyze": ["examine", "study", "check", "review"],
            "format": ["style", "organize", "structure", "arrange"],
            "secure": ["safe", "protect", "encrypt", "lock"],
            "count": ["calculate", "measure", "compute"],
            "translate": ["convert language", "change language"],
            "summary": ["summarize", "brief", "overview", "condensed"]
        }

    def search_and_respond(self, query: str) -> Dict[str, Any]:
        """Enhanced search with better matching and specific tool navigation"""
        # Find relevant tools using enhanced search
        relevant_tools = self._enhanced_search(query)

        # Build context for AI response
        context = self._build_context(relevant_tools[:3])

        # Generate intelligent response
        response = self._generate_enhanced_response(query, context, relevant_tools)

        # Determine specific navigation targets
        navigation_targets = self._get_navigation_targets(relevant_tools)

        return {
            "response": response,
            "relevant_tools": relevant_tools,
            "navigation_targets": navigation_targets,
            "can_navigate_directly": len(navigation_targets) > 0
        }

    def _enhanced_search(self, query: str) -> List[Dict[str, Any]]:
        """Enhanced search with synonym matching and better scoring"""
        query_lower = query.lower()
        query_words = re.findall(r'\b\w+\b', query_lower)

        # Expand query with synonyms
        expanded_words = set(query_words)
        for word in query_words:
            if word in self.tool_synonyms:
                expanded_words.update(self.tool_synonyms[word])

        results = []

        for tool in self.knowledge_base:
            score = 0

            # Exact tool name match (highest priority)
            if query_lower in tool["tool_name"].lower():
                score += 50

            # Keyword matching with expanded synonyms
            for keyword in tool["keywords"]:
                for word in expanded_words:
                    if word in keyword.lower():
                        score += 10
                    if keyword.lower() in query_lower:
                        score += 15

            # Content matching
            tool_content_words = set(re.findall(r'\b\w+\b', tool["content"].lower()))
            word_matches = len(expanded_words.intersection(tool_content_words))
            score += word_matches * 5

            # Tool description matching
            if any(word in tool["tool_description"].lower() for word in expanded_words):
                score += 8

            # Category matching
            if any(word in tool["category"] for word in expanded_words):
                score += 3

            if score > 0:
                tool_copy = tool.copy()
                tool_copy["relevance_score"] = score
                results.append(tool_copy)

        # Sort by relevance score
        return sorted(results, key=lambda x: x["relevance_score"], reverse=True)

    def _build_context(self, relevant_tools: List[Dict[str, Any]]) -> str:
        """Build rich context from relevant tools"""
        context_parts = []
        for tool in relevant_tools:
            context_parts.append(
                f"Tool: {tool['tool_name']}\n"
                f"Category: {tool['navigation_category']}\n"
                f"Description: {tool['content']}\n"
                f"Navigation: Go to {tool['navigation_category']}"
                + (f" → {tool['navigation_tool']}" if tool['navigation_tool'] else "") + "\n"
            )
        return "\n".join(context_parts)

    def _generate_enhanced_response(self, query: str, context: str, relevant_tools: List[Dict[str, Any]]) -> str:
        """Generate enhanced AI response with specific tool guidance"""

        prompt = f"""You are an expert assistant for InOneBox, a comprehensive digital toolkit with 500+ professional tools created by Vatsal Varshney.

User Query: {query}

Available Tools and Information:
{context}

Provide a helpful, specific response that:
1. Directly addresses what the user wants to do
2. Recommends the most relevant specific tool(s) 
3. Explains how the tool will help them
4. Gives clear navigation instructions
5. Mentions the creator Vatsal Varshney when appropriate

Be conversational, specific, and actionable. Focus on the exact tools that match their needs.

Response:"""

        try:
            response = ai_client.generate_text(prompt, model="gemini", max_tokens=400)

            # Add creator attribution for relevant queries
            creator_keywords = ["who made", "creator", "author", "vatsal", "portfolio", "about"]
            if any(keyword in query.lower() for keyword in creator_keywords):
                if "vatsal" not in response.lower():
                    response += "\n\n💡 This amazing toolkit was created by Vatsal Varshney! Check out his Portfolio section to learn more about him and connect professionally."

            return response.strip()

        except Exception as e:
            # Enhanced fallback response when AI is unavailable
            if relevant_tools:
                tool_names = [tool['tool_name'] for tool in relevant_tools[:2]]
                category = relevant_tools[0]['navigation_category']

                # Create smart responses based on query type
                if "generate" in query.lower() or "create" in query.lower():
                    return f"🎯 Perfect! I found exactly what you need: **{' and '.join(tool_names)}**. \n\n📍 **How to access:** Go to **{category}** category from the main menu.\n\n✨ This comprehensive toolkit was created by Vatsal Varshney - check out his Portfolio section to learn more!"
                elif "edit" in query.lower() or "modify" in query.lower():
                    return f"🛠️ Great! For editing and modifications, you'll want **{' and '.join(tool_names)}**. \n\n📍 **Navigation:** Click **{category}** in the category dropdown.\n\n💡 Pro tip: This toolkit by Vatsal Varshney has many more tools to explore!"
                else:
                    return f"🔍 Found it! **{' and '.join(tool_names)}** in the **{category}** section will help you perfectly.\n\n📍 **Access:** Select **{category}** from the categories menu.\n\n👨‍💻 Created by Vatsal Varshney - visit Portfolio to connect with him!"

            # Generic helpful response
            greeting_words = ["hi", "hello", "hey", "greetings"]
            if any(word in query.lower() for word in greeting_words):
                return "👋 **Hello! Welcome to InOneBox!** \n\n🛠️ I'm your personal toolkit guide with **500+ professional tools** at your service.\n\n💡 **Try asking me:**\n- 'Show me AI tools'\n- 'I need to edit images'\n- 'Help with data analysis'\n\n👨‍💻 **Created by Vatsal Varshney** - AI/ML Engineer. Check out his Portfolio!"

            return "🚀 **I'm here to help you navigate InOneBox!** \n\n🎯 **Try being more specific about what you want to do:**\n- Generate, create, edit, analyze...\n- Or browse categories to discover amazing features!\n\n✨ This comprehensive toolkit was created by **Vatsal Varshney** - don't forget to explore his Portfolio section!"

    def _get_navigation_targets(self, relevant_tools: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Get specific navigation targets for the most relevant tools"""
        targets = []
        for tool in relevant_tools[:3]:  # Top 3 most relevant
            if tool.get("navigation_tool"):
                targets.append({
                    "category": tool["navigation_category"],
                    "tool": tool["navigation_tool"],
                    "description": tool["tool_description"]
                })
            elif tool["navigation_category"] != "Dashboard":
                targets.append({
                    "category": tool["navigation_category"],
                    "tool": None,
                    "description": f"Browse {tool['navigation_category']} category"
                })
        return targets

    def search_web_with_gemini(self, query: str) -> Dict[str, Any]:
        """Search the web using Gemini AI for current information"""
        try:
            cache_key = f"gemini_web_{query}"
            if cache_key in self.search_cache:
                return self.search_cache[cache_key]

            # Create a web search prompt for Gemini
            web_search_prompt = f"""
            Please search for current, factual information about: {query}

            Provide a comprehensive answer that includes:
            1. Key facts and current information
            2. Recent developments or updates if applicable
            3. Relevant statistics or data
            4. Important context or background

            Focus on accuracy and include the most recent information available. 
            If you don't have current information, please indicate that.

            Query: {query}
            """

            # Use AI client to get web-informed response from Gemini
            response = ai_client.generate_text(web_search_prompt, model="gemini", max_tokens=800)

            result = {
                'query': query,
                'response': response,
                'source': 'Gemini Web Search',
                'timestamp': int(time.time())
            }

            # Cache the result
            self.search_cache[cache_key] = result
            return result

        except Exception as e:
            return {
                'query': query,
                'response': f"I'm unable to search for current information about '{query}' right now. Please try again later.",
                'source': 'Error',
                'error': str(e)
            }

    def search_web(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Search the web using DuckDuckGo API (fallback method)"""
        try:
            cache_key = f"{query}_{max_results}"
            if cache_key in self.search_cache:
                return self.search_cache[cache_key]

            # DuckDuckGo instant answer API
            encoded_query = urllib.parse.quote_plus(query)
            url = f"https://api.duckduckgo.com/?q={encoded_query}&format=json&no_redirect=1&no_html=1&skip_disambig=1"

            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())

            results = []

            # Get instant answer
            if data.get('Abstract'):
                results.append({
                    'title': data.get('AbstractText', 'Instant Answer'),
                    'snippet': data.get('Abstract', ''),
                    'url': data.get('AbstractURL', ''),
                    'source': 'DuckDuckGo Answer'
                })

            # Get related topics
            for topic in data.get('RelatedTopics', [])[:max_results - len(results)]:
                if isinstance(topic, dict) and topic.get('Text'):
                    results.append({
                        'title': topic.get('Text', '')[:100] + '...',
                        'snippet': topic.get('Text', ''),
                        'url': topic.get('FirstURL', ''),
                        'source': 'Related Topic'
                    })

            self.search_cache[cache_key] = results
            return results[:max_results]

        except Exception as e:
            return [{'title': f'Search results for: {query}',
                     'snippet': f'Web search for "{query}" - real-time results would appear here.',
                     'url': '#', 'source': 'Demo'}]

    def determine_search_strategy(self, query: str) -> str:
        """Determine whether to use web search, local knowledge, news search, or hybrid approach"""
        # News-specific indicators
        news_indicators = ['news', 'breaking', 'headlines', 'trending', 'current events',
                           'latest updates', 'what happened', 'recent developments', 'today news',
                           'breaking news', 'news about', 'current news', 'latest news']

        # Web search indicators
        web_indicators = ['current', 'latest', 'recent', 'today', 'now', 'this week', 'this month',
                          'what is happening', '2024', '2025', 'price', 'weather', 'update', 'status']

        # Local knowledge indicators
        local_indicators = ['how to', 'tool', 'inonebox', 'vatsal', 'navigate', 'find tool',
                            'show me', 'help with', 'what tools', 'category', 'features']

        query_lower = query.lower()

        # Check for news-specific queries first
        news_score = sum(1 for indicator in news_indicators if indicator in query_lower)
        web_score = sum(1 for indicator in web_indicators if indicator in query_lower)
        local_score = sum(1 for indicator in local_indicators if indicator in query_lower)

        # Determine strategy based on scores
        if news_score > 0 and news_score >= web_score:
            return 'news'
        elif web_score > local_score:
            return 'web'
        elif local_score > web_score:
            return 'local'
        else:
            return 'hybrid'

    def search_news_with_gemini(self, query: str) -> Dict[str, Any]:
        """Search for real-time news using Gemini AI"""
        try:
            cache_key = f"news_search_{query}"
            if cache_key in self.search_cache:
                return self.search_cache[cache_key]

            # Create news-specific search prompt
            news_search_prompt = f"""
            Please search for and provide current real-time news about: {query}

            Focus on:
            1. Latest breaking news and headlines
            2. Recent developments and updates
            3. Current events and trending stories
            4. Key facts, dates, and specific details
            5. Recent announcements or changes

            Provide structured information with:
            - Clear headlines
            - Key facts and details
            - Recent developments
            - Current status or ongoing situation

            Prioritize accuracy and recency. Only include information you are confident is current.
            Query: {query}
            """

            response = ai_client.generate_text(news_search_prompt, model="gemini", max_tokens=1000)

            result = {
                'query': query,
                'response': response,
                'source': 'Gemini News Search',
                'timestamp': int(time.time()),
                'type': 'news'
            }

            # Cache the result for 5 minutes
            self.search_cache[cache_key] = result
            return result

        except Exception as e:
            return {
                'query': query,
                'response': f"I'm unable to fetch current news about '{query}' right now. Please try again later.",
                'source': 'Error',
                'error': str(e),
                'type': 'news'
            }

    def search_and_respond_enhanced(self, query: str) -> Dict[str, Any]:
        """Enhanced search with web search and news integration"""
        strategy = self.determine_search_strategy(query)

        # Get local results
        local_results = self._enhanced_search(query) if strategy in ['local', 'hybrid'] else []

        # Get web/news results based on strategy
        web_results = []
        news_result = None

        if strategy == 'news':
            # Prioritize news search for news-related queries
            news_result = self.search_news_with_gemini(query)
            if news_result and news_result.get('response'):
                web_results = [news_result]
        elif strategy in ['web', 'hybrid']:
            # Use general web search for other queries
            web_result = self.search_web_with_gemini(query)
            if web_result and web_result.get('response'):
                web_results = [web_result]

        # Build combined context
        local_context = self._build_context(local_results[:2]) if local_results else ""

        # Generate enhanced response with news awareness
        response = self._generate_news_enhanced_response(query, local_context, web_results, local_results, strategy)

        return {
            "response": response,
            "relevant_tools": local_results,
            "web_results": web_results,
            "news_result": news_result,
            "search_strategy": strategy,
            "navigation_targets": self._get_navigation_targets(local_results)
        }

    def _generate_news_enhanced_response(self, query: str, local_context: str,
                                         web_results: List[Dict], local_results: List[Dict], strategy: str) -> str:
        """Generate response combining news search and local knowledge"""
        news_context = ""
        if web_results:
            news_context = "📰 **Current News & Updates:**\n"
            for result in web_results[:2]:
                if 'response' in result:
                    # News search result from Gemini
                    content = result['response']
                    if strategy == 'news':
                        news_context += f"🔥 **Breaking News:** {content[:400]}...\n\n"
                    else:
                        news_context += f"📊 **Current Information:** {content[:300]}...\n\n"
                else:
                    # Fallback format
                    news_context += f"📄 **{result.get('title', 'News Update')}:** {result.get('snippet', '')[:200]}...\n\n"

        # Build the prompt without nested f-strings
        local_knowledge_section = f"🛠️ **Local InOneBox Knowledge:**\n{local_context}\n" if local_context else ""
        strategy_section = f"🎯 **Strategy Used:** {strategy.title()} search approach" if strategy else ""

        prompt = f"""You are an enhanced AI assistant with access to both local InOneBox knowledge and real-time news/web information.

User Query: {query}

{local_knowledge_section}

{news_context if news_context else ""}

Provide a comprehensive response that:
1. **Directly addresses the user's question**
2. **Combines news/current information with relevant tools when applicable**
3. **Clearly indicates when using real-time news vs local knowledge**
4. **Provides actionable guidance and tool recommendations**
5. **Uses engaging formatting with emojis and clear structure**

{strategy_section}

Response:"""

        try:
            return ai_client.generate_text(prompt, model="gemini", max_tokens=600).strip()
        except:
            return f"📰 Based on your query '{query}', I found relevant information from both news sources and local tools. The search used {strategy} approach to provide you with the most current and relevant information available."

    def _generate_web_enhanced_response(self, query: str, local_context: str,
                                        web_results: List[Dict], local_results: List[Dict]) -> str:
        """Generate response combining Gemini web search and local knowledge"""
        web_context = ""
        if web_results:
            web_context = "Current web information:\n"
            for result in web_results[:2]:
                if 'response' in result:
                    # Gemini web search result
                    web_context += f"• {result['response'][:300]}...\n"
                else:
                    # Fallback format
                    web_context += f"• {result.get('title', 'Web Result')}: {result.get('snippet', '')[:150]}...\n"

        prompt = f"""You are an enhanced AI assistant with access to both local InOneBox knowledge and real-time web information.

User Query: {query}

{f"Local InOneBox Knowledge: {local_context}" if local_context else ""}

{web_context if web_context else ""}

Provide a comprehensive response that:
1. Directly addresses the user's question
2. Uses the most relevant information (prioritizing local tools for InOneBox queries)
3. Clearly indicates when using web information vs local knowledge
4. Provides actionable guidance and tool recommendations

Response:"""

        try:
            return ai_client.generate_text(prompt, model="gemini", max_tokens=500).strip()
        except:
            return f"Based on your query '{query}', I found relevant information from both local tools and web sources. Please try being more specific for better results."


# Global enhanced RAG instance
enhanced_rag = EnhancedRAG()