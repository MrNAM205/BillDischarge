#!/usr/bin/env python3
"""
VeroBrix Command Line Interface

A user-friendly CLI for the VeroBrix legal intelligence system.
"""

import sys
import os
import argparse
import json
from datetime import datetime

from modules.config_manager import config
from verobrix_core import VeroBrixSystem
from modules.provenance_logger import log_provenance

def print_banner() -> None:
    """Print the VeroBrix banner."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                        VeroBrix 2.3                         ║
║              Sovereignty-Aligned Legal Intelligence          ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)

def analyze_file(filepath: str, system: VeroBrixSystem, context: dict = None, output_path: str = None) -> None:
    """Analyze a legal document from file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"📄 Analyzing file: {filepath}")
        analyze_text(content, system, context, output_path)
    except FileNotFoundError:
        print(f"❌ Error: File '{filepath}' not found. Please check the file path.")
    except Exception as e:
        print(f"❌ Error reading file: {e}")

def analyze_text(text: str, system: VeroBrixSystem, context: dict = None, output_path: str = None) -> None:
    """Analyze legal text directly."""
    try:
        print("=" * 60)
        results = system.analyze_situation(text, situation_context=context)
        system.print_analysis_summary(results)
        
        # Overwrite the default save path if a custom one is provided
        if output_path:
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
                print(f"\n✅ Full analysis results saved to: {output_path}")
            except Exception as e:
                print(f"\n❌ Error saving results to custom path: {e}")
        else:
            # Default behavior (already saved by _save_analysis_results)
            default_path = os.path.join(config.get_output_path(), f"verobrix_analysis_{system.session_id}.json")
            print(f"\n✅ Full analysis results saved to: {default_path}")

    except Exception as e:
        print(f"❌ Error during analysis: {e}")

def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="VeroBrix - Sovereignty-Aligned Legal Intelligence System",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument('-f', '--file', help='Path to the legal document to analyze.')
    parser.add_argument('-t', '--text', help='A string of legal text to analyze directly.')
    parser.add_argument('-o', '--output', help='Specify a custom output file for the analysis results (JSON).')
    parser.add_argument('--context', help='JSON string providing context for the situation (e.g., \'{\"type\": \"traffic_stop\"}\").')
    parser.add_argument('-i', '--interactive', action='store_true', help='Run in interactive mode (not yet implemented).')
    parser.add_argument('--version', action='version', version='VeroBrix 2.3')
    
    args = parser.parse_args()
    
    system = VeroBrixSystem()
    print_banner()

    context_dict = None
    if args.context:
        try:
            context_dict = json.loads(args.context)
        except json.JSONDecodeError:
            print("❌ Error: Invalid JSON format for --context argument.")
            return

    if args.file:
        analyze_file(args.file, system, context_dict, args.output)
    elif args.text:
        analyze_text(args.text, system, context_dict, args.output)
    else:
        parser.print_help()
        print("\nNo input provided. Use -f to specify a file or -t to provide text.")

if __name__ == "__main__":
    main()
