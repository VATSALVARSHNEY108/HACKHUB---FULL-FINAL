import json
import os
import random
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from gemini_assistant import gemini_assistant


class ConversationContext:
    """Manages conversation context and memory"""

    def __init__(self):
        self.conversation_history = []
        self.user_preferences = {}
        self.current_topic = None
        self.last_interaction = None
        self.session_data = {}

    def add_message(self, user_message: str, ai_response: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'user': user_message,
            'ai': ai_response
        })
        self.last_interaction = datetime.now()

        # Keep only last 10 exchanges to prevent memory bloat
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]

    def get_context_summary(self) -> str:
        """Generate a summary of recent conversation context"""
        if not self.conversation_history:
            return "Starting fresh conversation"

        recent_topics = []
        for exchange in self.conversation_history[-3:]:
            recent_topics.append(exchange['user'][:50] + "...")

        return f"Recent topics: {', '.join(recent_topics)}"


class IntentRecognizer:
    """Advanced intent recognition for better conversation flow"""

    INTENT_PATTERNS = {
        'greeting': [
            r'\b(hi|hello|hey|greetings|good morning|good afternoon)\b',
            r'^(hi|hello|hey)\s*[!.]*$'
        ],
        'project_help': [
            r'\b(project|idea|build|create|develop|app|website|application)\b',
            r'\b(what should I|what can I|ideas for)\b.*\b(build|create|make)\b'
        ],
        'team_formation': [
            r'\b(team|teammate|partner|collaborate|group|find people)\b',
            r'\b(looking for|need|want).*\b(team|teammate|partner)\b'
        ],
        'technical_help': [
            r'\b(code|programming|debug|error|bug|technical|development)\b',
            r'\b(python|javascript|react|flask|database|api)\b'
        ],
        'hackathon_strategy': [
            r'\b(hackathon|strategy|plan|timeline|schedule|competition)\b',
            r'\b(how to|tips for|advice for)\b.*\b(hackathon|competition)\b'
        ],
        'presentation_help': [
            r'\b(present|pitch|demo|presentation|showcase|judges)\b',
            r'\b(how to present|pitch tips|demo advice)\b'
        ]
    }

    @classmethod
    def recognize_intent(cls, message: str) -> str:
        """Recognize the primary intent of a user message"""
        message_lower = message.lower()

        # Check each intent pattern
        for intent, patterns in cls.INTENT_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    return intent

        return 'general'


