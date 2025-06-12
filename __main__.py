from src.garmin.client import Garmin
from src.claude.client import Claude
import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    email = os.getenv("GARMIN_EMAIL")
    password = os.getenv("GARMIN_PASSWORD")
    api_key = os.getenv("CLAUDE_API_KEY")
    
    if not all([email, password, api_key]):
        raise ValueError("Missing required environment variables. Please check your .env file.")
    
    # Type assertions since we've verified they're not None
    assert email is not None
    assert password is not None
    assert api_key is not None
    
    with Garmin(email=email, password=password, return_on_mfa=True) as garmin_client:
        print("Connected to Garmin Connect")
        claude = Claude(api_key=api_key, garmin_client=garmin_client)
        
        print("\n=== TrainMe Workout Generator ===")
        print("Tell Claude what kind of running workout you want to create.")
        print("Example: 'Create a 5k tempo run with warm-up and cool-down'")
        print("Type 'quit' to exit.\n")
        
        while True:
            user_input = input("Workout request: ").strip()
            
            if user_input.lower() == 'quit':
                break
                
            if not user_input:
                continue
                
            print("\nGenerating workout with Claude...")
            response, workouts = claude.chat_complete(user_input)
            print(f"Claude: {response}")
            
            if workouts and len(workouts) > 0:
                print("\nWorkout Details:")
                for workout in workouts:
                    print(workout)
            
            # TODO: Parse Claude's response into a workout and upload to Garmin

if __name__ == "__main__":
    main()
