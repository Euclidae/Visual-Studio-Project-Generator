import subprocess
import sys
import os

def install_requirements():
    while(True):
        print("Installing required dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("Dependencies installed successfully!")
            break
        except subprocess.CalledProcessError as e:
            print(f"Error installing dependencies: {e}")
            input("Press enter to repeat or Ctrl + C to stop program.")
            continue
            
    return True

def check_python_version():
    if sys.version_info < (3, 7):
        print("Python 3.7 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    print(f"Python version {sys.version.split()[0]} is compatible")
    return True

def main():
    print("Visual Studio Project Generator Setup")
    print("=" * 40)
    
    if not check_python_version():
        sys.exit(1)

    if not install_requirements():
        print("\nTry running: pip install --upgrade pip")
        print("Then run this setup again")
        sys.exit(1)
    
    print("\nSetup completed successfully!")
    print("\This is how to run the project:")
    print("  GUI Version: python GUIprojBuilder.py")
    print("  CLI Version: python CLIprojBuilder.py")
    print("\nFor more information, check the README.md file")

if __name__ == "__main__":
    main()
