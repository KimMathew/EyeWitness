import mysql.connector
from kivy.uix.image import Image
from database.database import DatabaseManager
from kivymd.uix.screenmanager import MDScreenManager

# Database initialization
database = DatabaseManager()
db = database.get_connection()
cursor = db.cursor()

class CreditScore():
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
        
        
    # Displaying Credit score
    def display_credit_score_image(self, user_id, screen_manager):
        # Fetch the user's credit score from the database
        print(f"Hello {user_id}!")
        try:
            cursor.execute("SELECT CreditScore FROM UserProfile WHERE ProfileID = %s", (user_id,))
            result = cursor.fetchone()
            if result:
                credit_score = result[0]
            else:
                print(f"No credit score found for user_id: {user_id}")
                return
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return
        finally:
            cursor.close()
            db.close()

        # Determine the appropriate image path based on the credit score
        if 81 <= credit_score:
            selected_image_path = 'Assets/Excellent.png'
        elif 61 <= credit_score <= 80:
            selected_image_path = 'Assets/Good.png'
        elif 41 <= credit_score <= 60:
            selected_image_path = 'Assets/Fair.png'
        elif 21 <= credit_score <= 40:
            selected_image_path = 'Assets/Poor.png'
        elif 1 <= credit_score <= 20:
            selected_image_path = 'Assets/VeryPoor.png'
        else:
            selected_image_path = 'Assets/Fair.png'  # Provide a default image for unexpected cases

        # Add the image to the BoxLayout with id 'image_container'
        homescreen = self.screen_manager.get_screen('homescreen')
        image_container = homescreen.ids.image_container
        credit_score_label = homescreen.ids.credit_score_label  # Get the label object
        # Determine the color based on the credit score
        credit_score_color = self.get_credit_score_color(credit_score)
        credit_score_label.color = credit_score_color

        image_container.clear_widgets()
        image_container.add_widget(Image(source=selected_image_path))
        credit_score_label.text = f"Trustiness: {credit_score}"  # Update the label's text
        
    def get_credit_score_color(self, score):
        if score >= 81:
            return (0, 128/255, 55/255, 1)  # Green for excellent scores
        elif score >= 61:
            return (126/255, 217/255, 87/255, 1)  # Darker green for good scores
        elif score >= 41:
            return (237/255, 183/255, 0, 1)  # Yellow for fair scores
        elif score >= 21:
            return (255/255, 118/255, 67/255, 1)  # Orange for poor scores
        else:
            return (231/255, 0, 51/255, 1)  # Red for very poor scores