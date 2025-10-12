import sys
import os
import json
from datetime import datetime

# Add modules to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules')))

from agents.JARVIS.jarvis_agent import extract_clauses, detect_contradictions, analyze_legal_structure
from agents.FRIDAY.friday_agent import interpret_tone, suggest_remedy, analyze_legal_risk, generate_legal_summary, log_provenance
from modules.remedy_synthesizer import RemedySynthesizer
from modules.situation_interpreter import SituationInterpreter
from modules.provenance_logger import get_provenance_logger, log_provenance as log_provenance_entry
from modules.sovereignty_scorer import get_sovereignty_scorer, score_sovereignty


class VeroBrixSystem:
    """
    Enhanced VeroBrix Sovereign Modular Intelligence System.
    Integrates all modules for comprehensive legal analysis with provenance logging and sovereignty scoring.
    """

    def __init__(self):
        self.remedy_synthesizer = RemedySynthesizer()
        self.situation_interpreter = SituationInterpreter()
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Initialize architecture components
        self.provenance_logger = get_provenance_logger()
        self.sovereignty_scorer = get_sovereignty_scorer()

        # Ensure output directories exist
        os.makedirs("logs", exist_ok=True)
        os.makedirs("output", exist_ok=True)
        os.makedirs("logs/provenance", exist_ok=True)

        # Log system initialization
        self.provenance_logger.log_action(
            action_type="system_init",
            action_description=f"VeroBrix Sovereign Intelligence System initialized - Session: {self.session_id}",
            agent_name="VeroBrixSystem"
        )
        log_provenance("VeroBrixSystem", f"Initialized new session: {self.session_id}")

    def analyze_situation(self, input_text: str, situation_context: dict = None) -> dict:
        """
        Performs a comprehensive analysis of a legal situation using all VeroBrix modules.
        Returns a dictionary containing the complete analysis results.
        """
        log_provenance("VeroBrixSystem", "Starting comprehensive situation analysis")

        # Step 1: Interpret situation
        situation = self.situation_interpreter.interpret_situation(input_text, situation_context)

        # Step 2–4: JARVIS analysis
        clauses = extract_clauses(input_text)
        contradictions = detect_contradictions(clauses)
        legal_structure = analyze_legal_structure(input_text)

        # Step 5–6: FRIDAY analysis
        tone_analysis = interpret_tone(input_text)
        legal_risks = analyze_legal_risk(input_text)
        legal_summary = generate_legal_summary(input_text, tone_analysis, legal_risks)

        # Step 7: Sovereignty scoring
        self.provenance_logger.log_action(
            action_type="sovereignty_analysis",
            action_description="Analyzing sovereignty alignment of input text",
            agent_name="SovereigntyScorer",
            input_data=input_text[:200] + "..." if len(input_text) > 200 else input_text
        )
        sovereignty_metrics = self.sovereignty_scorer.score_text(input_text, context="legal_document")

        # Step 8: Remedy synthesis
        remedy_input = {
            'type': situation['type'],
            'risk_level': legal_summary['risk_level'],
            'contradictions': contradictions,
            'tone_analysis': tone_analysis,
            'urgency': situation['urgency'],
            'jurisdiction': situation['jurisdiction'],
            'legal_framework': situation['legal_framework']
        }
        remedy = self.remedy_synthesizer.synthesize_remedy(remedy_input)

        # Score remedy
        remedy_sovereignty = self.sovereignty_scorer.score_decision({
            'description': remedy.get('description', ''),
            'reasoning': remedy.get('reasoning', ''),
            'recommendations': remedy.get('legal_strategies', []),
            'remedy_type': remedy.get('type', 'unknown')
        })

        # Log final analysis
        self.provenance_logger.log_action(
            action_type="analysis_complete",
            action_description="Comprehensive VeroBrix analysis completed",
            agent_name="VeroBrixSystem",
            input_data={"text_length": len(input_text), "situation_type": situation['type']},
            output_data={"sovereignty_score": sovereignty_metrics.overall_score, "remedy_score": remedy_sovereignty.overall_score},
            sovereignty_score=sovereignty_metrics.overall_score,
            confidence_level=0.9,
            legal_context=situation['jurisdiction']['primary']
        )

        # Compile results
        results = {
            'session_id': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'system_version': 'VeroBrix v2.0 - Sovereign Modular Intelligence',
            'input': {'raw_text': input_text, 'context': situation_context},
            'situation_analysis': situation,
            'legal_analysis': {
                'clauses': clauses,
                'contradictions': contradictions,
                'legal_structure': legal_structure,
                'tone_analysis': tone_analysis,
                'legal_risks': legal_risks,
                'legal_summary': legal_summary
            },
            'sovereignty_analysis': {
                'input_sovereignty': sovereignty_metrics.to_dict(),
                'remedy_sovereignty': remedy_sovereignty.to_dict()
            },
            'remedy': remedy,
            'recommendations': self._generate_recommendations(situation, legal_summary, remedy, sovereignty_metrics)
        }

        self._save_analysis_results(results)
        log_provenance("VeroBrixSystem", "Comprehensive analysis completed")
        return results
    def _generate_recommendations(self, situation: dict, legal_summary: dict, remedy: dict, sovereignty_metrics=None) -> dict:
        """
        Generates prioritized recommendations based on the analysis, including sovereignty considerations.
        """
        recommendations = {
            'immediate_actions': [],
            'short_term_actions': [],
            'long_term_actions': [],
            'warnings': [],
            'opportunities': [],
            'sovereignty_improvements': []
        }

        # Sovereignty-based recommendations
        if sovereignty_metrics:
            level = sovereignty_metrics.sovereignty_level
            if level == "Servile":
                recommendations['warnings'].append("SOVEREIGNTY WARNING: Language contains servile patterns")
                recommendations['sovereignty_improvements'].extend(sovereignty_metrics.improvement_suggestions)
            elif level == "Transitional":
                recommendations['opportunities'].append("SOVEREIGNTY OPPORTUNITY: Transitional language—can be improved")
                recommendations['sovereignty_improvements'].extend(sovereignty_metrics.improvement_suggestions[:3])
            else:
                recommendations['opportunities'].append("SOVEREIGNTY STRENGTH: Language demonstrates sovereign principles")

            if sovereignty_metrics.overall_score < 0.4:
                recommendations['immediate_actions'].append("CRITICAL: Review language for servile patterns")

        # Urgency-based actions
        if situation['urgency']['level'] == 'high':
            recommendations['immediate_actions'].extend([
                "URGENT: Time-sensitive situation detected",
                "Review all deadlines immediately",
                "Consider emergency legal consultation"
            ])

        # Risk-based actions
        if legal_summary['risk_level'] == 'HIGH':
            recommendations['immediate_actions'].append("HIGH RISK: Seek immediate legal counsel")
            recommendations['warnings'].append("Situation contains high-risk legal elements")

        # Contradiction-based actions
        if remedy.get('contradictions'):
            recommendations['short_term_actions'].append("Challenge contradictory provisions in documents")

        # Situation-type actions
        situation_actions = {
            'traffic_stop': {
                'immediate': ["Document all details", "Preserve any evidence"],
                'short_term': ["Review citation for errors", "Research applicable traffic laws"],
                'long_term': ["Challenge jurisdiction", "File administrative remedy if applicable"]
            },
            'fee_demand': {
                'immediate': ["Do not pay without challenging authority", "Request fee schedule"],
                'short_term': ["Challenge lawful authority", "Demand due process hearing"],
                'long_term': ["File administrative appeal", "Consider legal action if rights violated"]
            },
            'court_summons': {
                'immediate': ["Calculate response deadline", "Preserve all rights"],
                'short_term': ["File appropriate response", "Challenge jurisdiction if applicable"],
                'long_term': ["Prepare defense strategy", "Consider counterclaims if applicable"]
            }
        }

        if situation['type'] in situation_actions:
            actions = situation_actions[situation['type']]
            recommendations['immediate_actions'].extend(actions.get('immediate', []))
            recommendations['short_term_actions'].extend(actions.get('short_term', []))
            recommendations['long_term_actions'].extend(actions.get('long_term', []))

        # Tone and jurisdiction-based opportunities
        if legal_summary.get('tone_summary') == 'positive':
            recommendations['opportunities'].append("Document contains favorable language—preserve these terms")

        if situation['jurisdiction']['primary'] == 'commercial':
            recommendations['opportunities'].append("Commercial jurisdiction may provide UCC protections")

        return recommendations

    def _save_analysis_results(self, results: dict):
        """
        Saves the analysis results to a JSON file in the output directory.
        """
        filename = f"output/verobrix_analysis_{self.session_id}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            log_provenance("VeroBrixSystem", f"Analysis results saved to {filename}")
        except Exception as e:
            log_provenance("VeroBrixSystem", f"Error saving results: {e}")

    def generate_document(self, template_name: str, variables: dict) -> str:
        """
        Generates a legal document using the remedy synthesizer.
        """
        log_provenance("VeroBrixSystem", f"Generating document: {template_name}")
        return self.remedy_synthesizer.generate_document(template_name, variables)

    def get_available_templates(self) -> list:
        """
        Returns a list of available document templates.
        """
        return self.remedy_synthesizer.get_available_templates()

    def print_analysis_summary(self, results: dict):
        """
        Prints a formatted summary of the analysis results.
        """
        print("\n" + "=" * 60)
        print("VEROBRIX SOVEREIGN INTELLIGENCE ANALYSIS")
        print("=" * 60)

        print(f"Session ID: {results['session_id']}")
        print(f"System Version: {results.get('system_version', 'VeroBrix v2.0')}")
        print(f"Analysis Time: {results['timestamp']}")
        print(f"Situation Type: {results['situation_analysis']['type'].upper()}")
        print(f"Risk Level: {results['legal_analysis']['legal_summary']['risk_level']}")
        print(f"Urgency: {results['situation_analysis']['urgency']['level'].upper()}")

        if 'sovereignty_analysis' in results:
            sovereignty = results['sovereignty_analysis']['input_sovereignty']
            print(f"\n🏛️ SOVEREIGNTY ANALYSIS:")
            print(f"Sovereignty Level: {sovereignty['sovereignty_level']}")
            print(f"Overall Score: {sovereignty['overall_score']:.2f}/1.00")
            print(f"Language Score: {sovereignty['language_score']:.2f}/1.00")
            print(f"Remedy Score: {sovereignty['remedy_score']:.2f}/1.00")
            print(f"Autonomy Score: {sovereignty['autonomy_score']:.2f}/1.00")
            if sovereignty['servile_flags_count'] > 0:
                print(f"⚠️ Servile Language Flags: {sovereignty['servile_flags_count']}")
            if sovereignty['sovereign_indicators_count'] > 0:
                print(f"✅ Sovereign Indicators: {sovereignty['sovereign_indicators_count']}")

        jurisdiction = results['situation_analysis']['jurisdiction']
        print(f"Primary Jurisdiction: {jurisdiction['primary'].upper()}")
        if jurisdiction['secondary']:
            print(f"Secondary Jurisdictions: {', '.join(jurisdiction['secondary']).upper()}")

        entities = results['situation_analysis']['entities']
        if entities['people']:
            print(f"People Involved: {', '.join(entities['people'])}")
        if entities['organizations']:
            print(f"Organizations: {', '.join(entities['organizations'])}")

        contradictions = results['legal_analysis']['contradictions']
        if contradictions:
            print(f"\nCONTRADICTIONS DETECTED: {len(contradictions)}")
            for i, contradiction in enumerate(contradictions, 1):
                if isinstance(contradiction, dict):
                    print(f"{i}. {contradiction.get('description', 'Unknown contradiction')}")
                else:
                    print(f"{i}. {contradiction}")

        risks = results['legal_analysis']['legal_risks']
        if risks:
            print(f"\nLEGAL RISKS IDENTIFIED: {len(risks)}")
            for risk in risks:
                print(f"- {risk['level']} RISK: {risk['description']}")

        immediate = results['recommendations']['immediate_actions']
        if immediate:
            print(f"\nIMMEDIATE ACTIONS REQUIRED:")
            for action in immediate:
                print(f"• {action}")

        warnings = results['recommendations']['warnings']
        if warnings:
            print(f"\nWARNINGS:")
            for warning in warnings:
                print(f"⚠️ {warning}")

        strategies = results['remedy']['legal_strategies']
        if strategies:
            print(f"\nRECOMMENDED LEGAL STRATEGIES:")
            for strategy in strategies:
                print(f"• {strategy}")

        print("\n" + "=" * 60)

    # Additional methods (_generate_recommendations, _save_analysis_results, generate_document, etc.)
    # can be scaffolded next if you'd like.

