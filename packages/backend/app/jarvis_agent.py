from modules.voice_narrator import narrator
from modules.logger import log_provenance
from modules.system_monitor import get_system_status
from modules.corpus_manager import corpus_manager

class JarvisAgent:
    def analyze(self, file_path, nlp_results):
        classification = nlp_results.get('classification')
        entities = nlp_results.get('entities', {})

        narrator.say(f"JARVIS agent analyzing {classification} document.")
        
        log_provenance(
            agent_name="JARVIS",
            action="AnalyzeDocument",
            details=f"File: {file_path}, Classification: {classification}, Entities Found: {len(entities)}"
        )

        if entities:
            log_provenance(
                agent_name="JARVIS",
                action="ExtractEntities",
                details=str(entities)
            )
        
        # --- Corpus Integration Task ---
        self.check_terms_in_corpus(nlp_results.get('text_content', ''))

        # --- System Integration Task ---
        system_status = get_system_status()
        log_provenance(
            agent_name="JARVIS",
            action="CheckSystemStatus",
            details=str(system_status)
        )

    def check_terms_in_corpus(self, text_content):
        """Looks for known legal terms in the text and logs their definitions."""
        definitions = corpus_manager.knowledge.get('black_law_dictionary.json', {})
        for term, definition in definitions.items():
            if term in text_content.lower():
                log_provenance(
                    agent_name="JARVIS",
                    action="CorpusLookup",
                    details=f"Found term '{term}'. Definition: {definition}"
                )

# Singleton instance
jarvis_agent = JarvisAgent()