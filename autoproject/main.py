import os
import subprocess
import sys

import logomaker


def check_poetry():
    try:
        subprocess.run(["poetry", "--version"], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False


def create_gitignore(base_directory):
    print("Downloading github standard python .gitignore file...")
    gitignore_url = (
        "https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore"
    )
    gitignore_file = ".gitignore"
    gitignore_path = os.path.join(base_directory, gitignore_file)
    # Download the Python gitignore template
    subprocess.run(["curl", "-o", gitignore_path, gitignore_url])
    # Add the .idea and venv folders to the .gitignore list
    with open(gitignore_path, "a") as f:
        f.write("\n# Project-specific ignores\n")
        f.write("*.idea\n")


def create_project(
    project_name, project_description, poketdev_readme, project_path, github_username
):
    os.chdir(project_path)
    # Check if poetry is installed
    if not check_poetry():
        subprocess.run([sys.executable, "-m", "pip", "install", "poetry"])
    if not os.path.exists(project_name):
        # Workaround for bug where poetry created venv did not work
        subprocess.run(["poetry", "config", "virtualenvs.path", "--unset"])
        # Setting to make venv inside project directory
        subprocess.run(["poetry", "config", "virtualenvs.in-project", "true"])
        # Create new project using Poetry
        subprocess.run(["poetry", "new", project_name])
    os.chdir(project_name)
    base_directory = os.getcwd()
    logomaker.generate_logo(text=project_name, font="Segoe UI", width=500, height=100)
    print("Generated logo...")
    # Set projectname/projectname/ folder as cwd
    os.chdir(os.path.join(base_directory, project_name))
    # Generate main.py file
    with open("main.py", "w") as f:
        f.write(
            f"# {project_name} main file. Run this file to start the application. The Dockerfile is also preconfigured to run this file.\n"
        )
    print("Generated main.py file...")
    # Add packages using poetry
    subprocess.run(
        [
            "poetry",
            "add",
            "poetry",
            "flake8",
            "black",
            "radon",
            "bandit",
            "isort",
            "mypy",
        ]
    )
    # Go back to base directory
    os.chdir(base_directory)
    # Create .gitignore file
    create_gitignore(base_directory)
    # Go back to base directory
    os.chdir(base_directory)
    # Create Dockerfile
    with open("Dockerfile", "w") as f:
        f.write(
            f"""FROM python:3.10-alpine

# Install Poetry
RUN pip install poetry

# Copy the project files into the container
COPY . /app

# Set the working directory to the project directory
WORKDIR /app/{project_name}

# Install the project dependencies
RUN poetry install

# Expose the port for the application to run on
EXPOSE 8000

# Run the command to start the application
CMD ["poetry", "run", "python", "main.py"]"""
        )
    # Go back to base directory
    os.chdir(base_directory)
    # generate readme
    with open("README.md", "w") as f:
        # TODO: add poketdev readme
        if poketdev_readme:
            f.write("")
        else:
            f.write(
                f"""# <br />
<div align="center">
  <a href="https://github.com/{github_username}/{project_name}">
    <img src="logo.png" alt="{project_name}" width="500" height="100">
  </a>

  <p align="center">
    {project_description}
    <br />
    <a href="https://github.com/{github_username}/{project_name}/issues">Report Bug</a>
     | 
    <a href="https://github.com/{github_username}/{project_name}/issues">Request Feature</a>
  </p>
</div>
    """
            )


def main():
    project_name = input("Project name: ")
    project_description = input("Project description: ")
    while True:
        poketdev_readme = int(input("Readme (1 for PocketDev, 0 for regular): "))
        if poketdev_readme not in [1, 0]:
            print("Invalid option.")
            continue
        else:
            break
    github_username = input("Github Username: ")
    project_path = input("Project Target Path: ")
    create_project(
        project_name,
        project_description,
        poketdev_readme,
        project_path,
        github_username,
    )
    print("Complete.")


if __name__ == "__main__":
    main()
