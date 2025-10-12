
import re
from collections import Counter
from modules.logger import system_logger, log_provenance

# A simple list of common English stop words
STOP_WORDS = set([
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
    'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
    'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this',
    'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
    'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
    'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',
    'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from',
    'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
    'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
    'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y'
])

class EchoAgent:
    def process_transcript(self, transcript_text):
        system_logger.info("EchoAgent processing transcript.")
        
        summary = self._summarize(transcript_text)
        
        log_provenance(
            agent_name="EchoAgent",
            action="SummarizeTranscript",
            details=f"Generated summary of {len(summary.split())} words."
        )
        
        return summary, transcript_text

    def _summarize(self, text, num_sentences=3):
        # 1. Split text into sentences
        sentences = re.split(r'[\.!?] ', text)
        if not sentences:
            return ""

        # 2. Get word frequencies
        words = re.findall(r'\w+', text.lower())
        word_freq = Counter(word for word in words if word not in STOP_WORDS)

        # 3. Score sentences
        sentence_scores = {}
        for sentence in sentences:
            sentence_words = re.findall(r'\w+', sentence.lower())
            score = sum(word_freq[word] for word in sentence_words)
            # Store sentence with a minimum length to avoid fragments
            if len(sentence) > 20:
                sentence_scores[sentence] = score

        # 4. Get top N sentences
        top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
        
        return ' '.join(top_sentences)

# Singleton instance
echo_agent = EchoAgent()
