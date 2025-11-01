
import yaml
import os

def load_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def load_endorsement_templates(templates_dir):
    templates = {}
    for filename in os.listdir(templates_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(templates_dir, filename), 'r') as f:
                template_name = os.path.splitext(filename)[0]
                templates[template_name] = f.read().strip()
    return templates