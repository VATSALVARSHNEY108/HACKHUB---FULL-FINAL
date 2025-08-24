from datetime import datetime
from sqlalchemy import JSON
from database import db


class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)  # Developer, Designer, PM, etc.
    experience_level = db.Column(db.String(20), nullable=False)  # Beginner, Intermediate, Advanced
    skills = db.Column(JSON, nullable=False)  # List of skills
    interests = db.Column(JSON, nullable=False)  # List of interests
    preferred_team_size = db.Column(db.Integer, default=4)
    availability = db.Column(db.String(50), nullable=False)  # Full-time, Part-time
    github_url = db.Column(db.String(200))
    linkedin_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)

    def __init__(self, **kwargs):
        """Initialize Participant with keyword arguments"""
        super().__init__(**kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'experience_level': self.experience_level,
            'skills': self.skills,
            'interests': self.interests,
            'preferred_team_size': self.preferred_team_size,
            'availability': self.availability,
            'github_url': self.github_url,
            'linkedin_url': self.linkedin_url,
            'team_id': self.team_id
        }


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    project_idea = db.Column(db.Text)
    tech_stack = db.Column(JSON)  # List of technologies
    balance_score = db.Column(db.Float, default=0.0)  # Team balance metric
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    participants = db.relationship('Participant', backref='team', lazy=True)

    def __init__(self, **kwargs):
        """Initialize Team with keyword arguments"""
        super().__init__(**kwargs)

    def to_dict(self):
        participants_list = []
        try:
            # Safely access the relationship with proper loading
            if hasattr(self, 'participants') and self.participants is not None:
                # Query the participants directly to avoid relationship issues
                from database import db
                participants_list = db.session.query(Participant).filter_by(team_id=self.id).all()
        except (AttributeError, TypeError, Exception):
            participants_list = []
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'project_idea': self.project_idea,
            'tech_stack': self.tech_stack,
            'balance_score': self.balance_score,
            'participant_count': len(participants_list),
            'participants': [p.to_dict() for p in participants_list],
        }



