import os
import time
from modules.file_watcher import start_watching
from modules.voice_narrator import narrator
from modules.config_manager import config_manager
from modules.logger import system_logger
from modules.remedy_synthesizer import remedy_synthesizer
from modules.corpus_manager import corpus_manager
from modules.nlp_processor import nlp_processor

# Dynamically import agents based on config
if config_manager.get('agents.jarvis.enabled', False):
    from agents.jarvis_agent import jarvis_agent
if config_manager.get('agents.friday.enabled', False):
    from agents.friday_agent import friday_agent
if config_manager.get('agents.dialogos.enabled', False):
    from agents.dialogos_agent import dialogos_agent
if config_manager.get('agents.echo.enabled', False):
    from agents.echo_agent import echo_agent

def get_user_input(prompt):
    narrator.say(prompt)
    return input(prompt + " ")

def run_transcript_workflow():
    narrator.say("Starting transcript processing workflow.")
    file_path = get_user_input("Please enter the full path to the transcript text file:")

    if not os.path.exists(file_path):
        narrator.say("Error: File not found.")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            transcript_content = f.read()
        
        narrator.say("Transcript loaded. Processing with Echo Agent.")
        summary, _ = echo_agent.process_transcript(transcript_content)
        narrator.say(f"Summary generated. It reads: {summary}")

        narrator.say("Now, analyzing the summary with other agents.")
        
        nlp_results = nlp_processor.process_text(summary)
        
        if jarvis_agent:
            jarvis_agent.analyze(file_path, nlp_results)
        if friday_agent:
            friday_agent.analyze(file_path, summary)
        if dialogos_agent:
            dialogos_agent.analyze(summary)
        
        narrator.say("Full analysis of the transcript summary is complete. Check the provenance log for details.")

    except Exception as e:
        system_logger.error(f"Failed during transcript workflow: {e}")
        narrator.say("An error occurred during the transcript processing.")

def run_a4v_workflow():
    narrator.say("Starting Accepted for Value workflow.")
    
    rationale = corpus_manager.get_corpus_text('accepted_for_value_rationale.md')
    print("\n--- A4V Rationale ---")
    print(rationale)
    print("---------------------\n")
    
    proceed = get_user_input("Do you wish to proceed? (yes/no)")
    if proceed.lower() != 'yes':
        narrator.say("Aborting A4V workflow.")
        return

    data = {
        "your_name": get_user_input("What is your full name?"),
        "your_address": get_user_input("What is your mailing address?"),
        "recipient_name": get_user_input("Who is the bill from (person or company)?"),
        "company_name": get_user_input("What is the company name?"),
        "company_address": get_user_input("What is the company's mailing address?"),
        "account_number": get_user_input("What is the account number?"),
        "bill_date": get_user_input("What is the date on the bill?"),
        "bill_amount": get_user_input("What is the amount of the bill?"),
        "date": time.strftime("%Y-%m-%d")
    }

    narrator.say("Thank you. Generating A4V endorsement document.")
    output_path = remedy_synthesizer.generate_document('a4v_endorsement.txt.j2', data)

    if output_path:
        narrator.say(f"Document successfully generated and saved to {output_path}")
    else:
        narrator.say("Failed to generate the document.")

def interactive_corpus_lookup():
    narrator.say("Welcome to the legal dictionary.")
    term = get_user_input("What term would you like to look up?")
    definition = corpus_manager.get_definition(term)
    if definition:
        narrator.say(f"The definition of {term} is: {definition}")
    else:
        narrator.say(f"Sorry, I could not find a definition for {term}.")

def run_conditional_acceptance_workflow():
    narrator.say("Starting Conditional Acceptance workflow.")

    # Display the rationale and disclaimer
    rationale = corpus_manager.get_corpus_text('conditional_acceptance_guide.md')
    print("\n--- Conditional Acceptance Guide ---")
    print(rationale)
    print("---------------------\n")

    proceed = get_user_input("Do you wish to proceed? (yes/no)")
    if proceed.lower() != 'yes':
        narrator.say("Aborting Conditional Acceptance workflow.")
        return

    data = {
        "your_name": get_user_input("What is your full name?"),
        "your_address": get_user_input("What is your mailing address?"),
        "recipient_name": get_user_input("Who is the demand from (person or company)?"),
        "recipient_title": get_user_input("What is their title (e.g., CEO, Agent)?"),
        "company_name": get_user_input("What is the company name?"),
        "company_address": get_user_input("What is the company's mailing address?"),
        "matter_subject": get_user_input("What is the subject of the demand (e.g., Account #12345, Traffic Ticket)?"),
        "demand_date": get_user_input("What is the date of the demand you received?"),
        "condition_1": get_user_input("Enter your first condition for acceptance:"),
        "condition_2": get_user_input("Enter your second condition for acceptance:"),
        "condition_3": get_user_input("Enter your third condition for acceptance:"),
        "date": time.strftime("%Y-%m-%d")
    }

    narrator.say("Thank you. Generating Conditional Acceptance letter.")
    output_path = remedy_synthesizer.generate_document('conditional_acceptance_letter.txt.j2', data)

    if output_path:
        narrator.say(f"Document successfully generated and saved to {output_path}")
    else:
        narrator.say("Failed to generate the document.")

