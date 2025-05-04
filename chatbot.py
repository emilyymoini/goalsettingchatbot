import os
import json
from datetime import datetime
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

class GoalSettingChatbot:
    def __init__(self):
        self.goals = {
            "monthly": [],
            "weekly": [],
            "daily": []
        }
        self.load_goals()

    def save_goals(self):
        """Save goals to a JSON file"""
        with open('goals.json', 'w') as f:
            json.dump(self.goals, f)

    def load_goals(self):
        """Load goals from JSON file if it exists"""
        try:
            with open('goals.json', 'r') as f:
                self.goals = json.load(f)
        except FileNotFoundError:
            pass

    def add_goal(self, goal_type, goal):
        """Add a new goal"""
        if goal_type in self.goals:
            self.goals[goal_type].append(goal)
            self.save_goals()
            return True
        return False

    def get_chatbot_response(self, prompt, context=""):
        """Get response from OpenAI's GPT model"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": """You are a goal-setting coach focused on helping users set and achieve ambitious goals.
                    Your approach includes:
                    1. Helping users set clear, measurable goals
                    2. Encouraging users to think bigger and be more ambitious
                    3. Providing constructive feedback on goal alignment
                    4. Maintaining a supportive and motivating tone"""},
                    {"role": "user", "content": f"{context}\n\nUser input: {prompt}"}
                ],
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

    def display_goals(self):
        """Display all current goals"""
        print("\nCurrent Goals:")
        for goal_type, goals in self.goals.items():
            print(f"\n{goal_type.capitalize()} Goals:")
            for i, goal in enumerate(goals, 1):
                print(f"{i}. {goal}")

def main():
    chatbot = GoalSettingChatbot()
    print("Welcome to your Goal Setting Assistant!")
    print("I'm here to help you set and achieve ambitious goals.")
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Add a new goal")
        print("2. View current goals")
        print("3. Get goal feedback")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "1":
            print("\nWhat type of goal would you like to add?")
            print("1. Monthly")
            print("2. Weekly")
            print("3. Daily")
            goal_choice = input("Enter your choice (1-3): ")
            
            goal_types = {
                "1": "monthly",
                "2": "weekly",
                "3": "daily"
            }
            
            if goal_choice in goal_types:
                goal = input(f"\nEnter your {goal_types[goal_choice]} goal: ")
                chatbot.add_goal(goal_types[goal_choice], goal)
                
                # Get feedback on the goal
                context = f"The user has set a {goal_types[goal_choice]} goal: {goal}"
                feedback = chatbot.get_chatbot_response("Please provide feedback on this goal and suggest how it could be more ambitious or impactful.", context)
                print("\nFeedback from your goal coach:")
                print(feedback)
                
        elif choice == "2":
            chatbot.display_goals()
            
        elif choice == "3":
            chatbot.display_goals()
            goal_feedback = chatbot.get_chatbot_response(
                "Please review my current goals and provide feedback on how they align and how I could make them more ambitious.",
                f"Current goals: {json.dumps(chatbot.goals, indent=2)}"
            )
            print("\nFeedback from your goal coach:")
            print(goal_feedback)
            
        elif choice == "4":
            print("Thank you for using the Goal Setting Assistant. Keep pushing towards your goals!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
