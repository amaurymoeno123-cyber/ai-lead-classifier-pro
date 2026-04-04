import os

def update_env_file(key, value):
    """
    Updates or adds a key-value pair in the local .env file.
    """
    env_file = ".env"
    
    # Read existing lines
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            lines = f.readlines()
    else:
        lines = []

    # Check if key exists and update it
    found = False
    new_lines = []
    for line in lines:
        if line.startswith(f"{key}="):
            new_lines.append(f"{key}={value}\n")
            found = True
        else:
            new_lines.append(line)
            
    # If key not found, append it
    if not found:
        new_lines.append(f"{key}={value}\n")

    # Write back to .env
    with open(env_file, "w") as f:
        f.writelines(new_lines)
