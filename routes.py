from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from models import Participant, Team
from team_matcher import TeamMatcher
from ai_assistant import get_ai_suggestion, get_project_ideas, get_team_formation_advice, \
    get_comprehensive_hackathon_help, get_hackathon_resources
from datetime import datetime


@app.route('/')
def index():
    participant_count = Participant.query.count()

    # Get some stats for the dashboard
    developers = Participant.query.filter_by(role='Developer').count()
    designers = Participant.query.filter_by(role='Designer').count()

    return render_template('index.html',
                           participant_count=participant_count,
                           developer_count=developers,
                           designer_count=designers)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            # Parse skills and interests from comma-separated strings
            skills_str = request.form.get('skills', '')
            interests_str = request.form.get('interests', '')

            skills = [skill.strip() for skill in skills_str.split(',') if skill.strip()]
            interests = [interest.strip() for interest in interests_str.split(',') if interest.strip()]

            participant = Participant(
                name=request.form['name'],
                email=request.form['email'],
                role=request.form['role'],
                experience_level=request.form['experience_level'],
                skills=skills,
                interests=interests,
                preferred_team_size=int(request.form.get('preferred_team_size', 4)),
                availability=request.form['availability'],
                github_url=request.form.get('github_url', ''),
                linkedin_url=request.form.get('linkedin_url', '')
            )

            db.session.add(participant)
            db.session.commit()

            flash('Registration successful! You can now be matched with teams.', 'success')
            return redirect(url_for('participants'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error during registration: {str(e)}', 'error')

    return render_template('register.html')


@app.route('/participants')
def participants():
    participants = Participant.query.all()
    return render_template('participants.html', participants=participants)


@app.route('/teams')
def teams():
    teams = Team.query.all()
    return render_template('teams.html', teams=teams)


@app.route('/hackathon-portals')
def hackathon_portals():
    return render_template('hackathon_portals.html')


@app.route('/connect')
def connect():
    return render_template('connect.html')


@app.route('/simple_register', methods=['GET', 'POST'])
def simple_register():
    if request.method == 'POST':
        try:
            email = request.form['email']

            # Check if email already exists
            existing_participant = Participant.query.filter_by(email=email).first()
            if existing_participant:
                flash('This email is already registered! Please use a different email or check the participants list.',
                      'error')
                return render_template('simple_register.html')

            # Parse skills and interests from comma-separated strings
            skills_str = request.form.get('skills', '')
            interests_str = request.form.get('interests', '')

            skills = [skill.strip() for skill in skills_str.split(',') if skill.strip()]
            interests = [interest.strip() for interest in interests_str.split(',') if interest.strip()]

            participant = Participant(
                name=request.form['name'],
                email=email,
                role=request.form['role'],
                experience_level=request.form['experience_level'],
                skills=skills,
                interests=interests,
                preferred_team_size=int(request.form.get('preferred_team_size', 4)),
                availability=request.form['availability']
            )

            db.session.add(participant)
            db.session.commit()

            flash('Registration successful!', 'success')
            return redirect(url_for('simple_participants'))

        except Exception as e:
            db.session.rollback()
            # Handle specific database errors
            if "duplicate key value violates unique constraint" in str(e) and "email" in str(e):
                flash('This email is already registered! Please use a different email.', 'error')
            else:
                flash(f'Registration failed. Please try again.', 'error')

    return render_template('simple_register.html')


@app.route('/simple_participants')
def simple_participants():
    participants = Participant.query.all()
    return render_template('simple_participants.html', participants=participants)


@app.route('/project-ideas')
def project_ideas():
    return render_template('project_ideas.html')


@app.route('/generate-project-ideas', methods=['POST'])
def generate_project_ideas():
    try:
        data = request.get_json()

        # Build prompt based on user preferences
        prompt = "Generate 3 innovative hackathon project ideas with the following preferences:\n"

        if data.get('technology'):
            prompt += f"Technology focus: {data['technology']}\n"
        if data.get('team_size'):
            prompt += f"Team size: {data['team_size']} members\n"
        if data.get('experience'):
            prompt += f"Experience level: {data['experience']}\n"
        if data.get('duration'):
            prompt += f"Project duration: {data['duration']}\n"
        if data.get('skills'):
            prompt += f"Skills/interests: {data['skills']}\n"

        prompt += """
For each idea, provide:
1. Title (creative and catchy)
2. Description (2-3 sentences)
3. Category (e.g., Social Impact, FinTech, Health, etc.)
4. Difficulty level (Beginner, Intermediate, Advanced)
5. Tech stack (3-5 technologies)
6. Team roles needed (2-4 roles)
7. Key features (3-4 main features)

Format as JSON array with this structure:
[{
  "title": "Project Name",
  "description": "Brief description...",
  "category": "Category",
  "difficulty": "Level",
  "tech_stack": ["Tech1", "Tech2", "Tech3"],
  "team_roles": ["Role1", "Role2", "Role3"],
  "features": ["Feature1", "Feature2", "Feature3"]
}]
"""

        # Get AI response
        from ai_assistant import get_project_ideas
        ai_response = get_project_ideas(prompt)

        # Try to parse JSON response
        try:
            import json
            ideas = json.loads(ai_response)
            if not isinstance(ideas, list):
                raise ValueError("Response is not a list")
        except:
            # Fallback ideas if AI response fails
            ideas = [
                {
                    "title": "SmartGarden IoT",
                    "description": "Automated plant care system using sensors and AI to optimize watering, lighting, and nutrients for indoor gardens.",
                    "category": "IoT/GreenTech",
                    "difficulty": "Intermediate",
                    "tech_stack": ["Arduino", "Python", "React", "Firebase"],
                    "team_roles": ["IoT Developer", "Web Developer", "Data Scientist"],
                    "features": ["Sensor monitoring", "Mobile alerts", "Growth analytics", "Automated watering"]
                },
                {
                    "title": "CommunityFund",
                    "description": "Blockchain-based platform for transparent community fundraising with smart contracts and decentralized voting.",
                    "category": "Blockchain/Social",
                    "difficulty": "Advanced",
                    "tech_stack": ["Solidity", "React", "Web3.js", "IPFS"],
                    "team_roles": ["Blockchain Developer", "Frontend Developer", "UX Designer"],
                    "features": ["Smart contracts", "Voting mechanism", "Fund tracking", "Community dashboard"]
                },
                {
                    "title": "AI Meditation Guide",
                    "description": "Personalized meditation app that adapts to user's stress levels and preferences using ML and biometric data.",
                    "category": "Health/AI",
                    "difficulty": "Intermediate",
                    "tech_stack": ["Python", "TensorFlow", "React Native", "HealthKit"],
                    "team_roles": ["AI Developer", "Mobile Developer", "UX Designer", "Health Expert"],
                    "features": ["Stress detection", "Personalized sessions", "Progress tracking",
                                 "Biometric integration"]
                }
            ]

        return jsonify({"success": True, "ideas": ideas})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route('/teams-view')
def teams_view():
    teams = Team.query.all()
    available_count = Participant.query.filter_by(team_id=None).count()

    # Get team members for each team
    for team in teams:
        team.members = Participant.query.filter_by(team_id=team.id).all()

    return render_template('teams_view.html', teams=teams, available_count=available_count)


@app.route('/ai-suggest-teams', methods=['POST'])
def ai_suggest_teams():
    try:
        # Get all available participants (not in teams)
        participants = Participant.query.filter_by(team_id=None).all()

        if len(participants) < 2:
            return jsonify({"success": False, "error": "Need at least 2 participants to suggest teams"})

        # Build participant data for AI analysis
        participant_data = []
        for p in participants:
            participant_data.append({
                "name": p.name,
                "email": p.email,
                "role": p.role,
                "experience_level": p.experience_level,
                "skills": p.skills if p.skills else [],
                "interests": p.interests if p.interests else [],
                "preferred_team_size": p.preferred_team_size or 4,
                "availability": p.availability
            })

        # Create AI prompt for team suggestions
        prompt = f"""
Analyze the following {len(participants)} hackathon participants and suggest optimal team combinations:

Participants:
"""

        for p in participant_data:
            prompt += f"""
- {p['name']} ({p['role']}, {p['experience_level']})
  Skills: {', '.join(p['skills'])}
  Interests: {', '.join(p['interests'])}
  Preferred team size: {p['preferred_team_size']}
  Email: {p['email']}
"""

        prompt += """
Please provide 2-3 different team combination suggestions. For each suggestion:

1. List the team members
2. Explain the reasoning (why these people work well together)
3. Give a compatibility score (0-100%)
4. Suggest a project idea that matches the team's combined skills

Format as JSON:
[{
  "members": [{"name": "...", "role": "...", "experience_level": "...", "email": "...", "skills": [...]}],
  "reasoning": "Why this team works well together...",
  "compatibility_score": 85,
  "project_suggestion": "A brief project idea..."
}]
"""

        # Get AI response
        from ai_assistant import get_ai_suggestion
        ai_response = get_ai_suggestion(prompt)

        # Try to parse JSON response
        try:
            import json
            suggestions = json.loads(ai_response)
            if not isinstance(suggestions, list):
                raise ValueError("Response is not a list")
        except:
            # Fallback suggestions if AI response fails
            suggestions = []

            # Create simple suggestions based on role diversity
            if len(participants) >= 2:
                developers = [p for p in participant_data if p['role'] == 'Developer']
                designers = [p for p in participant_data if p['role'] == 'Designer']
                others = [p for p in participant_data if p['role'] not in ['Developer', 'Designer']]

                # Suggestion 1: Mix of roles
                team1 = []
                if developers: team1.append(developers[0])
                if designers: team1.append(designers[0])
                if len(team1) < 4 and others: team1.extend(others[:2])
                if len(team1) < 4 and len(developers) > 1: team1.append(developers[1])

                if len(team1) >= 2:
                    suggestions.append({
                        "members": team1,
                        "reasoning": "This team combines different roles for diverse skill coverage and balanced perspectives.",
                        "compatibility_score": 75,
                        "project_suggestion": "A web application that combines technical development with user-focused design."
                    })

                # Suggestion 2: Remaining participants
                remaining = [p for p in participant_data if p not in team1]
                if len(remaining) >= 2:
                    suggestions.append({
                        "members": remaining,
                        "reasoning": "This team groups remaining participants with complementary skills and experience levels.",
                        "compatibility_score": 70,
                        "project_suggestion": "A project that leverages the unique combination of skills in this team."
                    })

        return jsonify({"success": True, "suggestions": suggestions})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route('/generate-teams', methods=['POST'])
def generate_teams():
    try:
        # Get unassigned participants
        unassigned_participants = Participant.query.filter_by(team_id=None).all()

        if len(unassigned_participants) < 2:
            return jsonify({
                'success': False,
                'message': 'Need at least 2 unassigned participants to form teams'
            })

        # Initialize team matcher
        matcher = TeamMatcher()
        generated_teams = matcher.create_balanced_teams(unassigned_participants)

        teams_created = 0
        for team_data in generated_teams:
            # Create team
            team = Team(
                name=team_data['name'],
                description=team_data['description'],
                balance_score=team_data['balance_score'],
                tech_stack=team_data['suggested_tech_stack']
            )
            db.session.add(team)
            db.session.flush()  # Get team ID

            # Assign participants to team
            for participant_id in team_data['participant_ids']:
                participant = Participant.query.get(participant_id)
                if participant:
                    participant.team_id = team.id

            teams_created += 1

        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Successfully created {teams_created} teams!',
            'teams_created': teams_created
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error generating teams: {str(e)}'
        })


