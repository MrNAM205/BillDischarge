import os
from modules.config_manager import config
from modules.provenance_logger import log_provenance
from verobrix_core import VeroBrixSystem

def main():
    """
    Enhanced main function with comprehensive legal analysis.
    """
    system = VeroBrixSystem()
    
    # Load input document
    try:
        intake_file = os.path.join(config.get_intake_path(), "sample_document.txt")
        with open(intake_file, "r", encoding='utf-8') as f:
            input_text = f.read()
        log_provenance("VeroBrix System", f"Successfully loaded '{intake_file}'")
    except FileNotFoundError:
        intake_file = os.path.join(config.get_intake_path(), "sample_document.txt")
        log_provenance("VeroBrix System", f"Error: '{intake_file}' not found")
        print(f"Please create the file '{intake_file}' with some text.")
        return
    except Exception as e:
        log_provenance("VeroBrix System", f"Error loading input file: {e}")
        return
    
    # Perform comprehensive analysis
    try:
        results = system.analyze_situation(input_text)
        
        # Print summary
        system.print_analysis_summary(results)
        
        # Demonstrate document generation
        print("\n" + "="*60)
        print("DOCUMENT GENERATION EXAMPLE")
        print("="*60)
        
        # Generate a sample notice
        variables = {
            'OFFICER': 'Officer Johnson',
            'AGENCY': 'State Highway Patrol',
            'INDIVIDUAL_NAME': 'John Doe',
            'NAME': 'John Doe'
        }
        
        document = system.generate_document('traffic_stop', variables)
        print("Generated Notice of Lawful Travel:")
        print("-" * 40)
        print(document)
        
        output_file = os.path.join(config.get_output_path(), f"verobrix_analysis_{system.session_id}.json")
        print(f"\nFull analysis results saved to: {output_file}")
        
    except Exception as e:
        log_provenance("VeroBrix System", f"Error during analysis: {e}")
        print(f"An error occurred during analysis: {e}")

if __name__ == "__main__":
    main()
