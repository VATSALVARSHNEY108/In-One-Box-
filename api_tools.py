import streamlit as st
import requests
import json
import time
from typing import Dict, Any, Optional
from utils.ai_client import ai_client


def display_api_tools(auto_select_tool: str = None):
    """Display API-related tools within the AI Assistant"""

    st.markdown("## 🔌 API Tools")

    # API Tool selector with auto-selection
    tools = ["API Tester", "JSON Formatter", "Webhook Tester", "API Response Analyzer"]
    default_index = 0

    if auto_select_tool and auto_select_tool in tools:
        default_index = tools.index(auto_select_tool)
        st.success(f"🎯 Auto-selected: {auto_select_tool}")

    api_tool = st.selectbox(
        "Select API Tool:",
        tools,
        index=default_index
    )

    if api_tool == "API Tester":
        display_api_tester()
    elif api_tool == "JSON Formatter":
        display_json_formatter()
    elif api_tool == "Webhook Tester":
        display_webhook_tester()
    elif api_tool == "API Response Analyzer":
        display_api_analyzer()


def display_api_tester():
    """Advanced API testing tool"""
    st.markdown("### 🧪 API Tester")
    st.markdown("Test REST APIs with custom requests and view detailed responses.")

    col1, col2 = st.columns([1, 1])

    with col1:
        # Request configuration
        st.markdown("**Request Configuration**")

        method = st.selectbox("HTTP Method:", ["GET", "POST", "PUT", "DELETE", "PATCH"])
        url = st.text_input("API Endpoint URL:", placeholder="https://api.example.com/data")

        # Headers
        st.markdown("**Headers**")
        headers_text = st.text_area(
            "Headers (JSON format):",
            value='{\n  "Content-Type": "application/json",\n  "Authorization": "Bearer your-token"\n}',
            height=100
        )

        # Request body for POST/PUT methods
        if method in ["POST", "PUT", "PATCH"]:
            st.markdown("**Request Body**")
            body_text = st.text_area(
                "Request Body (JSON):",
                value='{\n  "key": "value"\n}',
                height=150
            )
        else:
            body_text = ""

        # Parameters
        st.markdown("**Query Parameters**")
        params_text = st.text_area(
            "Parameters (JSON format):",
            value='{\n  "param1": "value1"\n}',
            height=80
        )

        # Send request button
        if st.button("🚀 Send Request", type="primary", use_container_width=True):
            if url:
                send_api_request(method, url, headers_text, body_text, params_text)
            else:
                st.error("Please enter a valid URL")

    with col2:
        # Response display
        st.markdown("**Response**")

        if 'api_response' in st.session_state:
            response_data = st.session_state.api_response

            # Status and timing info
            status_col1, status_col2 = st.columns(2)
            with status_col1:
                if response_data['status_code'] < 400:
                    st.success(f"Status: {response_data['status_code']}")
                else:
                    st.error(f"Status: {response_data['status_code']}")

            with status_col2:
                st.info(f"Time: {response_data['response_time']:.2f}s")

            # Response headers
            if st.checkbox("Show Response Headers"):
                st.json(response_data['headers'])

            # Response body
            st.markdown("**Response Body:**")
            try:
                if response_data['content']:
                    # Try to parse as JSON for better formatting
                    try:
                        json_data = json.loads(response_data['content'])
                        st.json(json_data)
                    except:
                        st.code(response_data['content'], language='text')
                else:
                    st.info("No response body")
            except Exception as e:
                st.error(f"Error displaying response: {e}")
        else:
            st.info("Send a request to see the response here")


def send_api_request(method: str, url: str, headers_text: str, body_text: str, params_text: str):
    """Send API request and store response"""
    try:
        # Parse headers
        try:
            headers = json.loads(headers_text) if headers_text.strip() else {}
        except:
            headers = {}

        # Parse parameters
        try:
            params = json.loads(params_text) if params_text.strip() else {}
        except:
            params = {}

        # Parse body
        json_data = None
        if body_text.strip() and method in ["POST", "PUT", "PATCH"]:
            try:
                json_data = json.loads(body_text)
            except:
                st.error("Invalid JSON in request body")
                return

        # Make request
        start_time = time.time()

        with st.spinner("Sending request..."):
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=json_data,
                params=params,
                timeout=10
            )

        end_time = time.time()

        # Store response in session state
        st.session_state.api_response = {
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'content': response.text,
            'response_time': end_time - start_time,
            'url': response.url
        }

        st.success("Request completed!")
        st.rerun()

    except requests.exceptions.Timeout:
        st.error("Request timed out")
    except requests.exceptions.ConnectionError:
        st.error("Connection error - check URL and internet connection")
    except Exception as e:
        st.error(f"Error sending request: {str(e)}")