@app.route('/api/ai-chat', methods=['POST'])
def ai_chat():
    try:
        data = request.get_json()
        message = data.get('message', '')

        # Use Gemini-powered AI assistant for intelligent responses
        response = get_ai_suggestion(message)

        return jsonify({
            'success': True,
            'response': response
        })

    except Exception as e:
        print(f"AI Chat Error: {e}")
        return jsonify({
            'success': False,
            'response': f'Sorry, I encountered an error: {str(e)}'
        })


@app.route('/api/project-ideas', methods=['POST'])
def api_project_ideas():
    try:
        data = request.get_json()
        team_skills = data.get('team_skills', [])
        theme = data.get('theme', '')

        ideas = get_project_ideas(theme)

        return jsonify({
            'success': True,
            'ideas': ideas
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error generating project ideas: {str(e)}'
        })


@app.route('/api/hackathon-resources')
def api_hackathon_resources():
    """Provide useful resources for hackathon participants"""
    try:
        resources = get_hackathon_resources()
        return jsonify({
            'success': True,
            'resources': resources
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error getting resources: {str(e)}'
        })


@app.route('/api/ai-help', methods=['POST'])
def ai_help():
    """Enhanced AI help endpoint for specific hackathon questions"""
    try:
        data = request.get_json()
        query = data.get('query', '')

        # Use the comprehensive help function
        response = get_comprehensive_hackathon_help(query)

        return jsonify({
            'success': True,
            'response': response,
            'query': query
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'response': f'Sorry, I encountered an error: {str(e)}'
        })


@app.route('/api/team-stats')
def team_stats():
    try:
        teams = Team.query.all()
        participants = Participant.query.all()

        # Role distribution
        role_counts = {}
        for participant in participants:
            role = participant.role
            role_counts[role] = role_counts.get(role, 0) + 1

        # Experience distribution
        experience_counts = {}
        for participant in participants:
            exp = participant.experience_level
            experience_counts[exp] = experience_counts.get(exp, 0) + 1

        # Team size distribution
        team_sizes = {}
        for team in teams:
            size = len(team.participants)
            team_sizes[str(size)] = team_sizes.get(str(size), 0) + 1

        return jsonify({
            'role_distribution': role_counts,
            'experience_distribution': experience_counts,
            'team_size_distribution': team_sizes,
            'total_participants': len(participants),
            'total_teams': len(teams),
            'unassigned_participants': len([p for p in participants if p.team_id is None])
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching stats: {str(e)}'
        })


# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
