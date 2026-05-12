import os
import subprocess
import sys
import customtkinter

def build():
    # 1. Get customtkinter path
    ctk_path = os.path.dirname(customtkinter.__file__)
    
    # 2. Define command
    # We use --noconsole to hide the black terminal window
    # We use --onefile to bundle everything into a single exe
    # We add src directory and customtkinter assets
    # We EXCLUDE data/config, data/sessions to ensure a "Clean Build"
    
    cmd = [
        "pyinstaller",
        "--noconsole",
        "--onefile",
        "--name", "TranslatorApp",
        "--add-data", f"{ctk_path}{os.pathsep}customtkinter",
        "--add-data", f"src/assets{os.pathsep}src/assets",
        "main.py"
    ]
    
    print("--- STARTING CLEAN BUILD (v1.2.0) ---")
    print(f"CustomTkinter path: {ctk_path}")
    print(f"Command: {' '.join(cmd)}")
    print("-----------------------------------")
    
    try:
        subprocess.check_call(cmd)
        print("\nBUILD SUCCESSFUL!")
        print(f"Executable is located in: {os.path.abspath('dist')}")
    except subprocess.CalledProcessError as e:
        print(f"\nBUILD FAILED: {e}")
        print("Make sure you have installed pyinstaller: pip install pyinstaller")
    except FileNotFoundError:
        print("\nERROR: pyinstaller not found.")
        print("Please run: pip install pyinstaller")

if __name__ == "__main__":
    build()
