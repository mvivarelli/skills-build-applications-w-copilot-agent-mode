from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from octofit_tracker import settings

from pymongo import MongoClient

# Sample data for superheroes, teams, activities, leaderboard, workouts
USERS = [
    {"name": "Clark Kent", "email": "superman@dc.com", "team": "DC"},
    {"name": "Bruce Wayne", "email": "batman@dc.com", "team": "DC"},
    {"name": "Diana Prince", "email": "wonderwoman@dc.com", "team": "DC"},
    {"name": "Tony Stark", "email": "ironman@marvel.com", "team": "Marvel"},
    {"name": "Steve Rogers", "email": "captainamerica@marvel.com", "team": "Marvel"},
    {"name": "Natasha Romanoff", "email": "blackwidow@marvel.com", "team": "Marvel"},
]

TEAMS = [
    {"name": "Marvel", "members": ["Tony Stark", "Steve Rogers", "Natasha Romanoff"]},
    {"name": "DC", "members": ["Clark Kent", "Bruce Wayne", "Diana Prince"]},
]

ACTIVITIES = [
    {"user": "Clark Kent", "activity": "Flight", "duration": 60},
    {"user": "Tony Stark", "activity": "Suit Training", "duration": 45},
    {"user": "Diana Prince", "activity": "Combat", "duration": 50},
]

LEADERBOARD = [
    {"user": "Clark Kent", "points": 100},
    {"user": "Tony Stark", "points": 95},
    {"user": "Diana Prince", "points": 90},
]

WORKOUTS = [
    {"name": "Super Strength", "description": "Heavy lifting and resistance training."},
    {"name": "Agility Drills", "description": "Speed and agility exercises."},
]

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Insert test data
        db.users.insert_many(USERS)
        db.teams.insert_many(TEAMS)
        db.activities.insert_many(ACTIVITIES)
        db.leaderboard.insert_many(LEADERBOARD)
        db.workouts.insert_many(WORKOUTS)

        # Ensure unique index on email
        db.users.create_index([("email", 1)], unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
