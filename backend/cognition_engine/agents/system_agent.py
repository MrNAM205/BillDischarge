import subprocess
from core.narration import narrate

def execute_command(command):
    """Executes a shell command and returns the output."""
    narrate(f"Preparing to execute system command: {command}")
    
    # Security warning and confirmation
    narrate("Warning: This command will be executed with system privileges. Proceed with caution.")
    # In a real-world scenario, you might want a confirmation step here.
    # For now, we proceed directly to execution.
    
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            narrate("Command executed successfully.")
            if stdout:
                print(f"[System Agent] Output:\n{stdout}")
        else:
            narrate("Command execution failed.")
            if stderr:
                print(f"[System Agent] Error:\n{stderr}")
    except Exception as e:
        narrate(f"An error occurred while executing the command: {e}")
        print(f"[System Agent] Error: {e}")

def handle_system_command(file_path):
    """Handles system command tasks from a file."""
    narrate(f"System agent activated by file: {file_path}")
    try:
        with open(file_path, 'r') as f:
            content = f.read().strip()
        
        if content.startswith("execute:"):
            command = content.replace("execute:", "").strip()
            execute_command(command)
        else:
            narrate("Invalid system command format in file. Command must start with 'execute:'.")
    except Exception as e:
        narrate(f"Error reading system command file: {e}")
        print(f"[System Agent] Error: {e}")
