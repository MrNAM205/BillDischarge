# verobrix_app/modules/provenance_logger.py
"""
Logs every action with semantic lineage and agent attribution.
Enables full traceability and authorship.
"""
import datetime
import json

class ProvenanceLogger:
    def __init__(self, log_file="provenance.log"):
        self.log_file = log_file

    def log_action(self, agent_name: str, action_type: str, action_description: str, **kwargs):
        """
        Logs an action performed by an agent using a flexible set of details.
        """
        log_entry = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "agent": agent_name,
            "action_type": action_type,
            "description": action_description,
            **kwargs
        }
        
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
            
            print(f"Logged action '{action_type}' by agent '{agent_name}'.")
        except Exception as e:
            print(f"Error writing to provenance log: {e}")

if __name__ == '__main__':
    # Example usage matching verobrix_core.py
    logger = ProvenanceLogger(log_file="test_provenance.log")
    logger.log_action(
        agent_name="VeroBrixSystem",
        action_type="system_init",
        action_description="System initialized."
    )
    logger.log_action(
        agent_name="JarvisAgent",
        action_type="analysis",
        action_description="Extracted 3 clauses.",
        input_data={"text_len": 1024},
        output_data={"clauses_found": 3}
    )