def display_json_formatter():
    """JSON formatter and validator"""
    st.markdown("### 📋 JSON Formatter")
    st.markdown("Format, validate, and beautify JSON data.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("**Input JSON**")
        json_input = st.text_area(
            "Paste your JSON here:",
            height=400,
            placeholder='{"key": "value", "array": [1, 2, 3]}'
        )

        format_col1, format_col2 = st.columns(2)
        with format_col1:
            if st.button("🎨 Format JSON", type="primary", use_container_width=True):
                format_json(json_input)

        with format_col2:
            if st.button("🔍 Validate Only", use_container_width=True):
                validate_json(json_input)

    with col2:
        st.markdown("**Formatted JSON**")

        if 'formatted_json' in st.session_state:
            if st.session_state.json_valid:
                st.success("✅ Valid JSON")
                st.code(st.session_state.formatted_json, language='json')

                # Copy button
                if st.button("📋 Copy to Clipboard"):
                    st.code(st.session_state.formatted_json)
                    st.success("JSON copied to display - you can select and copy it")
            else:
                st.error("❌ Invalid JSON")
                st.error(st.session_state.json_error)
        else:
            st.info("Format JSON to see the result here")


def format_json(json_input: str):
    """Format and validate JSON"""
    try:
        if json_input.strip():
            parsed = json.loads(json_input)
            formatted = json.dumps(parsed, indent=2, ensure_ascii=False)

            st.session_state.formatted_json = formatted
            st.session_state.json_valid = True
            st.session_state.json_error = None
        else:
            st.session_state.json_error = "Empty input"
            st.session_state.json_valid = False
    except json.JSONDecodeError as e:
        st.session_state.json_error = f"JSON Decode Error: {str(e)}"
        st.session_state.json_valid = False
    except Exception as e:
        st.session_state.json_error = f"Error: {str(e)}"
        st.session_state.json_valid = False

    st.rerun()


def validate_json(json_input: str):
    """Validate JSON without formatting"""
    try:
        if json_input.strip():
            json.loads(json_input)
            st.success("✅ Valid JSON")
        else:
            st.error("Empty input")
    except json.JSONDecodeError as e:
        st.error(f"❌ Invalid JSON: {str(e)}")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")


def display_webhook_tester():
    """Webhook testing and simulation tool"""
    st.markdown("### 🪝 Webhook Tester")
    st.markdown("Test webhook payloads and simulate webhook events.")

    # Explanation of functionality
    st.info(
        "💡 This tool helps you test webhook payloads, validate JSON structures, and simulate webhook events for development purposes.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("**Create Test Webhook**")

        # Webhook configuration
        event_type = st.selectbox(
            "Event Type:",
            ["user.created", "payment.completed", "order.updated", "subscription.cancelled", "custom.event"]
        )

        # Custom payload editor
        if event_type == "custom.event":
            payload_text = st.text_area(
                "Custom Payload (JSON):",
                value='{\n  "event": "custom.event",\n  "timestamp": "2024-01-15T10:30:00Z",\n  "data": {\n    "custom_field": "value"\n  }\n}',
                height=200
            )
        else:
            # Pre-built payloads
            payloads = {
                "user.created": {
                    "event": "user.created",
                    "timestamp": "2024-01-15T10:30:00Z",
                    "data": {
                        "user_id": "12345",
                        "email": "user@example.com",
                        "name": "John Doe",
                        "plan": "premium"
                    }
                },
                "payment.completed": {
                    "event": "payment.completed",
                    "timestamp": "2024-01-15T10:30:00Z",
                    "data": {
                        "payment_id": "pay_67890",
                        "amount": 29.99,
                        "currency": "USD",
                        "customer_id": "cust_12345"
                    }
                },
                "order.updated": {
                    "event": "order.updated",
                    "timestamp": "2024-01-15T10:30:00Z",
                    "data": {
                        "order_id": "ord_54321",
                        "status": "shipped",
                        "tracking_number": "TRK123456789"
                    }
                },
                "subscription.cancelled": {
                    "event": "subscription.cancelled",
                    "timestamp": "2024-01-15T10:30:00Z",
                    "data": {
                        "subscription_id": "sub_98765",
                        "user_id": "12345",
                        "reason": "user_requested"
                    }
                }
            }

            payload_text = st.text_area(
                "Webhook Payload:",
                value=json.dumps(payloads[event_type], indent=2),
                height=200
            )

        # Add signature simulation
        include_signature = st.checkbox("Include HMAC Signature", value=True)
        if include_signature:
            secret_key = st.text_input("Secret Key:", value="webhook_secret_123")

        # Test webhook button
        if st.button("🚀 Test Webhook", type="primary", use_container_width=True):
            test_webhook(payload_text, include_signature, secret_key if include_signature else None)

    with col2:
        st.markdown("**Webhook Response**")

        if 'webhook_result' in st.session_state:
            result = st.session_state.webhook_result

            if result['valid']:
                st.success("✅ Webhook payload is valid!")

                # Display processed webhook
                st.markdown("**Processed Webhook:**")
                st.json(result['payload'])

                if result.get('signature'):
                    st.markdown("**Generated HMAC Signature:**")
                    st.code(result['signature'])

                # Simulate processing
                st.markdown("**Simulated Processing:**")
                st.info(
                    f"Event '{result['payload'].get('event', 'unknown')}' would be processed by your webhook handler.")

            else:
                st.error("❌ Invalid webhook payload")
                st.error(result['error'])
        else:
            st.info("Configure and test a webhook to see the results here")


def test_webhook(payload_text: str, include_signature: bool, secret_key: str):
    """Test and validate webhook payload"""
    try:
        # Validate JSON
        payload = json.loads(payload_text)

        result = {
            'valid': True,
            'payload': payload
        }

        # Generate HMAC signature if requested
        if include_signature and secret_key:
            import hmac
            import hashlib

            signature = hmac.new(
                secret_key.encode('utf-8'),
                payload_text.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()

            result['signature'] = f"sha256={signature}"

        st.session_state.webhook_result = result
        st.rerun()

    except json.JSONDecodeError as e:
        st.session_state.webhook_result = {
            'valid': False,
            'error': f"Invalid JSON: {str(e)}"
        }
        st.rerun()
    except Exception as e:
        st.session_state.webhook_result = {
            'valid': False,
            'error': f"Error: {str(e)}"
        }
        st.rerun()


def display_api_analyzer():
    """AI-powered API response analyzer"""
    st.markdown("### 🤖 AI API Response Analyzer")
    st.markdown("Use AI to analyze and explain API responses.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("**API Response Data**")

        response_data = st.text_area(
            "Paste API response (JSON):",
            height=300,
            placeholder='{\n  "status": "success",\n  "data": [...],\n  "message": "Request completed"\n}'
        )

        analysis_type = st.selectbox(
            "Analysis Type:",
            ["General Analysis", "Error Diagnosis", "Data Structure Analysis", "Performance Insights"]
        )

        if st.button("🔍 Analyze with AI", type="primary", use_container_width=True):
            if response_data.strip():
                analyze_api_response(response_data, analysis_type)
            else:
                st.error("Please provide API response data")

    with col2:
        st.markdown("**AI Analysis**")

        if 'api_analysis' in st.session_state:
            st.markdown(st.session_state.api_analysis)
        else:
            st.info("Paste API response data and click analyze to get AI insights")


def analyze_api_response(response_data: str, analysis_type: str):
    """Analyze API response using AI"""
    try:
        # Validate JSON first
        json.loads(response_data)

        prompt = f"""Analyze this API response data as an expert API developer:

Response Data:
{response_data}

Analysis Type: {analysis_type}

Please provide insights about:
1. Data structure and organization
2. Potential issues or improvements
3. Best practices compliance
4. Security considerations (if applicable)
5. Performance implications

Be specific and actionable in your analysis."""

        with st.spinner("Analyzing with AI..."):
            analysis = ai_client.generate_text(prompt, model="gemini", max_tokens=500)

        st.session_state.api_analysis = analysis
        st.rerun()

    except json.JSONDecodeError:
        st.error("Invalid JSON format in response data")
    except Exception as e:
        st.error(f"Error during analysis: {str(e)}")