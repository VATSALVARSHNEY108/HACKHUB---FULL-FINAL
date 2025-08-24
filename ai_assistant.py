import json
import os
import random
import re
from gemini_assistant import gemini_assistant


# Removed OpenAI integration - using only Gemini and local fallback

# Comprehensive AI assistant with OpenAI integration
class EnhancedAIAssistant:
    def __init__(self):
        # Enhanced team formation tips
        self.team_tips = [
            "Look for teammates with complementary skills - if you're a developer, find a designer and a business person.",
            "Diverse experience levels work great together - senior members can mentor juniors while bringing fresh perspectives.",
            "Good communication is more important than perfect technical skills. Choose people you can work with.",
            "Aim for 3-4 people per team - small enough to move fast, large enough to handle different aspects.",
            "Consider timezone compatibility if working remotely during the hackathon.",
            "Test your team's chemistry with a quick brainstorming session before committing.",
            "Establish clear roles and responsibilities early to avoid confusion during crunch time.",
            "Choose teammates who are passionate about the problem you want to solve, not just the technology.",
            "Look for people who stay calm under pressure and can adapt when plans change."
        ]

        # Expanded project ideas by category
        self.project_ideas = {
            "ai_ml": [
                "AI-powered study buddy that adapts to learning styles and generates personalized quizzes",
                "Computer vision app for real-time sign language translation",
                "Machine learning model to predict and prevent equipment failures in smart buildings",
                "AI chatbot for mental health support with mood tracking and therapy techniques",
                "Automated code review assistant that suggests improvements and catches bugs"
            ],
            "web_mobile": [
                "Social platform for skill sharing and local community building",
                "Progressive web app for offline-first note-taking with smart organization",
                "Mobile app for crowdsourced accessibility mapping of public spaces",
                "Real-time collaboration tool for remote teams with integrated video and whiteboarding",
                "Gamified habit tracker that creates social accountability groups"
            ],
            "iot_hardware": [
                "Smart home energy optimizer using IoT sensors and machine learning",
                "Wearable device for monitoring air quality and providing health alerts",
                "IoT-based smart garden system with automated watering and growth tracking",
                "Connected pet monitoring system with health analytics and vet recommendations",
                "Smart parking solution using sensors and mobile payments"
            ],
            "social_impact": [
                "Platform connecting volunteers with local nonprofits based on skills and availability",
                "App for reporting and tracking community infrastructure issues",
                "Digital literacy training platform for seniors with simplified interfaces",
                "Food waste reduction app connecting restaurants with food banks",
                "Emergency preparedness app with community alert system and resource sharing"
            ],
            "fintech": [
                "Micro-investment app that rounds up purchases and invests spare change",
                "Peer-to-peer lending platform for students with income-based repayment",
                "Personal finance assistant that analyzes spending patterns and suggests optimizations",
                "Cryptocurrency portfolio tracker with risk assessment and educational content",
                "Digital wallet for small businesses with integrated accounting and tax preparation"
            ],
            "health_wellness": [
                "Mental health check-in app with mood tracking and personalized coping strategies",
                "Fitness app that creates custom workouts based on available equipment and time",
                "Medication reminder system with pill identification and interaction warnings",
                "Sleep optimization app that analyzes patterns and suggests environmental improvements",
                "Nutrition tracker that scans food labels and provides personalized dietary advice"
            ]
        }

        # Comprehensive role-based advice
        self.role_advice = {
            "developer": "You bring technical implementation skills. Look for designers for UI/UX and business minds for strategy. Focus on feasible MVPs and clean, scalable code.",
            "designer": "Your visual and user experience skills are crucial. Partner with developers and product thinkers. Create wireframes early and test usability assumptions.",
            "business": "Your strategic thinking is valuable. Team up with technical implementers and creative designers. Focus on market validation and compelling storytelling.",
            "data": "Your analytical skills are in high demand. Join forces with developers and domain experts. Prepare datasets early and focus on actionable insights.",
            "product": "You bridge technical and business needs. Work with all team members to define scope and priorities. Keep the user experience at the center of decisions.",
            "marketing": "Your growth and communication skills are essential for demos. Partner with technical team members and focus on user acquisition strategies.",
            "researcher": "Your deep domain knowledge adds credibility. Collaborate with implementers to translate research into practical solutions."
        }

        # Hackathon timeline and planning advice
        self.timeline_advice = {
            "planning": [
                "Spend the first 2-3 hours on ideation and team formation - don't rush this step",
                "Create a project timeline with hourly milestones for the first day",
                "Set up your development environment and version control immediately",
                "Define your MVP clearly and write it down - refer back to it when you get distracted"
            ],
            "development": [
                "Start with the core functionality first, then add features if time permits",
                "Use existing libraries and frameworks to save time - don't reinvent the wheel",
                "Make frequent commits and push to version control regularly",
                "Test your app on different devices and browsers early and often"
            ],
            "presentation": [
                "Start preparing your pitch at least 4 hours before the deadline",
                "Practice your demo multiple times and have a backup plan if tech fails",
                "Tell a story: problem, solution, impact - not just technical features",
                "Prepare for questions about scalability, monetization, and technical challenges"
            ]
        }

        # Technical tips and best practices
        self.technical_tips = {
            "architecture": [
                "Choose technologies your team knows well - hackathons aren't the time to learn new frameworks",
                "Use cloud platforms for quick deployment - Vercel, Netlify, Heroku make hosting easy",
                "Set up CI/CD early if you have the expertise - automated testing saves debugging time",
                "Design your database schema on paper before coding to avoid restructuring later"
            ],
            "apis": [
                "Research API rate limits and authentication requirements before building dependencies",
                "Always have a fallback plan if external APIs fail during the demo",
                "Use API mocking tools for development when external services are unreliable",
                "Document your API endpoints clearly for team members working on frontend"
            ],
            "frontend": [
                "Use CSS frameworks like Bootstrap or Tailwind for rapid UI development",
                "Focus on core user flows first - you can always improve visual polish later",
                "Make sure your app works on mobile devices, even if it's not mobile-first",
                "Use placeholder content initially, then replace with real data when backend is ready"
            ],
            "data": [
                "Clean and validate your datasets early in the process",
                "Use visualization libraries to make your data insights compelling",
                "Prepare example queries and results to demonstrate your data analysis",
                "Consider data privacy and security implications, especially for sensitive information"
            ]
        }

        # Common hackathon pitfalls and how to avoid them
        self.pitfall_advice = [
            "Scope creep: Start small and add features only if you finish early",
            "Technical debt: Write clean code from the start - you won't have time to refactor later",
            "Poor time management: Use timeboxing and set hard deadlines for each feature",
            "Neglecting the demo: Your presentation is as important as your code",
            "Not testing early: Test on different devices and edge cases throughout development",
            "Forgetting about users: Always think about who will use your app and why",
            "Overengineering: Simple solutions that work are better than complex ones that don't",
            "Poor team communication: Use tools like Slack or Discord to stay coordinated"
        ]


