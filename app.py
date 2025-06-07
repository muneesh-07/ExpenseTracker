import time
import re
from datetime import datetime, timedelta
from database.manager import DatabaseManager
from ai.nlp_processor import FreeNLP
from ai.local_llm import FreeAIAssistant
from utils.voice import FreeVoiceAssistant
from utils.helpers import format_table

class ExpenseTrackerApp:
    def __init__(self):
        print("Initializing Expense Tracker AI...")
        self.db = DatabaseManager()
        self.nlp = FreeNLP()
        self.ai = FreeAIAssistant()
        self.voice = FreeVoiceAssistant()
        self.mode = "text"
        self.running = True
        print("System ready!\n")

    def start(self):
        print("Welcome to Gene - Your AI Expense Tracker!")
        print("Type 'help' for available commands\n")

        try:
            while self.running:
                if self.mode == "voice":
                    self._process_voice_command()
                else:
                    self._process_text_command()
        except KeyboardInterrupt:
            self.shutdown()

    def _process_text_command(self):
        user_input = input("You: ").strip()
        
        if not user_input:
            return
            
        if user_input.lower() in ['q', 'quit', 'exit']:
            self.shutdown()
        elif user_input.lower() in ['v', 'voice']:
            self._switch_to_voice()
        elif user_input.lower() == 'help':
            self._show_help()
        else:
            self._handle_command(user_input, voice_feedback=False)

    def _process_voice_command(self):
        print("\n🎤 Voice Mode Activated (say 'exit' to quit)")
        self.voice.speak("Voice mode activated. Speak your command.")
        
        while self.mode == "voice":
            try:
                text = self.voice.listen()
                if not text:
                    continue
                    
                print(f"\nYou said: {text}")
                
                if any(word in text.lower() for word in ['exit', 'quit', 'text mode']):
                    self._switch_to_text()
                    break
                    
                self._handle_command(text, voice_feedback=True)
                
            except Exception as e:
                print(f"Error: {str(e)}")
                self.voice.speak("Sorry, I didn't catch that")

    def _handle_command(self, text, voice_feedback):
        try:
            text_lower = text.lower()
            
            if self._is_expense_entry(text_lower):
                expense = self._parse_expense_with_context(text)
                if expense['amount']:
                    self.db.add_expense(expense)
                    response = f"Added ₹{expense['amount']:.2f} for {expense['category']} on {expense['date']}"
                else:
                    response = "Please include an amount like '500 for food'"
            
            elif any(word in text_lower for word in ['show', 'list', 'how much']):
                filters = self._get_date_filters(text_lower)
                expenses = self.db.get_expenses(filters)
                
                if not expenses:
                    response = "No expenses found"
                elif "total" in text_lower:
                    total = sum(float(exp[2]) for exp in expenses)
                    response = f"Total spent: ₹{total:.2f}"
                else:
                    response = format_table(expenses)
            
            else:
                response = self.ai.generate_response(text)
                
            print(f"\nGene: {response}")
            if voice_feedback:
                self.voice.speak(response)
                
        except Exception as e:
            error_msg = f"Error processing command: {str(e)}"
            print(error_msg)
            if voice_feedback:
                self.voice.speak("Sorry, I didn't understand that")

    def _parse_expense_with_context(self, text):
        """Parse natural language expense entries"""
        text_lower = text.lower()
        
        # Extract amount
        amount_match = re.search(r'(?:spent|used|paid|₹|rs|rupees?)\s*(\d+(?:\.\d{1,2})?)', text_lower)
        amount = float(amount_match.group(1)) if amount_match else None
        
        # Extract category
        category = "other"
        if " for " in text_lower:
            category = text_lower.split(" for ")[-1].split(" on ")[0].strip()
        elif " on " in text_lower:
            category = text_lower.split(" on ")[-1].split(" for ")[0].strip()
        
        # Clean category
        category = ' '.join([word for word in category.split() 
                           if not word.replace('.', '').isdigit()])
        
        # Extract date
        date = datetime.now().date()
        if "yesterday" in text_lower:
            date -= timedelta(days=1)
        elif "last week" in text_lower:
            date -= timedelta(weeks=1)
        
        return {
            'amount': amount,
            'category': category.title(),
            'date': date.isoformat()
        }

    def _get_date_filters(self, text):
        """Generate date filters based on time references"""
        today = datetime.now().date()
        filters = {}
        
        if "this week" in text:
            start = today - timedelta(days=today.weekday())
            filters = {
                'start_date': start.isoformat(),
                'end_date': today.isoformat()
            }
        elif "last week" in text:
            start = today - timedelta(days=today.weekday() + 7)
            end = start + timedelta(days=6)
            filters = {
                'start_date': start.isoformat(),
                'end_date': end.isoformat()
            }
        elif "today" in text:
            filters = {'date': today.isoformat()}
            
        return filters

    def _is_expense_entry(self, text):
        return (any(word in text for word in ['spent', 'used', 'paid', '₹', 'rs', 'rupees']) 
                and any(word in text for word in ['for', 'on']))

    def _switch_to_voice(self):
        self.mode = "voice"
        print("Switching to voice mode...")

    def _switch_to_text(self):
        self.mode = "text"
        print("\nText mode activated")

    def _show_help(self):
        help_text = """
        Available Commands:
        - Add expense: "500 for food" or "spent 1000 on shopping"
        - View expenses: "show this week" or "how much last week"
        - Voice mode: "voice"
        - Exit: "quit" or "exit"

        Examples:
        - "I spent 500 for dinner yesterday"
        - "Show expenses from last week"
        - "How much did I spend today"
        - "750 rupees for taxi"
        """
        print(help_text)

    def shutdown(self):
        self.running = False
        print("\nGoodbye!")
        if hasattr(self, 'voice'):
            self.voice.speak("Goodbye")
        exit()

if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.start()