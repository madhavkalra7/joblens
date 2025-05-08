import streamlit as st
import streamlit.components.v1 as components
import sqlite3
from datetime import datetime
import pandas as pd
import time
import json

class FeedbackManager:
    def __init__(self):
        self.db_path = "feedback/feedback.db"
        self.setup_database()
        # Set your email here for FormSubmit
        self.formsubmit_email = "madhavkalra2005@gmail.com"  # Replace with your actual email

    def setup_database(self):
        """Create feedback table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rating INTEGER,
                usability_score INTEGER,
                feature_satisfaction INTEGER,
                missing_features TEXT,
                improvement_suggestions TEXT,
                user_experience TEXT,
                timestamp DATETIME
            )
        ''')
        conn.commit()
        conn.close()

    def save_feedback(self, feedback_data):
        """Save feedback to database"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            INSERT INTO feedback (
                rating, usability_score, feature_satisfaction,
                missing_features, improvement_suggestions,
                user_experience, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            feedback_data['rating'],
            feedback_data['usability_score'],
            feedback_data['feature_satisfaction'],
            feedback_data['missing_features'],
            feedback_data['improvement_suggestions'],
            feedback_data['user_experience'],
            datetime.now()
        ))
        conn.commit()
        conn.close()
        
    def send_email_notification(self, feedback_data):
        """Send email notification using FormSubmit via an HTML form"""
        try:
            # Format the data for the email
            formatted_data = f"""
                Rating: {feedback_data['rating']}/5
                Usability Score: {feedback_data['usability_score']}/5
                Feature Satisfaction: {feedback_data['feature_satisfaction']}/5
                
                Missing Features:
                {feedback_data['missing_features'] or "None provided"}
                
                Improvement Suggestions:
                {feedback_data['improvement_suggestions'] or "None provided"}
                
                User Experience:
                {feedback_data['user_experience'] or "None provided"}
                
                Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            """
            
            # Create a hidden form using FormSubmit's service
            form_html = f"""
            <form id="formsubmit-form" action="https://formsubmit.co/{self.formsubmit_email}" method="POST" style="display:none;">
                <input type="hidden" name="_subject" value="New Feedback Submission - Smart Resume AI">
                <input type="hidden" name="feedback_data" value="{formatted_data.replace('"', '&quot;')}">
                <input type="hidden" name="_captcha" value="false">
                <input type="hidden" name="_template" value="table">
                <button type="submit" id="form-submit-button">Send</button>
            </form>
            <script>
                document.getElementById('formsubmit-form').submit();
            </script>
            """
            
            # Display the form (this will auto-submit)
            st.components.v1.html(form_html, height=0)
            return True
            
        except Exception as e:
            st.error(f"Error sending email notification: {str(e)}")
            return False

    def get_feedback_stats(self):
        """Get feedback statistics"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM feedback", conn)
        conn.close()
        
        if df.empty:
            return {
                'avg_rating': 0,
                'avg_usability': 0,
                'avg_satisfaction': 0,
                'total_responses': 0
            }
        
        return {
            'avg_rating': df['rating'].mean(),
            'avg_usability': df['usability_score'].mean(),
            'avg_satisfaction': df['feature_satisfaction'].mean(),
            'total_responses': len(df)
        }

    def render_feedback_form(self):
        """Render the feedback form"""
        # Apply only CSS fixes for the text areas
        st.markdown("""
            <style>
            /* Fix for the black line issue with text areas */
            .stTextArea textarea {
                background-color: #f0f2f6 !important;
                color: #262730 !important;
                border: 1px solid #ccc !important;
                border-radius: 4px !important;
            }
            </style>
        """, unsafe_allow_html=True)

        st.markdown('<h2>📝 Share Your Feedback</h2>', unsafe_allow_html=True)

        # Overall Rating
        st.markdown('<label><b>Overall Experience Rating</b></label>', unsafe_allow_html=True)
        rating = st.slider("Overall Rating", 1, 5, 5, help="Rate your overall experience with the app")
        st.markdown(f'{"⭐" * rating}', unsafe_allow_html=True)

        # Usability Score
        st.markdown('<label><b>How easy was it to use our app?</b></label>', unsafe_allow_html=True)
        usability_score = st.slider("Usability Score", 1, 5, 5, help="Rate the app's ease of use")
        st.markdown(f'{"⭐" * usability_score}', unsafe_allow_html=True)

        # Feature Satisfaction
        st.markdown('<label><b>How satisfied are you with our features?</b></label>', unsafe_allow_html=True)
        feature_satisfaction = st.slider("Feature Satisfaction", 1, 5, 5, help="Rate your satisfaction with the app's features")
        st.markdown(f'{"⭐" * feature_satisfaction}', unsafe_allow_html=True)

        # Text Feedback - Using default Streamlit components but with CSS fix applied above
        st.markdown('<label><b>What features would you like to see added?</b></label>', unsafe_allow_html=True)
        missing_features = st.text_input("Missing Features", placeholder="Share your feature requests...")

        st.markdown('<label><b>How can we improve?</b></label>', unsafe_allow_html=True)
        improvement_suggestions = st.text_input("Improvement Suggestions", placeholder="Your suggestions for improvement...")

        st.markdown('<label><b>Tell us about your experience</b></label>', unsafe_allow_html=True)
        user_experience = st.text_area("User Experience", placeholder="Share your experience with us...")

        # Submit Button
        if st.button("Submit Feedback", key="submit_feedback"):
            try:
                # Create progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Simulate processing with animation
                for i in range(100):
                    progress_bar.progress(i + 1)
                    if i < 30:
                        status_text.text("Processing feedback... 📝")
                    elif i < 60:
                        status_text.text("Analyzing responses... 🔍")
                    elif i < 90:
                        status_text.text("Saving to database... 💾")
                    else:
                        status_text.text("Finalizing... ✨")
                    time.sleep(0.01)

                # Save feedback
                feedback_data = {
                    'rating': rating,
                    'usability_score': usability_score,
                    'feature_satisfaction': feature_satisfaction,
                    'missing_features': missing_features,
                    'improvement_suggestions': improvement_suggestions,
                    'user_experience': user_experience
                }
                self.save_feedback(feedback_data)
                
                # Clear progress elements
                progress_bar.empty()
                status_text.empty()
                 
                # Show success message with animation
                success_container = st.empty()
                success_container.markdown("""
                    <div style="text-align: center; padding: 20px; background: linear-gradient(90deg, rgba(76, 175, 80, 0.1), rgba(33, 150, 243, 0.1)); border-radius: 10px;">
                        <h2 style="color: #4CAF50;">Thank You! 🎉</h2>
                        <p>Your feedback helps us improve Smart Resume AI</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Send email notification
                email_sent = self.send_email_notification(feedback_data)
                
                # Show balloons animation
                st.balloons()
                
                # Keep success message visible
                time.sleep(2)
                
            except Exception as e:
                st.error(f"Error submitting feedback: {str(e)}")

    def render_feedback_stats(self):
        """Render feedback statistics"""
        stats = self.get_feedback_stats()
        
        st.markdown("""
            <div style="text-align: center; padding: 15px; background: linear-gradient(90deg, rgba(76, 175, 80, 0.1), rgba(33, 150, 243, 0.1)); border-radius: 10px; margin-bottom: 20px;">
                <h3>Feedback Overview 📊</h3>
            </div>
        """, unsafe_allow_html=True)
        
        cols = st.columns(4)
        metrics = [
            {"label": "Total Responses", "value": f"{stats['total_responses']:,}", "delta": "↗"},
            {"label": "Avg Rating", "value": f"{stats['avg_rating']:.1f}/5.0", "delta": "⭐"},
            {"label": "Usability Score", "value": f"{stats['avg_usability']:.1f}/5.0", "delta": "🎯"},
            {"label": "Satisfaction", "value": f"{stats['avg_satisfaction']:.1f}/5.0", "delta": "😊"}
        ]
        
        for col, metric in zip(cols, metrics):
            col.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 8px; text-align: center;">
                    <div style="color: #B0B0B0; font-size: 0.9em;">{metric['label']}</div>
                    <div style="font-size: 1.5em; color: #4CAF50; margin: 5px 0;">{metric['value']}</div>
                    <div style="font-size: 1.2em;">{metric['delta']}</div>
                </div>
            """, unsafe_allow_html=True)