# Enhanced AI assistant with OpenAI integration
ai_assistant = EnhancedAIAssistant()


# Removed OpenAI function - now using only Gemini and local fallback

def get_local_ai_suggestion(user_message, context=None):
    """
    Comprehensive local AI assistant that can handle any type of question intelligently
    """
    message_lower = user_message.lower()

    # Quick access to AI assistant data
    assistant = EnhancedAIAssistant()

    # Greeting and general conversation
    if any(word in message_lower for word in ["hello", "hi", "hey", "greetings"]):
        greetings = [
            "Hey there! Great to meet you. I'm genuinely excited to dive into whatever you're working on or thinking about. What's on your mind?",
            "Hi! I love getting to know what people are curious about or trying to solve. Whether it's something technical, creative, or just an interesting idea you want to explore, I'm all ears.",
            "Hello! There's something energizing about new conversations. I'm here to think through problems with you, brainstorm, or just have an engaging discussion about whatever interests you.",
            "Hey! I'm really curious about what brought you here today. Are you wrestling with a challenge, exploring a new idea, or just want to have an interesting conversation?"
        ]
        return random.choice(greetings)

    # Thank you responses
    elif any(phrase in message_lower for phrase in ["thank you", "thanks", "appreciate"]):
        return "That really means a lot! I love when we can work through something together and find a path forward. What else is on your mind?"

    # Team formation specific advice
    elif any(phrase in message_lower for phrase in
             ["team formation", "find team", "looking for team", "team up", "join team"]):
        tips = [
            "Great question! Here are some proven strategies for finding the right hackathon team:",
            "\n• **Skill Complementarity**: Look for people whose skills complement yours. If you're technical, find designers and business-minded folks.",
            "\n• **Communication Style**: Good teams communicate well under pressure. Look for people who listen, ask questions, and stay positive.",
            "\n• **Experience Balance**: Mix of experience levels often works well - seniors mentor, juniors bring fresh perspectives.",
            "\n• **Project Passion**: Find people genuinely excited about similar problem spaces or technologies.",
            "\n• **Team Size**: 3-4 people is usually optimal - enough diverse skills, small enough to move fast."
        ]
        tips.append(f"\n\nAlso, here's a specific tip: {random.choice(assistant.team_tips)}")
        return "".join(tips)

    # Project ideas and brainstorming
    elif any(phrase in message_lower for phrase in
             ["project idea", "what to build", "hackathon project", "brainstorm", "ideas"]):
        categories = list(assistant.project_ideas.keys())
        selected_category = random.choice(categories)
        ideas = assistant.project_ideas[selected_category]

        response = f"Here are some inspiring project ideas in the **{selected_category.replace('_', '/').upper()}** category:\n\n"
        for i, idea in enumerate(ideas[:3], 1):
            response += f"{i}. {idea}\n"

        response += f"\nI love how these projects solve real problems while being technically exciting! What kind of impact or technology area interests you most? I can suggest ideas in other categories like {', '.join([cat.replace('_', '/') for cat in categories if cat != selected_category][:3])}."

        return response

    # Hackathon strategy and timeline advice
    elif any(phrase in message_lower for phrase in
             ["hackathon strategy", "time management", "hackathon tips", "how to win", "hackathon advice"]):
        if "time" in message_lower or "timeline" in message_lower:
            phase = random.choice(["planning", "development", "presentation"])
            tips = assistant.timeline_advice[phase]
            response = f"**{phase.upper()} PHASE TIPS:**\n\n"
            for tip in tips:
                response += f"• {tip}\n"
            response += f"\nTime management is crucial! Here's a key insight: {random.choice(assistant.pitfall_advice)}"
        else:
            response = "**HACKATHON SUCCESS STRATEGY:**\n\n"
            response += "**1. Team Formation (First 3 hours)**\n"
            response += "• Find complementary skills and good communication\n"
            response += "• Test team chemistry with quick ideation session\n\n"
            response += "**2. Project Planning (Next 2 hours)**\n"
            response += "• Define clear MVP scope and stick to it\n"
            response += "• Set up development environment immediately\n\n"
            response += "**3. Development (Bulk of time)**\n"
            response += "• Build core functionality first, polish later\n"
            response += "• Test frequently on different devices\n\n"
            response += "**4. Presentation Prep (Final 4 hours)**\n"
            response += "• Practice demo multiple times\n"
            response += "• Focus on problem/solution story, not just tech"

        return response

    # Direct question answering
    elif any(phrase in message_lower for phrase in ["what is", "what are", "define", "explain", "meaning of"]):
        # Handle specific technical terms and concepts
        if "llm" in message_lower:
            return "LLM stands for Large Language Model. It's an AI system trained on massive amounts of text data to understand and generate human-like text. Examples include GPT, Claude, and Gemini."
        elif "api" in message_lower:
            return "API stands for Application Programming Interface. It's a way for different software applications to communicate with each other by defining rules and protocols for requests and responses."
        elif "machine learning" in message_lower or "ml" in message_lower:
            return "Machine Learning (ML) is a type of artificial intelligence where computers learn patterns from data to make predictions or decisions without being explicitly programmed for each task."
        elif "neural network" in message_lower:
            return "A neural network is a computing system inspired by biological neural networks. It uses interconnected nodes (neurons) to process information and learn patterns from data."
        elif "algorithm" in message_lower:
            return "An algorithm is a step-by-step set of instructions designed to solve a specific problem or perform a particular task in computing."
        elif "database" in message_lower:
            return "A database is an organized collection of data stored electronically. It allows you to store, retrieve, and manage information efficiently."
        elif "framework" in message_lower:
            return "A framework is a pre-built foundation of code that provides structure and common functionality for building applications more efficiently."
        elif "library" in message_lower:
            return "A library is a collection of pre-written code that developers can use to perform common tasks without writing everything from scratch."
        else:
            return "I'd be happy to explain that! Can you be more specific about what you'd like to know?"

    # Technical implementation advice
    elif any(
            word in message_lower for word in ["api", "backend", "frontend", "database", "deployment", "architecture"]):
        if "api" in message_lower:
            tips = assistant.technical_tips["apis"]
            area = "API INTEGRATION"
        elif "frontend" in message_lower or "ui" in message_lower:
            tips = assistant.technical_tips["frontend"]
            area = "FRONTEND DEVELOPMENT"
        elif "database" in message_lower or "data" in message_lower:
            tips = assistant.technical_tips["data"]
            area = "DATA & DATABASE"
        else:
            tips = assistant.technical_tips["architecture"]
            area = "ARCHITECTURE & DEPLOYMENT"

        response = f"**{area} TIPS:**\n\n"
        for tip in tips:
            response += f"• {tip}\n"

        response += f"\n**Key insight:** {random.choice(assistant.pitfall_advice)}"
        return response

    # Role-specific advice
    elif any(role in message_lower for role in ["developer", "designer", "business", "product", "marketing", "data"]):
        for role, advice in assistant.role_advice.items():
            if role in message_lower:
                response = f"**ADVICE FOR {role.upper()}S:**\n\n{advice}\n\n"
                response += f"**Bonus tip:** {random.choice(assistant.team_tips)}"
                return response

    # Creative requests and entertainment
    elif any(word in message_lower for word in ["joke", "story", "creative", "funny", "entertain"]):
        if "joke" in message_lower:
            jokes = [
                "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
                "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
                "Why did the programmer quit his job? He didn't get arrays! (a raise)",
                "What's a programmer's favorite hangout place? Foo Bar!",
                "Why do Java developers wear glasses? Because they can't C#!"
            ]
            return f"Oh, I love a good joke! {random.choice(jokes)} I have to admit, I find these programming puns way funnier than I probably should. Do you write code? There's something about developer humor that just hits different when you've lived through the pain yourself."
        elif "story" in message_lower:
            return """I love this story! So there was this developer who had been staring at a bug for literally hours. Nothing was working, they'd tried everything, and they were getting that special kind of frustrated that only comes from code that should absolutely be working but isn't.

Finally, in desperation, they grabbed the rubber duck sitting on their desk and started explaining the entire problem out loud, line by line. And you know what happened? Halfway through talking to this duck, they suddenly went "Oh my god, I see it!" The solution just clicked.

That's how "rubber duck debugging" became a real thing. There's something magical about forcing yourself to articulate a problem clearly enough that you could explain it to, well, a rubber duck. Your brain often finds the answer in the process of trying to teach it to someone else. Even if that someone is a bath toy."""
        else:
            return "I'm always up for some creative exploration! There's something really energizing about brainstorming wild ideas, spinning stories, or just letting our minds wander in interesting directions. What kind of creative thing are you in the mood for? We could brainstorm something innovative, dive into storytelling, or just explore whatever random creative tangent sounds fun to you."

    # Programming and technical questions
    elif any(word in message_lower for word in
             ["python", "javascript", "java", "html", "css", "react", "function", "code", "programming", "algorithm",
              "web", "app", "software", "debug", "error"]):
        if "python" in message_lower:
            return """Python is a versatile, beginner-friendly programming language! Here are some key features:

• **Easy syntax**: Readable and intuitive code
• **Versatile**: Web development, data science, AI, automation
• **Rich ecosystem**: Millions of packages on PyPI
• **Great for beginners**: Clear syntax and excellent documentation

Popular Python frameworks:
- **Web**: Django, Flask, FastAPI
- **Data Science**: Pandas, NumPy, Matplotlib
- **AI/ML**: TensorFlow, PyTorch, scikit-learn

**Common Python use cases:**
• Web scraping with Beautiful Soup and Selenium
• API development with FastAPI or Flask
• Data analysis with Pandas and visualization with Matplotlib
• Machine learning with scikit-learn and TensorFlow
• Automation and scripting for repetitive tasks"""

        elif "javascript" in message_lower:
            return """JavaScript is the language of the web! Here's what makes it powerful:

• **Universal**: Runs in browsers, servers (Node.js), and mobile apps
• **Event-driven**: Perfect for interactive user interfaces
• **Flexible**: Supports multiple programming paradigms
• **Huge ecosystem**: NPM has over 1 million packages

**Key JavaScript concepts:**
- **DOM manipulation**: Changing web page content
- **Async programming**: Promises and async/await
- **ES6+ features**: Arrow functions, destructuring, modules

Popular frameworks:
- **Frontend**: React, Vue, Angular
- **Backend**: Express.js, Next.js

**Modern JavaScript is used for:**
• Interactive web applications
• Server-side development with Node.js
• Mobile app development with React Native
• Desktop apps with Electron"""

        else:
            return """**PROGRAMMING FUNDAMENTALS:**

**Key Concepts:**
• **Variables**: Store and manipulate data
• **Functions**: Reusable blocks of code
• **Control Flow**: if/else statements, loops
• **Data Structures**: Arrays, objects, lists
• **Algorithms**: Step-by-step problem-solving approaches

**Best Practices:**
• Write clean, readable code with good naming
• Use version control (Git) for all projects
• Test your code frequently during development
• Comment your code to explain complex logic
• Follow consistent coding style and conventions

**Popular Languages for Beginners:**
• **Python**: Great syntax, versatile applications
• **JavaScript**: Essential for web development
• **Java**: Object-oriented, widely used in enterprise
• **HTML/CSS**: Foundation for web development

What specific programming topic interests you most?"""

    # General conversation and fallback
    else:
        # Try to extract key concepts and provide relevant advice
        if "help" in message_lower or "advice" in message_lower:
            return f"I'm here to help! I specialize in hackathon advice, team formation, project ideas, and technical guidance. What specific area would you like to explore?"
        elif "problem" in message_lower or "challenge" in message_lower:
            return "I love tackling challenges! The best approach is usually to break big problems into smaller, manageable pieces. What's the specific challenge you're facing?"
        else:
            return "How can I help you today? I can assist with hackathons, programming, team formation, or answer technical questions."


