# verobrix_app/modules/sovereignty_scorer.py
"""
Scores language for sovereignty, autonomy, and remedy strength.
Evaluates language for servile vs. sovereign patterns.
"""

class SovereigntyScorer:
    def __init__(self):
        pass

    def _calculate_scores(self, text):
        # Placeholder scoring logic
        sovereign_keywords = ["lawful", "right", "remedy", "without prejudice", "private", "notice", "demand"]
        servile_keywords = ["request", "please", "submit", "person", "employee", "permission", "appeal"]

        sovereign_count = sum(text.lower().count(kw) for kw in sovereign_keywords)
        servile_count = sum(text.lower().count(kw) for kw in servile_keywords)

        if sovereign_count + servile_count > 0:
            score = (sovereign_count / (sovereign_count + servile_count))
        else:
            score = 0.5 # Neutral

        level = "Servile"
        if score > 0.7:
            level = "Sovereign"
        elif score > 0.4:
            level = "Transitional"
            
        return {
            "overall_score": score,
            "language_score": score * 0.8, # dummy value
            "remedy_score": score * 0.1, # dummy value
            "autonomy_score": score * 0.1, # dummy value
            "sovereignty_level": level,
            "servile_flags": [kw for kw in servile_keywords if kw in text.lower()],
            "sovereign_indicators": [kw for kw in sovereign_keywords if kw in text.lower()],
            "improvement_suggestions": ["Consider replacing servile language (e.g., 'request') with more assertive, sovereign terms (e.g., 'demand', 'notice').", "Clearly state reservation of rights."]
        }

    def score_text(self, text, context=None):
        """
        Scores the text for sovereignty.
        """
        print("Scoring text for sovereignty...")
        return self._calculate_scores(text)

    def score_decision(self, decision_data):
        """
        Scores a synthesized remedy or decision for sovereignty.
        """
        print("Scoring decision for sovereignty...")
        # Combine text from the decision data for scoring
        text_to_score = " ".join(str(v) for v in decision_data.values())
        return self._calculate_scores(text_to_score)

if __name__ == '__main__':
    scorer = SovereigntyScorer()
    
    sample_text = "I request that you please review my application as a person."
    report = scorer.score_text(sample_text)
    print("---" + " Text Score" + " ---")
    print(report)

    sample_decision = {
        'description': 'Send a notice of default.',
        'reasoning': 'Failure to cure the defect.',
        'remedy_type': 'UCC'
    }
    decision_report = scorer.score_decision(sample_decision)
    print("\n" + "---" + " Decision Score" + " ---")
    print(decision_report)
