import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import random
from collections import defaultdict


class TeamMatcher:

    def __init__(self):
        self.role_weights = {
            'Developer':
            ['Frontend', 'Backend', 'Full Stack', 'Mobile', 'DevOps'],
            'Designer': ['UI/UX', 'Graphic Designer', 'Product Designer'],
            'Product Manager': ['PM', 'Product Owner', 'Scrum Master'],
            'Data Scientist': ['ML Engineer', 'Data Analyst', 'AI Researcher'],
            'Marketing':
            ['Digital Marketing', 'Growth Hacker', 'Content Creator']
        }

        self.experience_scores = {
            'Beginner': 1,
            'Intermediate': 2,
            'Advanced': 3
        }

    def create_balanced_teams(self, participants, target_team_size=4):
        """
        Create balanced teams using clustering and optimization algorithms
        """
        if len(participants) < 2:
            return []

        # Convert participants to feature vectors
        feature_matrix = self._create_feature_matrix(participants)

        # Determine optimal number of teams
        num_teams = max(1, len(participants) // target_team_size)

        # Use K-means clustering for initial grouping
        if len(participants) > num_teams:
            kmeans = KMeans(n_clusters=num_teams,
                            random_state=42,
                            n_init='auto')
            cluster_labels = kmeans.fit_predict(feature_matrix)
        else:
            # If we have fewer participants than desired teams, put everyone in one team
            cluster_labels = [0] * len(participants)
            num_teams = 1

        # Group participants by cluster
        teams = []
        for cluster_id in range(num_teams):
            cluster_participants = [
                participants[i] for i in range(len(participants))
                if cluster_labels[i] == cluster_id
            ]

            if cluster_participants:
                team_data = self._create_team_data(cluster_participants,
                                                   len(teams) + 1)
                teams.append(team_data)

        # Balance teams by redistributing if necessary
        teams = self._balance_teams(teams, target_team_size)

        return teams

    def _create_feature_matrix(self, participants):
        """
        Create feature matrix for participants using skills, role, and experience
        """
        # Combine all skills and interests for TF-IDF
        text_features = []
        role_features = []
        experience_features = []

        for participant in participants:
            # Text features from skills and interests
            skills_text = ' '.join(
                participant.skills) if participant.skills else ''
            interests_text = ' '.join(
                participant.interests) if participant.interests else ''
            combined_text = f"{skills_text} {interests_text}"
            text_features.append(combined_text)

            # Role features (one-hot encoded)
            role_features.append(participant.role)

            # Experience features (numerical)
            experience_features.append(
                self.experience_scores.get(participant.experience_level, 1))

        # Create TF-IDF vectors for skills and interests
        if any(text_features):
            vectorizer = TfidfVectorizer(max_features=50, stop_words='english')
            try:
                sparse_matrix = vectorizer.fit_transform(text_features)
                # Convert sparse matrix to dense numpy array
                from scipy.sparse import issparse
                if issparse(sparse_matrix):
                    text_vectors = sparse_matrix.toarray()
                else:
                    text_vectors = np.array(sparse_matrix)
            except Exception:
                text_vectors = np.zeros((len(participants), 1))
        else:
            text_vectors = np.zeros((len(participants), 1))

        # Create role vectors (simple one-hot)
        unique_roles = list(set(role_features))
        role_vectors = np.zeros((len(participants), len(unique_roles)))
        for i, role in enumerate(role_features):
            if role in unique_roles:
                role_vectors[i, unique_roles.index(role)] = 1

        # Combine all features
        experience_vectors = np.array(experience_features).reshape(-1, 1)

        # Normalize experience to 0-1 range
        if experience_vectors.max() > experience_vectors.min():
            experience_vectors = (
                experience_vectors - experience_vectors.min()) / (
                    experience_vectors.max() - experience_vectors.min())

        feature_matrix = np.hstack(
            [text_vectors, role_vectors, experience_vectors])

        return feature_matrix

    def _create_team_data(self, participants, team_number):
        """
        Create team data structure with balance metrics
        """
        # Calculate balance score
        balance_score = self._calculate_balance_score(participants)

        # Generate team name
        roles = list(set([p.role for p in participants]))
        team_name = f"Team {team_number}"
        if len(roles) <= 2:
            team_name = f"Team {roles[0][:4]}{team_number}"

        # Collect all skills for tech stack suggestion
        all_skills = []
        for p in participants:
            all_skills.extend(p.skills if p.skills else [])

        # Get most common skills as suggested tech stack
        skill_counts = defaultdict(int)
        for skill in all_skills:
            skill_counts[skill] += 1

        suggested_tech_stack = sorted(skill_counts.keys(),
                                      key=lambda x: skill_counts[x],
                                      reverse=True)[:5]

        # Create description
        role_summary = ", ".join(list(set([p.role for p in participants])))
        description = f"A diverse team of {len(participants)} members with roles in {role_summary}."

        return {
            'name': team_name,
            'description': description,
            'participant_ids': [p.id for p in participants],
            'balance_score': balance_score,
            'suggested_tech_stack': suggested_tech_stack
        }

    def _calculate_balance_score(self, participants):
        """
        Calculate team balance score based on role diversity, experience mix, and skill overlap
        """
        if not participants:
            return 0.0

        # Role diversity score (0-1)
        unique_roles = set([p.role for p in participants])
        role_diversity = min(
            len(unique_roles) / min(4, len(participants)), 1.0)

        # Experience diversity score (0-1)
        experiences = [
            self.experience_scores.get(p.experience_level, 1)
            for p in participants
        ]
        if len(set(experiences)) > 1:
            exp_diversity = float(np.std(experiences)) / max(
                experiences) if max(experiences) > 0 else 0
        else:
            exp_diversity = 0.5  # Neutral score for same experience level

        # Skill complementarity score (0-1)
        all_skills = []
        for p in participants:
            all_skills.extend(p.skills if p.skills else [])

        if all_skills:
            unique_skills = len(set(all_skills))
            total_skills = len(all_skills)
            skill_diversity = unique_skills / total_skills if total_skills > 0 else 0
        else:
            skill_diversity = 0

        # Combine scores with weights
        balance_score = (role_diversity * 0.4 + exp_diversity * 0.3 +
                         skill_diversity * 0.3)

        return round(balance_score, 3)

    def _balance_teams(self, teams, target_size):
        """
        Balance team sizes by redistributing members
        """
        if not teams:
            return teams

        # Sort teams by size (smallest first)
        teams.sort(key=lambda t: len(t['participant_ids']))

        # Try to balance team sizes
        for i in range(len(teams) - 1):
            current_team = teams[i]
            next_team = teams[i + 1]

            current_size = len(current_team['participant_ids'])
            next_size = len(next_team['participant_ids'])

            # If there's a significant size difference, try to balance
            if next_size - current_size > 1 and next_size > target_size:
                # Move one member from larger team to smaller team
                moved_participant = next_team['participant_ids'].pop()
                current_team['participant_ids'].append(moved_participant)

                # Recalculate balance scores would require participant objects
                # For simplicity, we'll keep the existing scores

        return teams

    def suggest_team_for_participant(self, participant, existing_teams):
        """
        Suggest the best team for a new participant to join
        """
        if not existing_teams:
            return None

        best_team = None
        best_score = -1

        for team in existing_teams:
            if len(team.participants) >= 5:  # Don't suggest overfull teams
                continue

            # Calculate compatibility score
            compatibility_score = self._calculate_team_compatibility(
                participant, team.participants)

            if compatibility_score > best_score:
                best_score = compatibility_score
                best_team = team

        return best_team

    def _calculate_team_compatibility(self, participant, team_members):
        """
        Calculate how well a participant would fit with a team
        """
        if not team_members:
            return 1.0

        # Role complementarity
        team_roles = set([member.role for member in team_members])
        role_bonus = 0.3 if participant.role not in team_roles else 0.1

        # Skill overlap (some overlap is good, but not too much)
        participant_skills = set(
            participant.skills) if participant.skills else set()
        team_skills = set()
        for member in team_members:
            if member.skills:
                team_skills.update(member.skills)

        if participant_skills and team_skills:
            overlap = len(participant_skills & team_skills)
            total_unique = len(participant_skills | team_skills)
            skill_score = overlap / total_unique if total_unique > 0 else 0
            # Optimal overlap is around 30-50%
            if 0.3 <= skill_score <= 0.5:
                skill_bonus = 0.3
            elif 0.1 <= skill_score < 0.3:
                skill_bonus = 0.2
            else:
                skill_bonus = 0.1
        else:
            skill_bonus = 0.1

        # Experience balance
        team_experiences = [
            self.experience_scores.get(member.experience_level, 1)
            for member in team_members
        ]
        participant_exp = self.experience_scores.get(
            participant.experience_level, 1)

        avg_team_exp = np.mean(team_experiences)
        exp_diff = abs(participant_exp - avg_team_exp)
        exp_bonus = max(0.1, 0.4 - float(exp_diff * 0.1))

        total_score = role_bonus + skill_bonus + exp_bonus
        return min(total_score, 1.0)
