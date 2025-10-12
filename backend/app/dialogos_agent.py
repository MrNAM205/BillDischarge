
from modules.logger import log_provenance, system_logger
from modules.corpus_manager import corpus_manager
import re

class DialogosAgent:
    def __init__(self):
        self.carl_miller_teachings = corpus_manager.get_corpus_text('carl_miller_teachings_structured.md')
        if not self.carl_miller_teachings:
            system_logger.warning("Carl Miller teachings not loaded. Dialogos agent will have limited Miller analysis.")

        self.anelia_sutton_teachings = corpus_manager.get_corpus_text('anelia_sutton_teachings_structured.md')
        if not self.anelia_sutton_teachings:
            system_logger.warning("Anelia Sutton teachings not loaded. Dialogos agent will have limited Sutton analysis.")

        self.david_straight_teachings = corpus_manager.get_corpus_text('david_straight_teachings_structured.md')
        if not self.david_straight_teachings:
            system_logger.warning("David Straight teachings not loaded. Dialogos agent will have limited Straight analysis.")

        self.brandon_joe_williams_teachings = corpus_manager.get_corpus_text('brandon_joe_williams_teachings_structured.md')
        if not self.brandon_joe_williams_teachings:
            system_logger.warning("Brandon Joe Williams teachings not loaded. Dialogos agent will have limited Williams analysis.")

        self.common_law_vs_admiralty_overview = corpus_manager.get_corpus_text('common_law_vs_admiralty_overview.md')
        if not self.common_law_vs_admiralty_overview:
            system_logger.warning("Common Law vs. Admiralty overview not loaded. Dialogos agent will have limited jurisdictional analysis.")

        self.color_of_law_overview = corpus_manager.get_corpus_text('color_of_law_overview.md')
        if not self.color_of_law_overview:
            system_logger.warning("Color of Law overview not loaded. Dialogos agent will have limited analysis on official authority.")

        self.constructive_trust_equitable_estoppel_overview = corpus_manager.get_corpus_text('constructive_trust_equitable_estoppel_overview.md')
        if not self.constructive_trust_equitable_estoppel_overview:
            system_logger.warning("Constructive Trust/Equitable Estoppel overview not loaded. Dialogos agent will have limited analysis on these concepts.")

        self.judicial_notice_immunity_overview = corpus_manager.get_corpus_text('judicial_notice_immunity_overview.md')
        if not self.judicial_notice_immunity_overview:
            system_logger.warning("Judicial Notice/Immunity overview not loaded. Dialogos agent will have limited analysis on judicial authority.")

        self.payment_coupon_endorsement_overview = corpus_manager.get_corpus_text('payment_coupon_endorsement_overview.md')
        if not self.payment_coupon_endorsement_overview:
            system_logger.warning("Payment Coupon Endorsement overview not loaded. Dialogos agent will have limited analysis on this topic.")

        self.res_judicata_collateral_estoppel_overview = corpus_manager.get_corpus_text('res_judicata_collateral_estoppel_overview.md')
        if not self.res_judicata_collateral_estoppel_overview:
            system_logger.warning("Res Judicata/Collateral Estoppel overview not loaded. Dialogos agent will have limited analysis on these concepts.")

        self.cfr_interpretation_overview = corpus_manager.get_corpus_text('cfr_interpretation_overview.md')
        if not self.cfr_interpretation_overview:
            system_logger.warning("CFR Interpretation overview not loaded. Dialogos agent will have limited analysis on CFR.")

    def _get_section_from_markdown(self, markdown_text, heading_pattern):
        match = re.search(heading_pattern + r'\n(.*?)(?=\n##|\Z)', markdown_text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return None

    def analyze(self, text_content):
        log_provenance("Dialogos", "AnalyzePhilosophicalOverlays", "Starting analysis from multiple perspectives.")
        
        self.get_sutton_analysis(text_content)
        self.get_miller_analysis(text_content)
        self.get_straight_analysis(text_content)
        self.get_williams_analysis(text_content)
        self._check_key_terms(text_content)

    def _check_key_terms(self, text):
        key_terms = ["payment", "performance", "money", "legal tender", "contract"]
        for term in key_terms:
            if term in text.lower():
                definition = corpus_manager.get_definition(term)
                if definition:
                    log_provenance("Dialogos", f"TermDefinition: {term}", definition)

    def get_sutton_analysis(self, text):
        if self.anelia_sutton_teachings:
            if "presumption" in text.lower() or "presumed" in text.lower():
                snippet = self._get_section_from_markdown(self.anelia_sutton_teachings, r'##.*Challenging Presumptions')
                log_provenance("Dialogos(Sutton)", "ChallengingPresumption", 
                               f"Text mentions presumption. Sutton's view: {snippet[:200]}...")
            if "unlawful authority" in text.lower() or "unlawful command" in text.lower():
                snippet = self._get_section_from_markdown(self.anelia_sutton_teachings, r'##.*Rejection of Unlawful Authority')
                log_provenance("Dialogos(Sutton)", "UnlawfulAuthorityChallenge", 
                               f"Text mentions unlawful authority. Sutton's view: {snippet[:200]}...")
            if "pro se" in text.lower() or "self-representation" in text.lower():
                snippet = self._get_section_from_markdown(self.anelia_sutton_teachings, r'##.*Self-Empowerment')
                log_provenance("Dialogos(Sutton)", "ProSeLitigationContext", 
                               f"Text mentions pro se litigation. Sutton's view: {snippet[:200]}...")
        
        # Constructive Trust / Equitable Estoppel integration
        if self.constructive_trust_equitable_estoppel_overview:
            if "constructive trust" in text.lower():
                snippet = self._get_section_from_markdown(self.constructive_trust_equitable_estoppel_overview, r'##.*Reinterpretation of "Constructive Trust"')
                log_provenance("Dialogos(Sutton)", "ConstructiveTrustReference", 
                               f"Text mentions constructive trust. Overview: {snippet[:200]}...")
            if "equitable estoppel" in text.lower():
                snippet = self._get_section_from_markdown(self.constructive_trust_equitable_estoppel_overview, r'##.*Reinterpretation of "Equitable Estoppel"')
                log_provenance("Dialogos(Sutton)", "EquitableEstoppelReference", 
                               f"Text mentions equitable estoppel. Overview: {snippet[:200]}...")
        else:
            presumption_words = ["assume", "presume", "obviously", "of course", "clearly", "acquiesce"]
            found_words = [word for word in presumption_words if word in text.lower()]
            if found_words:
                details = f"Found words that may indicate challengeable presumptions (Sutton - basic): {found_words}"
                log_provenance("Dialogos(Sutton)", "ChallengeablePresumption", details)

    def get_miller_analysis(self, text):
        if self.carl_miller_teachings:
            if "marbury v. madison" in text.lower():
                snippet = self._get_section_from_markdown(self.carl_miller_teachings, r'##.*Marbury v. Madison')
                log_provenance("Dialogos(Miller)", "MarburyVMadisonReference", 
                               f"Text references Marbury v. Madison. Miller's interpretation: {snippet[:200]}...")
            if "article 6" in text.lower() or "supremacy clause" in text.lower():
                snippet = self._get_section_from_markdown(self.carl_miller_teachings, r'##.*Supremacy Clause')
                log_provenance("Dialogos(Miller)", "SupremacyClauseReference", 
                               f"Text references Supremacy Clause. Miller's interpretation: {snippet[:200]}...")
            if "willful" in text.lower() or "willfulness" in text.lower():
                snippet = self._get_section_from_markdown(self.carl_miller_teachings, r'##.*United States v. Bishop')
                log_provenance("Dialogos(Miller)", "WillfulnessConcept", 
                               f"Text references willfulness, relevant to criminal intent defense (Bishop v. US).")
            
            # Color of Law integration
            if self.color_of_law_overview:
                if "color of law" in text.lower() or "color of office" in text.lower():
                    snippet = self._get_section_from_markdown(self.color_of_law_overview, r'##.*Core Interpretation')
                    log_provenance("Dialogos(Miller)", "ColorOfLawReference", 
                                   f"Text mentions Color of Law/Office. Miller's view on challenging authority: {snippet[:200]}...")
            
            # Judicial Notice / Immunity integration
            if self.judicial_notice_immunity_overview:
                if "judicial notice" in text.lower():
                    snippet = self._get_section_from_markdown(self.judicial_notice_immunity_overview, r'##.*Reinterpretation of "Judicial Notice"')
                    log_provenance("Dialogos(Miller)", "JudicialNoticeReference", 
                                   f"Text mentions judicial notice. Miller's view on judicial authority: {snippet[:200]}...")
                if "judicial immunity" in text.lower():
                    snippet = self._get_section_from_markdown(self.judicial_notice_immunity_overview, r'##.*Reinterpretation of "Judicial Immunity"')
                    log_provenance("Dialogos(Miller)", "JudicialImmunityReference", 
                                   f"Text mentions judicial immunity. Miller's view on judicial accountability: {snippet[:200]}...")

            # Res Judicata / Collateral Estoppel integration
            if self.res_judicata_collateral_estoppel_overview:
                if "res judicata" in text.lower():
                    snippet = self._get_section_from_markdown(self.res_judicata_collateral_estoppel_overview, r'##.*Reinterpretation of "Res Judicata"')
                    log_provenance("Dialogos(Miller)", "ResJudicataReference", 
                                   f"Text mentions res judicata. Overview: {snippet[:200]}...")
                if "collateral estoppel" in text.lower():
                    snippet = self._get_section_from_markdown(self.res_judicata_collateral_estoppel_overview, r'##.*Reinterpretation of "Collateral Estoppel"')
                    log_provenance("Dialogos(Miller)", "CollateralEstoppelReference", 
                                   f"Text mentions collateral estoppel. Overview: {snippet[:200]}...")

            # CFR Interpretation integration
            if self.cfr_interpretation_overview:
                if "cfr" in text.lower() or "code of federal regulations" in text.lower():
                    snippet = self._get_section_from_markdown(self.cfr_interpretation_overview, r'##.*Core Interpretation')
                    log_provenance("Dialogos(Miller)", "CFRInterpretationReference", 
                                   f"Text mentions CFR. Miller's view on regulations vs. law: {snippet[:200]}...")

            info_war_words = ["disinformation", "narrative", "troll", "bot", "propaganda"]
            found_words = [word for word in info_war_words if word in text.lower()]
            if found_words:
                details = f"Found words related to information warfare (Miller): {found_words}"
                log_provenance("Dialogos(Miller)", "InformationWarfareIndicator", details)
        else:
            info_war_words = ["disinformation", "narrative", "troll", "bot", "propaganda"]
            found_words = [word for word in info_war_words if word in text.lower()]
            if found_words:
                details = f"Found words related to information warfare (Miller - basic): {found_words}"
                log_provenance("Dialogos(Miller)", "InformationWarfareIndicator", details)

    def get_straight_analysis(self, text):
        if self.david_straight_teachings:
            # Extracting specific sections from David Straight's teachings
            if "american state national" in text.lower() or "state national" in text.lower():
                snippet = self._get_section_from_markdown(self.david_straight_teachings, r'##.*American State National Ideology')
                log_provenance("Dialogos(Straight)", "StateNationalIdeology", 
                               f"Text references American State National ideology. Straight's view: {snippet[:200]}...")
            if "strawman" in text.lower():
                snippet = self._get_section_from_markdown(self.david_straight_teachings, r'##.*The "Strawman" and the UCC')
                log_provenance("Dialogos(Straight)", "StrawmanTheoryReference", 
                               f"Text references the 'strawman' theory. Straight's view: {snippet[:200]}...")
            if "right to travel" in text.lower():
                snippet = self._get_section_from_markdown(self.david_straight_teachings, r'##.*Driver\'s License/Title/Registration')
                log_provenance("Dialogos(Straight)", "RightToTravelInterpretation", 
                               f"Text references the 'right to travel'. Straight's view: {snippet[:200]}...")
            if "cestui que vie" in text.lower() or "cqv trust" in text.lower():
                snippet = self._get_section_from_markdown(self.david_straight_teachings, r'##.*Cestui Que Vie (CQV) Trust')
                log_provenance("Dialogos(Straight)", "CestuiQueVieTrustReference", 
                               f"Text references Cestui Que Vie Trust. Straight's view: {snippet[:200]}...")
            if "gold and silver" in text.lower():
                snippet = self._get_section_from_markdown(self.david_straight_teachings, r'##.*Gold and Silver')
                log_provenance("Dialogos(Straight)", "GoldAndSilverReference", 
                               f"Text references gold and silver. Straight's view: {snippet[:200]}...")
            if "three signatures to jail" in text.lower():
                snippet = self._get_section_from_markdown(self.david_straight_teachings, r'##.*Three Signatures to Jail')
                log_provenance("Dialogos(Straight)", "ThreeSignaturesToJailReference", 
                               f"Text references three signatures to jail. Straight's view: {snippet[:200]}...")
            if "color of law" in text.lower() or "color of office" in text.lower():
                snippet = self._get_section_from_markdown(self.color_of_law_overview, r'##.*Core Interpretation')
                log_provenance("Dialogos(Straight)", "ColorOfLawReference", 
                               f"Text mentions Color of Law/Office. Straight's view on challenging authority: {snippet[:200]}...")

            # CFR Interpretation integration
            if self.cfr_interpretation_overview:
                if "cfr" in text.lower() or "code of federal regulations" in text.lower():
                    snippet = self._get_section_from_markdown(self.cfr_interpretation_overview, r'##.*Core Interpretation')
                    log_provenance("Dialogos(Straight)", "CFRInterpretationReference", 
                                   f"Text mentions CFR. Straight's view on regulations vs. law: {snippet[:200]}...")

        if self.common_law_vs_admiralty_overview:
            if "common law" in text.lower() and "admiralty" in text.lower():
                snippet = self._get_section_from_markdown(self.common_law_vs_admiralty_overview, r'##.*The Core Distinction')
                log_provenance("Dialogos(Straight)", "CommonLawVsAdmiralty", 
                               f"Text discusses Common Law vs. Admiralty. Overview: {snippet[:200]}...")
            elif "admiralty" in text.lower() or "maritime law" in text.lower():
                snippet = self._get_section_from_markdown(self.common_law_vs_admiralty_overview, r'##.*The Core Distinction')
                log_provenance("Dialogos(Straight)", "AdmiraltyJurisdiction", 
                               f"Text mentions Admiralty/Maritime Law. Overview: {snippet[:200]}...")
            elif "common law" in text.lower():
                snippet = self._get_section_from_markdown(self.common_law_vs_admiralty_overview, r'##.*The Core Distinction')
                log_provenance("Dialogos(Straight)", "CommonLawReference", 
                               f"Text mentions Common Law. Overview: {snippet[:200]}...")
        else:
            jurisdiction_words = ["jurisdiction", "citizen", "national", "domicile", "residence", "strawman"]
            found_words = [word for word in jurisdiction_words if word in text.lower()]
            if found_words:
                details = f"Found words related to jurisdiction and status (Straight - basic): {found_words}"
                log_provenance("Dialogos(Straight)", "JurisdictionalIndicator", details)

    def get_williams_analysis(self, text):
        if self.brandon_joe_williams_teachings:
            if "legal authorship" in text.lower() or "precise language" in text.lower():
                snippet = self._get_section_from_markdown(self.brandon_joe_williams_teachings, r'##.*Legal Authorship & Precise Language')
                log_provenance("Dialogos(Williams)", "LegalAuthorshipEmphasis", 
                               f"Text emphasizes legal authorship and precise language. Williams' view: {snippet[:200]}...")
            if "contract law" in text.lower() or "challenge contracts" in text.lower():
                snippet = self._get_section_from_markdown(self.brandon_joe_williams_teachings, r'##.*Contract Law as the Basis of a Just System')
                log_provenance("Dialogos(Williams)", "ContractLawFocus", 
                               f"Text focuses on contract law and challenging contracts. Williams' view: {snippet[:200]}...")
            if "state national" in text.lower() and "citizen" in text.lower():
                snippet = self._get_section_from_markdown(self.brandon_joe_williams_teachings, r'##.*State National vs. U.S. Citizen')
                log_provenance("Dialogos(Williams)", "StateNationalVsCitizen", 
                               f"Text discusses State National vs. U.S. Citizen. Williams' view: {snippet[:200]}...")
            if "negotiable instrument" in text.lower() or "infinite money" in text.lower():
                snippet = self._get_section_from_markdown(self.brandon_joe_williams_teachings, r'##.*Negotiable Instruments and "Infinite Money"')
                log_provenance("Dialogos(Williams)", "NegotiableInstrumentReference", 
                               f"Text mentions negotiable instruments/infinite money. Williams' view: {snippet[:200]}...")
            if "agent vs. principal" in text.lower() or "all caps name" in text.lower():
                snippet = self._get_section_from_markdown(self.brandon_joe_williams_teachings, r'##.*"Agent" vs. "Principal"')
                log_provenance("Dialogos(Williams)", "AgentVsPrincipalReference", 
                               f"Text discusses Agent vs. Principal. Williams' view: {snippet[:200]}...")
            if "discovery" in text.lower() and "litigation" in text.lower():
                snippet = self._get_section_from_markdown(self.brandon_joe_williams_teachings, r'##.*Litigation as the Only Path')
                log_provenance("Dialogos(Williams)", "LitigationDiscoveryReference", 
                               f"Text discusses litigation and discovery. Williams' view: {snippet[:200]}...")
        
        if self.common_law_vs_admiralty_overview:
            if "common law" in text.lower() and "admiralty" in text.lower():
                snippet = self._get_section_from_markdown(self.common_law_vs_admiralty_overview, r'##.*The Core Distinction')
                log_provenance("Dialogos(Williams)", "CommonLawVsAdmiralty", 
                               f"Text discusses Common Law vs. Admiralty. Overview: {snippet[:200]}...")
            elif "admiralty" in text.lower() or "maritime law" in text.lower():
                snippet = self._get_section_from_markdown(self.common_law_vs_admiralty_overview, r'##.*The Core Distinction')
                log_provenance("Dialogos(Williams)", "AdmiraltyJurisdiction", 
                               f"Text mentions Admiralty/Maritime Law. Overview: {snippet[:200]}...")
            elif "common law" in text.lower():
                snippet = self._get_section_from_markdown(self.common_law_vs_admiralty_overview, r'##.*The Core Distinction')
                log_provenance("Dialogos(Williams)", "CommonLawReference", 
                               f"Text mentions Common Law. Overview: {snippet[:200]}...")
        else:
            contract_words = ["contract", "agreement", "terms", "party", "consent", "signature", "authorship"]
            found_words = [word for word in contract_words if word in text.lower()]
            if found_words:
                details = f"Found words related to contracts and legal authorship (Williams - basic): {found_words}"
                log_provenance("Dialogos(Williams)", "ContractualIndicator", details)

        # Constructive Trust / Equitable Estoppel integration
        if self.constructive_trust_equitable_estoppel_overview:
            if "constructive trust" in text.lower():
                snippet = self._get_section_from_markdown(self.constructive_trust_equitable_estoppel_overview, r'##.*Reinterpretation of "Constructive Trust"')
                log_provenance("Dialogos(Williams)", "ConstructiveTrustReference", 
                               f"Text mentions constructive trust. Overview: {snippet[:200]}...")
            if "equitable estoppel" in text.lower():
                snippet = self._get_section_from_markdown(self.constructive_trust_equitable_estoppel_overview, r'##.*Reinterpretation of "Equitable Estoppel"')
                log_provenance("Dialogos(Williams)", "EquitableEstoppelReference", 
                               f"Text mentions equitable estoppel. Overview: {snippet[:200]}...")

        # Payment Coupon Endorsement integration
        if self.payment_coupon_endorsement_overview:
            if "payment coupon" in text.lower() or "endorse" in text.lower() or "bill discharge" in text.lower():
                snippet = self._get_section_from_markdown(self.payment_coupon_endorsement_overview, r'##.*Core Principle')
                log_provenance("Dialogos(Williams)", "PaymentCouponEndorsementReference", 
                               f"Text mentions payment coupon endorsement. Overview: {snippet[:200]}...")

        # Res Judicata / Collateral Estoppel integration
        if self.res_judicata_collateral_estoppel_overview:
            if "res judicata" in text.lower():
                snippet = self._get_section_from_markdown(self.res_judicata_collateral_estoppel_overview, r'##.*Reinterpretation of "Res Judicata"')
                log_provenance("Dialogos(Williams)", "ResJudicataReference", 
                               f"Text mentions res judicata. Overview: {snippet[:200]}...")
            if "collateral estoppel" in text.lower():
                snippet = self._get_section_from_markdown(self.res_judicata_collateral_estoppel_overview, r'##.*Reinterpretation of "Collateral Estoppel"')
                log_provenance("Dialogos(Williams)", "CollateralEstoppelReference", 
                               f"Text mentions collateral estoppel. Overview: {snippet[:200]}...")

# Singleton instance
dialogos_agent = DialogosAgent()
