import os
import json
from modules.logger import system_logger

class CorpusManager:
    def __init__(self, corpus_dir='corpus'):
        self.corpus_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', corpus_dir))
        self.knowledge = {}
        self.term_definitions = {}
        self.load_corpus()
        self._populate_term_definitions()

    def load_corpus(self):
        system_logger.info("Loading legal corpus...")
        try:
            for filename in os.listdir(self.corpus_dir):
                path = os.path.join(self.corpus_dir, filename)
                if filename.endswith(".json"):
                    with open(path, 'r') as f:
                        self.knowledge[filename] = json.load(f)
                elif filename.endswith(".txt") or filename.endswith(".md"):
                    with open(path, 'r') as f:
                        self.knowledge[filename] = f.read()
            system_logger.info(f"Corpus loaded. Knowledge sources: {list(self.knowledge.keys())}")
        except Exception as e:
            system_logger.error(f"Failed to load corpus: {e}")

    def _populate_term_definitions(self):
        # Populate definitions from Black's Law Dictionary (if loaded)
        blacks_law = self.knowledge.get('black_law_dictionary.json', {})
        for term, definition in blacks_law.items():
            self.term_definitions[term.lower()] = definition

        # Add specific interpretations from teachings (example for 'payment')
        # This can be expanded for other terms and other teachers
        self.term_definitions['payment'] = (
            "Mainstream: The act of paying money or other compensation to settle a debt or obligation.\n"
            "Sovereign/Williams: Performance; the act of doing something with a document (e.g., endorsing and returning a bill) that legally discharges a debt. Often linked to the concept of 'payment as performance' rather than just monetary transfer."
        )
        self.term_definitions['performance'] = (
            "Mainstream: The action or process of carrying out or accomplishing an action, task, or function.\n"
            "Sovereign/Williams: The act of fulfilling an obligation, often by processing a document or instrument, which is considered a form of 'payment' in commercial law."
        )
        self.term_definitions['money'] = (
            "Mainstream: A current medium of exchange in the form of coins and banknotes.\n"
            "Sovereign/Williams: Often distinguished from 'legal tender' (Federal Reserve Notes). True money is gold and silver coin (Article 1, Section 10 of US Constitution). All other forms are negotiable instruments (promises or orders to pay)."
        )
        self.term_definitions['legal tender'] = (
            "Mainstream: Currency that must be accepted when offered in payment of a debt.\n"
            "Sovereign/Williams: As per US Constitution Article 1, Section 10, only gold and silver coin can be made a tender in payment of debt. Federal Reserve Notes are considered promissory notes, not true legal tender for debt discharge."
        )
        self.term_definitions['contract'] = (
            "Mainstream: A written or spoken agreement, especially one concerning employment, sales, or tenancy, that is intended to be enforceable by law.\n"
            "Sovereign/Williams: An agreement between parties, but with emphasis on full disclosure, equal consideration, and 'like kind' parties (man with man, corporation with corporation). All interactions are viewed as contracts."
        )

    def get_definition(self, term):
        return self.term_definitions.get(term.lower())

    def get_corpus_text(self, corpus_name):
        return self.knowledge.get(corpus_name, "")

# Singleton instance
corpus_manager = CorpusManager(corpus_dir='corpus')