class AdvancedAIAssistant:
    """Enhanced AI Assistant with context awareness and specialized capabilities"""

    def __init__(self):
        self.context = ConversationContext()
        self.intent_recognizer = IntentRecognizer()

        # Enhanced knowledge bases
        self.project_templates = self._load_project_templates()
        self.technical_solutions = self._load_technical_solutions()
        self.team_psychology = self._load_team_psychology_insights()
        self.presentation_frameworks = self._load_presentation_frameworks()

        # Dynamic response generators
        self.response_generators = {
            'greeting': self._generate_greeting_response,
            'project_help': self._generate_project_help,
            'team_formation': self._generate_team_formation_help,
            'technical_help': self._generate_technical_help,
            'hackathon_strategy': self._generate_strategy_help,
            'presentation_help': self._generate_presentation_help,
            'general': self._generate_general_response
        }

    def generate_response(self, user_message: str, context_data: Optional[Dict] = None) -> str:
        """Generate intelligent, context-aware response"""

        # Update context with new information
        if context_data:
            self.context.session_data.update(context_data)

        # Recognize intent
        intent = self.intent_recognizer.recognize_intent(user_message)

        # Try Gemini first for more sophisticated responses
        try:
            if gemini_assistant.is_available():
                enhanced_prompt = self._create_enhanced_prompt(user_message, intent)
                gemini_response = gemini_assistant.generate_response(
                    enhanced_prompt,
                    context_type="hackathon"
                )
                if gemini_response and len(gemini_response.strip()) > 50:
                    self.context.add_message(user_message, gemini_response)
                    return gemini_response
        except Exception as e:
            print(f"Gemini error: {e}")

        # Generate local intelligent response
        response = self.response_generators[intent](user_message, intent)
        self.context.add_message(user_message, response)
        return response

    def _create_enhanced_prompt(self, user_message: str, intent: str) -> str:
        """Create an enhanced prompt with context for Gemini"""
        context_summary = self.context.get_context_summary()

        enhanced_prompt = f"""
Context: You're an expert hackathon mentor with deep experience in technology, team dynamics, and competition strategy.

Conversation Context: {context_summary}

User's Intent: {intent}

Session Data: {json.dumps(self.context.session_data, indent=2)}

User Message: "{user_message}"

Please provide a thoughtful, actionable response that:
1. Acknowledges the conversation context
2. Addresses their specific intent
3. Provides concrete, implementable advice
4. Maintains an encouraging, mentoring tone
5. Asks relevant follow-up questions when appropriate
"""
        return enhanced_prompt

    def _generate_greeting_response(self, message: str, intent: str) -> str:
        """Generate personalized greeting responses"""
        time_of_day = self._get_time_greeting()

        if self.context.conversation_history:
            return f"{time_of_day}! Good to see you back. I remember we were discussing {self.context.current_topic or 'hackathon planning'}. What's on your mind now?"
        else:
            greetings = [
                f"{time_of_day}! I'm excited to help you with whatever hackathon challenge you're tackling. Whether it's team formation, technical hurdles, or strategic planning - I'm here to think through it with you.",
                f"{time_of_day}! There's something energizing about hackathon conversations. I love diving into the creative and technical challenges. What aspect of your project or competition are you working on?",
                f"{time_of_day}! Ready to tackle some interesting problems together? I specialize in hackathon strategy, team dynamics, and technical problem-solving. What's your current challenge or curiosity?"
            ]
            return random.choice(greetings)

    def _generate_project_help(self, message: str, intent: str) -> str:
        """Generate intelligent project suggestions and guidance"""

        # Extract keywords for better recommendations
        keywords = self._extract_keywords(message)
        tech_mentions = self._extract_technology_mentions(message)

        response = "Let me help you brainstorm some compelling project ideas! "

        # Provide targeted suggestions based on mentioned technologies
        if tech_mentions:
            tech_focused_ideas = self._get_tech_focused_ideas(tech_mentions)
            response += f"\n\nSince you mentioned {', '.join(tech_mentions)}, here are some targeted ideas:\n\n"
            for i, idea in enumerate(tech_focused_ideas[:3], 1):
                response += f"{i}. **{idea['title']}**: {idea['description']}\n"
                response += f"   *Tech stack: {', '.join(idea['tech_stack'])}*\n\n"

        # Add general project framework advice
        response += "\n**Project Selection Framework:**\n"
        response += "• Choose problems you personally relate to - passion drives innovation\n"
        response += "• Aim for 80% familiar tech, 20% new tech - manageable learning curve\n"
        response += "• Think about the 'wow factor' for demos - what will impress judges?\n"
        response += "• Consider implementation feasibility in your time constraint\n\n"

        response += "What specific domain or technology interests you most? I can dive deeper into targeted recommendations."

        return response

    def _generate_team_formation_help(self, message: str, intent: str) -> str:
        """Advanced team formation guidance with psychology insights"""

        response = "Team formation is both an art and a science! Let me share some insights based on what actually works:\n\n"

        response += "**The Psychology of Great Teams:**\n"
        response += "• **Diverse thinking styles** matter more than similar skill levels\n"
        response += "• **Communication compatibility** beats perfect technical alignment\n"
        response += "• **Complementary work styles** create productive tension\n"
        response += "• **Shared excitement** about the problem domain drives success\n\n"

        response += "**Practical Team Building Strategy:**\n"
        response += "1. **Start with the problem** - find people passionate about similar challenges\n"
        response += "2. **Test chemistry quickly** - do a 15-minute brainstorming exercise together\n"
        response += "3. **Define roles early** - who's the decider when you're stuck?\n"
        response += "4. **Plan for conflict** - agree on how you'll handle disagreements\n\n"

        # Add personalized advice if we have session data
        if 'user_role' in self.context.session_data:
            role = self.context.session_data['user_role']
            response += f"**For {role}s specifically:**\n"
            response += self._get_role_specific_team_advice(role) + "\n\n"

        response += "What's your role and experience level? I can give you more targeted team-building advice."

        return response

    def _generate_technical_help(self, message: str, intent: str) -> str:
        """Provide intelligent technical guidance and problem-solving"""

        # Detect specific technical areas mentioned
        tech_areas = self._detect_technical_areas(message)

        response = "I love tackling technical challenges! Let me help you think through this systematically.\n\n"

        if 'debugging' in message.lower() or 'error' in message.lower():
            response += "**Debugging Strategy:**\n"
            response += "• **Reproduce consistently** - make the error happen reliably\n"
            response += "• **Isolate the problem** - comment out code until it works\n"
            response += "• **Check the obvious first** - syntax, imports, environment variables\n"
            response += "• **Read error messages carefully** - they're usually more helpful than they seem\n\n"

        if tech_areas:
            response += f"**For {', '.join(tech_areas)} specifically:**\n"
            for area in tech_areas:
                response += f"• {self._get_tech_specific_advice(area)}\n"
            response += "\n"

        response += "**General Technical Tips:**\n"
        response += "• Start with the simplest possible version that works\n"
        response += "• Use tools and libraries you're comfortable with\n"
        response += "• Test frequently on different devices/browsers\n"
        response += "• Have a backup plan if your main approach fails\n\n"

        response += "What specific technical challenge are you facing? Share some code or error messages and I can give more targeted help."

        return response

    def _generate_strategy_help(self, message: str, intent: str) -> str:
        """Provide comprehensive hackathon strategy guidance"""

        response = "Hackathon strategy is about smart execution under pressure. Here's your winning framework:\n\n"

        response += "**The 48-Hour Success Formula:**\n\n"

        response += "**🎯 Hours 0-4: Foundation (Critical!)**\n"
        response += "• Team formation + chemistry test (90 minutes)\n"
        response += "• Problem definition + user validation (60 minutes)\n"
        response += "• Tech stack decision + setup (90 minutes)\n"
        response += "• MVP scope definition + timeline (30 minutes)\n\n"

        response += "**⚡ Hours 4-36: Sprint Development**\n"
        response += "• Core functionality first - no bells and whistles\n"
        response += "• 4-hour development sprints with team check-ins\n"
        response += "• Test on real devices every 6 hours\n"
        response += "• Parallel work: backend + frontend + design\n\n"

        response += "**🎤 Hours 36-48: Demo Preparation**\n"
        response += "• Feature freeze - no new development\n"
        response += "• Create compelling demo narrative\n"
        response += "• Practice presentation 3+ times\n"
        response += "• Prepare for Q&A scenarios\n\n"

        response += "**Mental Game:**\n"
        response += "• Expect setbacks - they're normal and manageable\n"
        response += "• Take breaks - 20 minutes every 3 hours minimum\n"
        response += "• Celebrate small wins - maintain team morale\n"
        response += "• Remember: done is better than perfect\n\n"

        response += "What stage are you at in your hackathon? I can provide more specific guidance based on your current situation."

        return response

    def _generate_presentation_help(self, message: str, intent: str) -> str:
        """Advanced presentation and pitching guidance"""

        response = "Great presentations win hackathons! Here's how to create a compelling pitch:\n\n"

        response += "**The Winning Pitch Structure (3-5 minutes):**\n\n"

        response += "**🔥 Hook (30 seconds)**\n"
        response += "• Start with a relatable problem story\n"
        response += "• Use numbers: '70% of students struggle with...'\n"
        response += "• Ask a thought-provoking question\n\n"

        response += "**💡 Solution (90 seconds)**\n"
        response += "• Show your app solving the exact problem\n"
        response += "• Focus on user experience, not technical features\n"
        response += "• Demonstrate with real data/scenarios\n\n"

        response += "**⚙️ How It Works (60 seconds)**\n"
        response += "• High-level technical approach\n"
        response += "• Highlight innovative aspects\n"
        response += "• Mention scalability if relevant\n\n"

        response += "**📈 Impact & Next Steps (30 seconds)**\n"
        response += "• Quantify potential impact\n"
        response += "• Share concrete next steps\n"
        response += "• End with a memorable call-to-action\n\n"

        response += "**Demo Day Pro Tips:**\n"
        response += "• Practice your demo 5+ times - muscle memory matters\n"
        response += "• Have screenshots as backup if live demo fails\n"
        response += "• Tell a story - judges remember narratives, not features\n"
        response += "• Show personality - passion is contagious\n"
        response += "• Prepare for questions about team, tech choices, and scaling\n\n"

        response += "What aspect of your presentation needs the most work? I can help you refine your pitch!"

        return response

    def _generate_general_response(self, message: str, intent: str) -> str:
        """Generate thoughtful general responses with context awareness"""

        # Analyze message for key concepts
        concepts = self._extract_concepts(message)

        response = "I'm here to help you navigate whatever challenge you're working through! "

        if concepts:
            response += f"I see you're thinking about {', '.join(concepts[:2])}. "

        response += "Whether it's technical problem-solving, team dynamics, creative brainstorming, or strategic planning - I love diving into these kinds of challenges.\n\n"

        # Provide contextual guidance
        if self.context.conversation_history:
            response += "Based on our conversation, I can help you with:\n"
        else:
            response += "I'm particularly good at helping with:\n"

        response += "• **Project ideation** - turning concepts into implementable solutions\n"
        response += "• **Technical guidance** - debugging, architecture, and implementation strategies\n"
        response += "• **Team dynamics** - formation, communication, and collaboration\n"
        response += "• **Competition strategy** - planning, execution, and presentation\n\n"

        response += "What's the specific challenge or question that's on your mind right now?"

        return response

    # Helper methods for enhanced functionality

    def _get_time_greeting(self) -> str:
        """Get appropriate greeting based on time of day"""
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return "Good morning"
        elif 12 <= hour < 18:
            return "Good afternoon"
        elif 18 <= hour < 22:
            return "Good evening"
        else:
            return "Hello"

    def _extract_keywords(self, message: str) -> List[str]:
        """Extract important keywords from message"""
        # Simple keyword extraction - can be enhanced with NLP libraries
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is',
                        'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                        'would', 'could', 'should', 'may', 'might', 'can'}

        words = re.findall(r'\b\w+\b', message.lower())
        keywords = [word for word in words if len(word) > 3 and word not in common_words]
        return keywords[:5]  # Return top 5 keywords

    def _extract_technology_mentions(self, message: str) -> List[str]:
        """Extract mentioned technologies"""
        tech_keywords = ['python', 'javascript', 'react', 'flask', 'django', 'nodejs', 'vue', 'angular', 'mongodb',
                         'postgresql', 'mysql', 'docker', 'kubernetes', 'aws', 'gcp', 'azure', 'tensorflow', 'pytorch',
                         'ml', 'ai', 'blockchain', 'api', 'rest', 'graphql']

        message_lower = message.lower()
        mentioned = [tech for tech in tech_keywords if tech in message_lower]
        return mentioned

    def _detect_technical_areas(self, message: str) -> List[str]:
        """Detect specific technical areas from message"""
        areas = {
            'frontend': ['frontend', 'ui', 'css', 'html', 'react', 'vue', 'angular'],
            'backend': ['backend', 'api', 'server', 'database', 'flask', 'django'],
            'database': ['database', 'sql', 'mongodb', 'postgresql', 'mysql'],
            'deployment': ['deploy', 'hosting', 'aws', 'heroku', 'vercel', 'docker'],
            'mobile': ['mobile', 'android', 'ios', 'react native', 'flutter']
        }

        message_lower = message.lower()
        detected = []

        for area, keywords in areas.items():
            if any(keyword in message_lower for keyword in keywords):
                detected.append(area)

        return detected

    def _extract_concepts(self, message: str) -> List[str]:
        """Extract high-level concepts from message"""
        concepts = {
            'innovation': ['innovation', 'creative', 'novel', 'unique', 'original'],
            'collaboration': ['team', 'collaborate', 'together', 'group', 'partner'],
            'learning': ['learn', 'understand', 'study', 'education', 'tutorial'],
            'problem-solving': ['problem', 'solve', 'challenge', 'fix', 'debug'],
            'strategy': ['strategy', 'plan', 'approach', 'method', 'framework']
        }

        message_lower = message.lower()
        detected = []

        for concept, keywords in concepts.items():
            if any(keyword in message_lower for keyword in keywords):
                detected.append(concept)

        return detected

    def _load_project_templates(self) -> Dict:
        """Load comprehensive project templates"""
        return {
            "web_app": {
                "title": "Full-Stack Web Application",
                "description": "Complete web application with user authentication, database, and API",
                "tech_stack": ["React", "Flask/Django", "PostgreSQL", "Docker"],
                "timeline": "36 hours development + 12 hours polish"
            },
            "mobile_app": {
                "title": "Cross-Platform Mobile App",
                "description": "Mobile application with offline capabilities and cloud sync",
                "tech_stack": ["React Native", "Firebase", "MongoDB"],
                "timeline": "30 hours development + 18 hours testing"
            },
            "ai_solution": {
                "title": "AI-Powered Solution",
                "description": "Machine learning application solving real-world problems",
                "tech_stack": ["Python", "TensorFlow/PyTorch", "Flask API", "React"],
                "timeline": "24 hours ML + 24 hours integration"
            }
        }

    def _load_technical_solutions(self) -> Dict:
        """Load common technical solutions and patterns"""
        return {
            "authentication": "Use JWT tokens with Flask-JWT-Extended or implement OAuth with social providers",
            "database_design": "Start with simple schema, use migrations for changes, index frequently queried fields",
            "api_design": "RESTful design with clear endpoints, proper HTTP status codes, and comprehensive error handling",
            "frontend_state": "Use React hooks for simple state, Context API for shared state, or Redux for complex applications"
        }

    def _load_team_psychology_insights(self) -> Dict:
        """Load insights about team psychology and dynamics"""
        return {
            "communication_styles": {
                "direct": "Appreciate clear, straightforward communication",
                "collaborative": "Prefer discussion and consensus building",
                "analytical": "Need data and detailed explanations",
                "expressive": "Value enthusiasm and creative brainstorming"
            },
            "work_styles": {
                "structured": "Prefer detailed plans and clear timelines",
                "flexible": "Adapt well to changing requirements",
                "independent": "Work best with minimal supervision",
                "collaborative": "Thrive on team interaction and feedback"
            }
        }

    def _load_presentation_frameworks(self) -> Dict:
        """Load presentation frameworks and templates"""
        return {
            "problem_solution": ["Hook with problem", "Show solution demo", "Explain technical approach",
                                 "Discuss impact"],
            "story_driven": ["Personal story opening", "Problem discovery", "Solution journey", "Future vision"],
            "technical_deep_dive": ["Problem complexity", "Technical innovation", "Implementation details",
                                    "Performance results"]
        }

    def _get_tech_focused_ideas(self, technologies: List[str]) -> List[Dict]:
        """Generate project ideas focused on specific technologies"""
        tech_ideas = {
            'ai': [
                {
                    "title": "Smart Study Companion",
                    "description": "AI-powered learning assistant that adapts to individual learning styles and creates personalized study plans",
                    "tech_stack": ["Python", "TensorFlow", "Flask", "React"]
                },
                {
                    "title": "Code Review Assistant",
                    "description": "ML model that analyzes code for bugs, performance issues, and suggests improvements",
                    "tech_stack": ["Python", "PyTorch", "FastAPI", "GitHub API"]
                }
            ],
            'react': [
                {
                    "title": "Real-Time Collaboration Hub",
                    "description": "Live collaborative workspace with real-time editing, video chat, and project management",
                    "tech_stack": ["React", "WebRTC", "Socket.io", "Node.js"]
                }
            ],
            'blockchain': [
                {
                    "title": "Decentralized Learning Platform",
                    "description": "Blockchain-based skill verification and peer-to-peer learning marketplace",
                    "tech_stack": ["Solidity", "React", "Web3.js", "IPFS"]
                }
            ]
        }

        ideas = []
        for tech in technologies:
            if tech in tech_ideas:
                ideas.extend(tech_ideas[tech])

        return ideas[:3]  # Return top 3 relevant ideas

    def _get_role_specific_team_advice(self, role: str) -> str:
        """Get team formation advice specific to user's role"""
        role_advice = {
            "developer": "Look for a designer to handle UI/UX and a business person to validate market fit. Your technical skills are valuable - use them to assess project feasibility.",
            "designer": "Partner with developers who appreciate good design and product people who understand user experience. Your visual and UX skills will differentiate your team's solution.",
            "product_manager": "Find developers who can execute your vision and designers who can bring it to life. Your strategic thinking and user focus will guide the team to build something people actually want.",
            "data_scientist": "Team up with developers who can integrate your models and business people who understand the problem domain. Your analytical skills can provide unique insights."
        }

        return role_advice.get(role.lower(),
                               "Bring your unique skills and look for complementary team members who share your passion for the problem you want to solve.")

    def _get_tech_specific_advice(self, area: str) -> str:
        """Get specific advice for technical areas"""
        advice = {
            "frontend": "Use CSS frameworks like Tailwind or Bootstrap for rapid styling. Focus on user experience over visual perfection.",
            "backend": "Keep your API simple and well-documented. Use established patterns and don't over-engineer.",
            "database": "Design your schema on paper first. Use migrations and keep backups of sample data.",
            "deployment": "Set up deployment early and deploy often. Use platforms like Vercel, Netlify, or Heroku for quick hosting.",
            "mobile": "Test on real devices frequently. Use cross-platform frameworks to maximize reach with limited time."
        }

        return advice.get(area, "Start simple, test often, and focus on core functionality first.")


# Global enhanced assistant instance
enhanced_ai = AdvancedAIAssistant()


def get_enhanced_ai_response(query: str, context_data: Optional[Dict] = None) -> str:
    """Get enhanced AI response with context awareness"""
    return enhanced_ai.generate_response(query, context_data)


def get_ai_suggestion_with_context(query: str, participant_data: Optional[Dict] = None) -> str:
    """Get AI suggestions with participant context"""
    context = {}
    if participant_data:
        context.update({
            'user_role': participant_data.get('role'),
            'user_experience': participant_data.get('experience_level'),
            'user_skills': participant_data.get('skills', []),
            'user_interests': participant_data.get('interests', [])
        })

    return get_enhanced_ai_response(query, context)