def get_team_formation_advice(role, experience, interests):
    """
    Generate personalized team formation advice based on user profile
    """
    advice_parts = []

    if role.lower() in ['developer', 'engineer', 'programmer']:
        advice_parts.append(
            "As a developer, you're the technical backbone. Look for creative designers who can implement your vision and business minds who understand user needs.")
    elif role.lower() in ['designer', 'ui', 'ux']:
        advice_parts.append(
            "Your design skills are crucial for user experience. Partner with developers who can implement your vision and business minds who understand user needs.")
    elif role.lower() in ['business', 'product', 'manager']:
        advice_parts.append(
            "Your strategic thinking and user focus are valuable. Team up with technical implementers and creative designers to build something users actually want.")
    else:
        advice_parts.append(
            f"As a {role}, bring your unique perspective to the team. Look for complementary skills in technical implementation, design, and business strategy.")

    if experience.lower() in ['beginner', 'junior']:
        advice_parts.append(
            "Don't worry about being new - your fresh perspective is valuable! Look for mentors willing to guide you, and contribute your enthusiasm and different viewpoint.")
    elif experience.lower() in ['senior', 'expert', 'advanced']:
        advice_parts.append(
            "Your experience is a huge asset. Consider mentoring newer participants while leveraging your skills to tackle complex challenges.")

    advice_parts.append(
        f"Based on your interests in {', '.join(interests[:3]) if interests else 'various areas'}, look for projects that excite you personally - passion drives great hackathon results!")

    return " ".join(advice_parts)


