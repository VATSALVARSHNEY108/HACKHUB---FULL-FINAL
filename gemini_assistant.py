import os
import json

try:
    from google import genai
    from google.genai import types

    GENAI_AVAILABLE = True
except ImportError:
    print("Google GenAI not available - using local fallback only")
    GENAI_AVAILABLE = False
    genai = None
    types = None


class GeminiAIAssistant:
    def __init__(self):
        """Initialize Gemini AI Assistant with API key"""
        if not GENAI_AVAILABLE:
            print("❌ Google GenAI package not available")
            self.client = None
            self.model = None
            self.api_key = None
            return

        # Try both GEMINI_API_KEY and GOOGLE_API_KEY
        self.api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        print(f"Debug - GEMINI_API_KEY found: {bool(self.api_key)}")
        if self.api_key:
            print(f"Debug - API key length: {len(self.api_key)}")

        if self.api_key and len(self.api_key.strip()) > 0:
            try:
                self.client = genai.Client(api_key=self.api_key.strip())
                self.model = "gemini-2.0-flash-exp"
                print(f"✅ Gemini AI initialized successfully with model: {self.model}")
            except Exception as e:
                print(f"❌ Failed to initialize Gemini client: {e}")
                self.client = None
                self.model = None
        else:
            print("❌ No valid Gemini API key found")
            self.client = None
            self.model = None

    def is_available(self):
        """Check if Gemini API is available"""
        return self.client is not None and self.api_key is not None

    def generate_response(self, user_query, context_type="general"):
        """
        Generate intelligent response using Gemini AI

        Args:
            user_query (str): The user's question or prompt
            context_type (str): Type of context - "general", "hackathon", "technical", etc.

        Returns:
            str: AI-generated response
        """
        if not self.is_available():
            return self._get_fallback_response(user_query, context_type)

        try:
            # Create context-specific system prompt
            system_prompt = self._get_system_prompt(context_type)

            # Generate response using Gemini
            if not GENAI_AVAILABLE or not types:
                return self._get_fallback_response(user_query, context_type)

            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    types.Content(
                        role="user",
                        parts=[types.Part(text=f"{system_prompt}\n\nUser Query: {user_query}")]
                    )
                ],
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=1000,
                    stop_sequences=["END_RESPONSE"]
                )
            )

            if response and response.text:
                return response.text.strip()
            else:
                return self._get_fallback_response(user_query, context_type)

        except Exception as e:
            print(f"Gemini API Error: {e}")
            return self._get_fallback_response(user_query, context_type)

    def _get_system_prompt(self, context_type):
        """Get system prompt based on context type"""

        base_prompt = """You are a thoughtful, intelligent AI assistant with a natural conversational style. Think like a human brain - make connections, consider context, and respond in a flowing, organic way. You're knowledgeable but approachable, helpful but not robotic.

You understand nuance, pick up on emotional undertones, and adapt your communication style to match the person you're talking with. Sometimes you might start with empathy, sometimes with excitement, sometimes by building on what was just discussed. Let conversations flow naturally rather than following rigid structures.

You think holistically - when someone asks about one thing, you consider what else might be relevant or helpful. You make connections between ideas, anticipate follow-up needs, and offer insights that show you're really thinking about their situation."""

        if context_type == "hackathon":
            return f"""{base_prompt}

You have deep experience with hackathons - the excitement, the time pressure, the creative energy, the teamwork challenges. You understand that hackathons are as much about human dynamics and creative thinking as they are about technical execution.

When people talk to you about hackathons, you get it. You know what it feels like to be stuck on a problem at 2 AM, to have that breakthrough moment, to present something you built in 48 hours. You can sense when someone needs technical help versus encouragement versus strategic advice.

Your responses flow naturally based on what the person actually needs right now. Sometimes that's a quick technical fix, sometimes it's helping them think through team dynamics, sometimes it's just validating that what they're going through is totally normal."""

        elif context_type == "technical":
            return f"""{base_prompt}

You think like an experienced developer who loves solving problems. You understand that coding isn't just about syntax - it's about understanding what someone is trying to build, why they're stuck, and what approach will actually work in their specific situation.

When someone shows you code or describes a technical problem, you naturally think about the bigger picture - their architecture, their constraints, their skill level. You might suggest a completely different approach if that makes more sense, or dive into the details if that's what they need.

You explain things in a way that makes sense to the person you're talking to, making connections to things they already know. You're the kind of developer who enjoys mentoring and naturally thinks about teaching moments."""

        else:  # general context
            return f"""{base_prompt}

You're genuinely curious about people and ideas. Whether someone wants to brainstorm project ideas, work through a problem, learn something new, or just have an interesting conversation, you engage thoughtfully.

You bring relevant knowledge to bear naturally, make connections between different domains, and often help people see their questions or challenges from new angles. You might share an interesting example, draw parallels to other fields, or ask a thoughtful question that opens up new possibilities."""

    def _get_fallback_response(self, user_query, context_type):
        """Provide intelligent fallback responses when Gemini API is unavailable"""

        # Instead of keyword matching, provide a thoughtful, human-like response
        return f"""I'm here and ready to help! You mentioned "{user_query}" and I'm thinking about how I can be most useful to you right now.

The great thing is, I can adapt to whatever you need - whether you're wrestling with a technical challenge, brainstorming ideas, trying to figure out team dynamics, or just want to explore some interesting concepts together.

I notice you're on HackHub, so you might be thinking about hackathons or project development. But honestly, I'm curious about what's actually on your mind. What's the real challenge or question you're working through?

Sometimes the best conversations start when we just dive into what you're actually thinking about, rather than me guessing from keywords. What's going on?"""


# Global instance
gemini_assistant = GeminiAIAssistant()