def run_status_correction_workflow():
    narrator.say("Starting Status Correction workflow.")

    # Display the rationale and disclaimer
    rationale = corpus_manager.get_corpus_text('status_correction_overview.md')
    print("\n--- Status Correction Overview ---")
    print(rationale)
    print("---------------------\n")

    proceed = get_user_input("Do you wish to proceed? (yes/no)")
    if proceed.lower() != 'yes':
        narrator.say("Aborting Status Correction workflow.")
        return

    data = {
        "your_name": get_user_input("What is your full name?"),
        "declared_status": get_user_input("What status do you wish to declare (e.g., common law free man, state national)?"),
        "state_of_residence": get_user_input("What is your state of residence (e.g., Michigan)?"),
        "date": time.strftime("%Y-%m-%d"),
        "month": time.strftime("%B"),
        "year": time.strftime("%Y")
    }

    narrator.say("Thank you. Generating Affidavit of Status.")
    output_path = remedy_synthesizer.generate_document('affidavit_of_status.txt.j2', data)

    if output_path:
        narrator.say(f"Document successfully generated and saved to {output_path}")
    else:
        narrator.say("Failed to generate the document.")

def run_private_administrative_process_workflow():
    narrator.say("Starting Private Administrative Process workflow.")

    # Display the rationale and disclaimer
    rationale = corpus_manager.get_corpus_text('private_administrative_process_overview.md')
    print("\n--- Private Administrative Process Overview ---")
    print(rationale)
    print("---------------------
")

    proceed = get_user_input("Do you wish to proceed? (yes/no)")
    if proceed.lower() != 'yes':
        narrator.say("Aborting Private Administrative Process workflow.")
        return

    narrator.say("We will now generate the Notice of Fault and Opportunity to Cure.")
    data_notice = {
        "your_name": get_user_input("Your full name:"),
        "your_address": get_user_input("Your mailing address:"),
        "recipient_name": get_user_input("Recipient's full name:"),
        "recipient_title": get_user_input("Recipient's title (e.g., CEO, Agent):"),
        "company_name": get_user_input("Company name:"),
        "company_address": get_user_input("Company mailing address:"),
        "matter_subject": get_user_input("Subject of the matter:"),
        "demand_date": get_user_input("Date of their original demand:"),
        "fault_1": get_user_input("First fault (e.g., failure to provide proof of claim):"),
        "fault_2": get_user_input("Second fault:"),
        "fault_3": get_user_input("Third fault:"),
        "cure_action_1": get_user_input("First action to cure (e.g., provide original contract):"),
        "cure_action_2": get_user_input("Second action to cure:"),
        "cure_action_3": get_user_input("Third action to cure:"),
        "date": time.strftime("%Y-%m-%d")
    }
    output_path_notice = remedy_synthesizer.generate_document('notice_of_fault_and_opportunity_to_cure.txt.j2', data_notice)

    if output_path_notice:
        narrator.say(f"Notice of Fault generated: {output_path_notice}")
        narrator.say("Remember to send this via Certified Mail, Return Receipt Requested, and keep records.")
        
        proceed_affidavit = get_user_input("\nAfter 10 days, if no cure, do you want to generate the Affidavit of Default? (yes/no)")
        if proceed_affidavit.lower() == 'yes':
            narrator.say("Generating Affidavit of Default.")
            data_affidavit = {
                "your_name": data_notice["your_name"],
                "recipient_name": data_notice["recipient_name"],
                "company_name": data_notice["company_name"],
                "matter_subject": data_notice["matter_subject"],
                "notice_date": data_notice["date"],
                "tracking_number": get_user_input("Certified Mail tracking number for the Notice of Fault:"),
                "date": time.strftime("%Y-%m-%d"),
                "month": time.strftime("%B"),
                "year": time.strftime("%Y")
            }
            output_path_affidavit = remedy_synthesizer.generate_document('affidavit_of_default.txt.j2', data_affidavit)
            if output_path_affidavit:
                narrator.say(f"Affidavit of Default generated: {output_path_affidavit}")
                narrator.say("Remember to have this notarized and keep records.")
            else:
                narrator.say("Failed to generate Affidavit of Default.")
    else:
        narrator.say("Failed to generate Notice of Fault.")

def run_ucc_filing_workflow():
    narrator.say("Starting UCC Filing for Status workflow.")

    # Display the rationale and disclaimer
    rationale = corpus_manager.get_corpus_text('ucc_filings_for_status_overview.md')
    print("\n--- UCC Filings for Status Overview ---")
    print(rationale)
    print("---------------------
")

    proceed = get_user_input("Do you wish to proceed? (yes/no)")
    if proceed.lower() != 'yes':
        narrator.say("Aborting UCC Filing workflow.")
        return

    data = {
        "debtor_name": get_user_input("Enter the DEBTOR's name (e.g., JOHN DOE in all caps):"),
        "debtor_address": get_user_input("Enter the DEBTOR's address:"),
        "secured_party_name": get_user_input("Enter the SECURED PARTY's name (e.g., John Doe in upper/lower case):"),
        "secured_party_address": get_user_input("Enter the SECURED PARTY's address:"),
        "date": time.strftime("%Y-%m-%d")
    }

    narrator.say("Thank you. Generating UCC-1 Financing Statement.")
    output_path = remedy_synthesizer.generate_document('ucc1_financing_statement.txt.j2', data)

    if output_path:
        narrator.say(f"Document successfully generated and saved to {output_path}")
        narrator.say("Remember, this is a simplified template. Consult legal resources for proper UCC filing procedures.")
    else:
        narrator.say("Failed to generate the document.")

def run_claim_against_bond_workflow():
    narrator.say("Starting Claim Against Official's Bond workflow.")

    # Display the rationale and disclaimer
    rationale = corpus_manager.get_corpus_text('surety_and_bond_theory_overview.md')
    print("\n--- Surety and Bond Theory Overview ---")
    print(rationale)
    print("---------------------
")

    proceed = get_user_input("Do you wish to proceed? (yes/no)")
    if proceed.lower() != 'yes':
        narrator.say("Aborting Claim Against Bond workflow.")
        return

    data = {
        "your_name": get_user_input("Your full name:"),
        "your_address": get_user_input("Your mailing address:"),
        "official_name": get_user_input("Official's full name:"),
        "official_title": get_user_input("Official's title (e.g., Judge, Police Officer):"),
        "government_agency": get_user_input("Government agency/department:"),
        "agency_address": get_user_input("Agency mailing address:"),
        "date_of_violation": get_user_input("Date of alleged violation:"),
        "matter_subject": get_user_input("Subject of the matter (e.g., Unlawful Arrest, Violation of Rights):"),
        "violation_1": get_user_input("First specific violation:"),
        "violation_2": get_user_input("Second specific violation:"),
        "violation_3": get_user_input("Third specific violation:"),
        "damages_incurred": get_user_input("Damages incurred (e.g., $500, emotional distress):"),
        "date": time.strftime("%Y-%m-%d")
    }

    narrator.say("Thank you. Generating Notice of Claim Against Bond.")
    output_path = remedy_synthesizer.generate_document('notice_of_claim_against_bond.txt.j2', data)

    if output_path:
        narrator.say(f"Document successfully generated and saved to {output_path}")
        narrator.say("Remember to send this via Certified Mail, Return Receipt Requested, and keep records.")
    else:
        narrator.say("Failed to generate the document.")

def run_debt_discharge_instrument_workflow():
    narrator.say("Starting Debt Discharge Instrument workflow.")

    # Display the rationale and disclaimer
    rationale = corpus_manager.get_corpus_text('bills_promissory_notes_debt_discharge.md')
    print("\n--- Bills & Promissory Notes for Debt Discharge ---")
    print(rationale)
    print("---------------------
")

    proceed = get_user_input("Do you wish to proceed? (yes/no)")
    if proceed.lower() != 'yes':
        narrator.say("Aborting Debt Discharge Instrument workflow.")
        return

    instrument_type = get_user_input("Which instrument would you like to create? (Bill of Exchange / Promissory Note): ")
    
    data = {
        "your_name_upper_lower": get_user_input("Your name (e.g., John Doe):"),
        "your_name_all_caps": get_user_input("Your name in ALL CAPS (e.g., JOHN DOE - for Strawman):"),
        "payee_name": get_user_input("Payee's name (e.g., Creditor Name):"),
        "amount_words": get_user_input("Amount in words (e.g., One Thousand Dollars):"),
        "amount_numbers": get_user_input("Amount in numbers (e.g., $1,000.00):"),
        "account_number": get_user_input("Account Number:"),
        "creditor_name": get_user_input("Creditor Name:"),
        "date": time.strftime("%Y-%m-%d")
    }

    if instrument_type.lower() == 'bill of exchange':
        narrator.say("Generating Sovereign Bill of Exchange.")
        output_path = remedy_synthesizer.generate_document('sovereign_bill_of_exchange.txt.j2', data)
    elif instrument_type.lower() == 'promissory note':
        narrator.say("Generating Sovereign Promissory Note.")
        output_path = remedy_synthesizer.generate_document('sovereign_promissory_note.txt.j2', data)
    else:
        narrator.say("Invalid instrument type. Aborting.")
        return

    if output_path:
        narrator.say(f"Document successfully generated and saved to {output_path}")
        narrator.say("Remember, these instruments are not recognized by mainstream financial systems.")
    else:
        narrator.say("Failed to generate the document.")

def run_affidavit_of_fact_workflow():
    narrator.say("Starting Affidavit of Fact generation.")
    data = {
        "your_name": get_user_input("Your full name:"),
        "date_of_event": get_user_input("Date of the event (e.g., YYYY-MM-DD):"),
        "time_of_event": get_user_input("Time of the event (e.g., HH:MM AM/PM):"),
        "description_of_event": get_user_input("Describe the event:"),
        "date": time.strftime("%Y-%m-%d"),
        "month": time.strftime("%B"),
        "year": time.strftime("%Y")
    }
    narrator.say("Generating Affidavit of Fact.")
    output_path = remedy_synthesizer.generate_document('affidavit_of_fact.txt.j2', data)
    if output_path:
        narrator.say(f"Document successfully generated and saved to {output_path}")
    else:
        narrator.say("Failed to generate the document.")

def run_commercial_lien_workflow():
    narrator.say("Starting Commercial Lien workflow.")

    # Display the rationale and disclaimer
    rationale = corpus_manager.get_corpus_text('affidavit_of_commercial_lien_overview.md')
    print("\n--- Affidavit of Commercial Lien Overview ---")
    print(rationale)
    print("---------------------
")

    proceed = get_user_input("Do you wish to proceed? (yes/no)")
    if proceed.lower() != 'yes':
        narrator.say("Aborting Commercial Lien workflow.")
        return

    data = {
        "your_name": get_user_input("Your full name:"),
        "date_of_event": get_user_input("Date of the event leading to the lien (e.g., YYYY-MM-DD):"),
        "time_of_event": get_user_input("Time of the event (e.g., HH:MM AM/PM):"),
        "description_of_violation": get_user_input("Describe the violation/event leading to the lien:"),
        "alleged_debtor_name": get_user_input("Alleged Debtor's Name:"),
        "alleged_debtor_title": get_user_input("Alleged Debtor's Title (e.g., Judge, CEO):"),
        "specific_rights_violated": get_user_input("Specific rights violated (e.g., Due Process, Right to Travel):"),
        "damages_amount_words": get_user_input("Damages amount in words (e.g., One Million Dollars):"),
        "damages_amount_numbers": get_user_input("Damages amount in numbers (e.g., $1,000,000.00):"),
        "notice_date": get_user_input("Date of Notice of Fault (if applicable, YYYY-MM-DD):"),
        "tracking_number": get_user_input("Certified Mail tracking number for Notice of Fault (if applicable):"),
        "date": time.strftime("%Y-%m-%d"),
        "month": time.strftime("%B"),
        "year": time.strftime("%Y")
    }

    narrator.say("Thank you. Generating Affidavit of Commercial Lien.")
    output_path = remedy_synthesizer.generate_document('affidavit_of_commercial_lien.txt.j2', data)

    if output_path:
        narrator.say(f"Document successfully generated and saved to {output_path}")
        narrator.say("Remember, these liens are fraudulent and have severe legal consequences.")
    else:
        narrator.say("Failed to generate the document.")

def run_payment_coupon_endorsement_workflow():
    narrator.say("Starting Payment Coupon Endorsement workflow.")

    # Display the rationale and disclaimer
    rationale = corpus_manager.get_corpus_text('payment_coupon_endorsement_overview.md')
    print("\n--- Payment Coupon Endorsement Overview ---")
    print(rationale)
    print("---------------------
")

    proceed = get_user_input("Do you wish to proceed? (yes/no)")
    if proceed.lower() != 'yes':
        narrator.say("Aborting Payment Coupon Endorsement workflow.")
        return

    data = {
        "your_name": get_user_input("Your full name:"),
        "date": time.strftime("%Y-%m-%d"),
        "current_date": time.strftime("%Y-%m-%d"), # For template
        "bill_from": get_user_input("Who is the bill from (e.g., Utility Company Name):"),
        "bill_amount": get_user_input("Bill amount (e.g., $123.45):"),
        "account_number": get_user_input("Account Number:"),
        "your_name_all_caps": get_user_input("Your name in ALL CAPS (for endorsement):")
    }

    narrator.say("Thank you. Generating Payment Coupon Endorsement Instructions.")
    output_path = remedy_synthesizer.generate_document('payment_coupon_endorsement_instructions.txt.j2', data)

    if output_path:
        narrator.say(f"Instructions successfully generated and saved to {output_path}")
        narrator.say("Remember, this practice is not recognized by mainstream financial systems.")
    else:
        narrator.say("Failed to generate the instructions.")

def main_menu():
    while True:
        print("\n--- VeroBrix Engine Menu ---")
        print("1. Start Passive Monitoring")
        print("2. Generate a Cease & Desist Letter")
        print("3. Workflow: Process a Bill with 'Accepted for Value'")
        print("4. Workflow: Process a Video Transcript")
        print("5. Workflow: Respond with Conditional Acceptance")
        print("6. Workflow: Initiate Status Correction")
        print("7. Workflow: Initiate Private Administrative Process")
        print("8. Workflow: Initiate UCC Filing for Status")
        print("9. Workflow: Initiate Claim Against Official's Bond")
        print("10. Workflow: Create Debt Discharge Instrument")
        print("11. Workflow: File Commercial Lien")
        print("12. Workflow: Endorse Payment Coupon for Discharge")
        print("13. Generate a General Affidavit of Fact")
        print("14. Look up a Legal Term")
        print("15. Exit")
        choice = input("Enter your choice (1-15): ")

        if choice == '1':
            watch_dir_name = config_manager.get('engine.watch_directory', 'intake')
            watch_dir_abs = os.path.abspath(os.path.join(os.path.dirname(__file__), watch_dir_name))
            if not os.path.exists(watch_dir_abs):
                os.makedirs(watch_dir_abs)
            system_logger.info(f"Engine starting passive monitoring on: {watch_dir_abs}")
            start_watching(watch_dir_abs)
            break
        elif choice == '2':
            interactive_cd_generation()
        elif choice == '3':
            run_a4v_workflow()
        elif choice == '4':
            run_transcript_workflow()
        elif choice == '5':
            run_conditional_acceptance_workflow()
        elif choice == '6':
            run_status_correction_workflow()
        elif choice == '7':
            run_private_administrative_process_workflow()
        elif choice == '8':
            run_ucc_filing_workflow()
        elif choice == '9':
            run_claim_against_bond_workflow()
        elif choice == '10':
            run_debt_discharge_instrument_workflow()
        elif choice == '11':
            run_commercial_lien_workflow()
        elif choice == '12':
            run_payment_coupon_endorsement_workflow()
        elif choice == '13':
            run_affidavit_of_fact_workflow()
        elif choice == '14':
            interactive_corpus_lookup()
        elif choice == '15':
            narrator.say("Exiting VeroBrix Engine.")
            break
        else:
            narrator.say("Invalid choice. Please try again.")

# --- Full main.py for context ---

def interactive_cd_generation():
    narrator.say("Starting Cease and Desist generation.")
    data = {
        "your_name": get_user_input("What is your full name?"),
        "recipient_name": get_user_input("What is the recipient's full name?"),
        "company_name": get_user_input("What is the recipient's company name?"),
        "matter_subject": get_user_input("What is the subject of this matter?"),
        "date": time.strftime("%Y-%m-%d")
    }
    narrator.say("Generating document.")
    remedy_synthesizer.generate_document('cease_and_desist.txt.j2', data)

if __name__ == "__main__":
    narrator.say("VeroBrix Sovereign Intelligence Engine Initialized.")
    main_menu()
