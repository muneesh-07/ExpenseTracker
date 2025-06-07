import re
from datetime import datetime, timedelta

class FreeNLP:
    def __init__(self):
        self.amount_pattern = re.compile(r'(?:₹|rs|rupees?)\s*(\d+(?:\.\d{1,2})?)', re.IGNORECASE)
        self.date_keywords = {
            'today': 0,
            'yesterday': -1,
            'tomorrow': 1,
            'last week': -7
        }

    def parse_expense(self, text):
        # Extract amount
        amount_match = self.amount_pattern.search(text.lower())
        amount = float(amount_match.group(1)) if amount_match else None
        
        # Extract date
        date = self._parse_date(text)
        
        # Extract category (everything after "for")
        category = "other"
        if " for " in text.lower():
            category = text.lower().split(" for ")[-1].split(" on ")[0].strip()
            category = " ".join([w for w in category.split() if not w.isdigit()])
        
        return {
            'amount': amount,
            'date': date,
            'category': category.title() if category else "Other"
        }

    def _parse_date(self, text):
        text_lower = text.lower()
        for keyword, delta in self.date_keywords.items():
            if keyword in text_lower:
                return (datetime.now() + timedelta(days=delta)).date().isoformat()
        return datetime.now().date().isoformat()