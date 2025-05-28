import os

def verify_project_structure(project_folder):
    # Define the expected structure
    expected_structure = {
        "static": {
            "css": ["style.css", "linde.css"],
            "brand_assets": {
                "linde": ["logo.png", "splash.jpg", "fun_facts.txt"]
            }
        },
        "templates": ["index.html"],
        "app.py": None
    }

    # Function to recursively check the structure
    def check_structure(base_path, structure):
        for key, value in structure.items():
            path = os.path.join(base_path, key)
            if isinstance(value, dict):  # If it's a directory
                if not os.path.isdir(path):
                    print(f"❌ Missing directory: {path}")
                else:
                    check_structure(path, value)  # Recursively check subdirectories
            elif isinstance(value, list):  # If it's a list of files
                for file in value:
                    file_path = os.path.join(path, file)
                    if not os.path.isfile(file_path):
                        print(f"❌ Missing file: {file_path}")
            else:  # If it's a single file
                if not os.path.isfile(path):
                    print(f"❌ Missing file: {path}")

    # Start verification
    print("Verifying project structure...")
    check_structure(project_folder, expected_structure)
    print("Verification complete.")

if __name__ == "__main__":
    # Path to your project folder
    project_folder = os.getcwd()  # Current working directory
    verify_project_structure(project_folder)