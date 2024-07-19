import streamlit as st
import os
import subprocess
import json

def create_virtual_environment(env_name):
    result = subprocess.run(['python', '-m', 'venv', env_name], capture_output=True, text=True)
    
    if result.returncode == 0:
        vscode_settings_path = os.path.join(env_name, '.vscode')
        os.makedirs(vscode_settings_path, exist_ok=True)
        
        settings_file_path = os.path.join(vscode_settings_path, 'settings.json')
        activate_command = f".\\{env_name}\\Scripts\\activate" if os.name == 'nt' else f"source ./{env_name}/bin/activate"
        
        settings_content = {
            "terminal.integrated.shellArgs.windows": ["/K", activate_command],
            "terminal.integrated.shellArgs.linux": ["-i", "-c", activate_command],
            "terminal.integrated.shellArgs.osx": ["-i", "-c", activate_command]
        }
        
        with open(settings_file_path, 'w') as f:
            f.write(json.dumps(settings_content, indent=4))
        
        # Create a script to open the environment in VS Code
        script_content = f"""
        #!/bin/bash
        cd {os.path.abspath(env_name)}
        code . --new-window --folder-uri {os.path.abspath(env_name)}
        """
        script_path = os.path.join(env_name, 'open_in_vscode.sh')
        
        with open(script_path, 'w') as script_file:
            script_file.write(script_content)
        
        return f"Virtual environment '{env_name}' created successfully! Download the script to open it in VS Code."
    else:
        return f"Failed to create virtual environment '{env_name}'. Error: {result.stderr}"

def download_script(env_name):
    script_path = os.path.join(env_name, 'open_in_vscode.sh')
    with open(script_path, 'rb') as f:
        btn = st.download_button(
            label="Download open_in_vscode.sh",
            data=f,
            file_name="open_in_vscode.sh",
            mime="text/x-sh"
        )
    return btn

st.title('Python Virtual Environment Creator')

env_name = st.text_input('Enter the name of the virtual environment:')
if st.button('Create Environment'):
    if env_name:
        message = create_virtual_environment(env_name)
        st.write(message)
        if "created successfully" in message:
            download_script(env_name)
    else:
        st.write("Please enter a valid environment name.")
