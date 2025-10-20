from datetime import date
import os
import sys
from packages.LocalAgentCore.remedy_logger import RemedyLogger
import datetime

# Initialize RemedyLogger
remedy_logger = RemedyLogger()

# Add the logic directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'NationalityReclaimer', 'logic')))

from generate_affidavit import generate_affidavit

def load_template(template_name):
    """
    Loads a template from the templates directory.
    """
    remedy_logger.log("INFO", f"Loading template: {template_name}")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, '..', 'templates', template_name), 'r') as f:
        return f.read()

def compile_remedy(full_name, birth_location, nationality, trust_type=None, trustee_name=None, beneficiaries=None, trust_property=None):
    """
    Compiles the remedy package, including the affidavit, cover letter, and endorsement, OR the trust documents.
    """
    remedy_logger.log("INFO", f"Compiling remedy for full_name: {full_name}, birth_location: {birth_location}, nationality: {nationality}, trust_type: {trust_type}")

    remedy_package = {}
    if trust_type:
        # Generate trust documents
        trust_agreement_template = load_template('trust_agreement.txt')
        trust_agreement = trust_agreement_template.format(
            date=datetime.date.today().strftime("%B %d, %Y"),
            settlor_name=full_name,
            trustee_name=trustee_name
        )
        remedy_logger.log("INFO", "Generated trust agreement.")
        remedy_package['cover_letter'] = trust_agreement # repurposing this field

        declaration_of_trust_template = load_template('declaration_of_trust.txt')
        declaration_of_trust = declaration_of_trust_template.format(
            settlor_name=full_name,
            settlor_address="[Settlor Address]", # Hardcoded - needs to be updated
            trust_property=trust_property
        )
        remedy_logger.log("INFO", "Generated declaration of trust.")
        remedy_package['endorsement'] = declaration_of_trust # repurposing this field

    else:
        # Generate nationality reclamation documents
        affidavit = generate_affidavit(nationality, full_name, birth_location)
        remedy_logger.log("INFO", "Generated affidavit.")
        remedy_package['affidavit'] = affidavit

        cover_letter_template = load_template('cover_letter.txt')
        cover_letter = cover_letter_template.format(full_name=full_name)
        remedy_logger.log("INFO", "Generated cover letter.")
        remedy_package['cover_letter'] = cover_letter

        endorsement_template = load_template('endorsement.txt')
        today = date.today().strftime("%B %d, %Y")
        endorsement = endorsement_template.format(date=today)
        remedy_logger.log("INFO", "Generated endorsement.")
        remedy_package['endorsement'] = endorsement


    remedy_logger.log("INFO", "Remedy package compilation complete.")
    
    return remedy_package
