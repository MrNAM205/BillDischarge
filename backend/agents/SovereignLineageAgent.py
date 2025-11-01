import yaml
from datetime import datetime

LINEAGE_LOG_PATH = "/home/mrnam205/Desktop/BillDischarge/data/lineage_log.yaml"

class SovereignLineageAgent:
    """
    Manages the lineage log of sovereign invocations.
    """

    def __init__(self, log_path=LINEAGE_LOG_PATH):
        self.log_path = log_path

    def _read_log(self):
        """Reads the lineage log from the YAML file."""
        try:
            with open(self.log_path, 'r') as f:
                log_data = yaml.safe_load(f)
                if log_data is None:
                    return []
                return log_data
        except FileNotFoundError:
            return []

    def _write_log(self, log_data):
        """Writes the lineage log to the YAML file."""
        with open(self.log_path, 'w') as f:
            yaml.dump(log_data, f, default_flow_style=False, sort_keys=False)

    def log_invocation(self, module: str, signer: str, jurisdiction: str, overlays: list, manifest_hash: str, exported: bool, signed: bool, published: bool):
        """Appends a new invocation to the lineage log."""
        log_data = self._read_log()
        new_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "module": module,
            "signer": signer,
            "jurisdiction": jurisdiction,
            "overlays": overlays,
            "manifest_hash": manifest_hash,
            "exported": exported,
            "signed": signed,
            "published": published,
        }
        log_data.append(new_entry)
        self._write_log(log_data)
        return new_entry

    def get_history(self, module: str = None, signer: str = None):
        """
        Retrieves the full or filtered invocation history.

        :param module: Optional filter by module name.
        :param signer: Optional filter by signer name.
        """
        log_data = self._read_log()
        if not module and not signer:
            return log_data

        filtered_history = []
        for entry in log_data:
            if module and entry.get("module") != module:
                continue
            if signer and entry.get("signer") != signer:
                continue
            filtered_history.append(entry)

        return filtered_history