def get_comprehensive_hackathon_help(query):
    """
    Enhanced AI assistant using Gemini API for comprehensive hackathon guidance
    """
    return gemini_assistant.generate_response(query, context_type="hackathon")


def get_ai_suggestion(query):
    """
    General AI suggestions using Gemini with local fallback
    """
    # Try Gemini first
    try:
        if gemini_assistant.is_available():
            return gemini_assistant.generate_response(query, context_type="general")
    except Exception as e:
        print(f"Gemini AI error: {e}")

    # Fallback to local assistant
    return get_local_ai_suggestion(query)


def get_project_ideas(theme=None):
    """
    Get project ideas using Gemini API
    """
    if theme:
        query = f"Suggest innovative project ideas for a hackathon with the theme '{theme}'. Provide specific, implementable ideas with brief descriptions."
    else:
        query = "Suggest innovative project ideas for hackathons across different categories like AI/ML, web development, mobile apps, social impact, and fintech."

    return gemini_assistant.generate_response(query, context_type="hackathon")


def get_hackathon_resources():
    """
    Provide useful hackathon resources and tools
    """
    return {
        "design_tools": [
            "Figma - Free collaborative design tool",
            "Canva - Quick graphics and presentations",
            "Unsplash - Free high-quality photos",
            "Google Fonts - Free web fonts",
            "Coolors.co - Color palette generator"
        ],
        "development_tools": [
            "GitHub - Version control and collaboration",
            "Visual Studio Code - Free code editor",
            "Postman - API testing and documentation",
            "Firebase - Backend as a service",
            "Vercel/Netlify - Easy deployment platforms"
        ],
        "api_resources": [
            "RapidAPI - Marketplace for APIs",
            "OpenAI API - AI and language models",
            "Stripe API - Payment processing",
            "Google Maps API - Location services",
            "Twilio API - SMS and communication"
        ],
        "learning_resources": [
            "MDN Web Docs - Web development reference",
            "Stack Overflow - Programming Q&A",
            "YouTube tutorials - Video learning",
            "Codecademy - Interactive coding lessons",
            "FreeCodeCamp - Free coding bootcamp"
        ]
    }