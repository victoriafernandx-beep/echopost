import toml
import os

try:
    secrets_path = ".streamlit/secrets.toml"
    if not os.path.exists(secrets_path):
        print("secrets.toml not found")
    else:
        secrets = toml.load(secrets_path)
        print("Keys in secrets.toml:")
        def print_keys(d, prefix=""):
            for k, v in d.items():
                if isinstance(v, dict):
                    print_keys(v, prefix + k + ".")
                else:
                    print(f"- {prefix}{k}")
        
        print_keys(secrets)
except Exception as e:
    print(f"Error: {e}")
