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


def create_requirements_txt(base_directory):
    requirements_file = os.path.join(base_directory, "requirements.txt")
    with open(requirements_file, "w") as file:
        pass


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

    # generate requirements.txt
    create_requirements_txt(base_directory)
    print("Generated requirements.txt file...")

    # generate venv
    subprocess.run(["poetry", "install"])
    print("Generated poetry venv...")

    # Add packages using poetry
    # subprocess.run(
    #     [
    #         "poetry",
    #         "add",
    #         "poetry",
    #         "flake8",
    #         "black",
    #         "radon",
    #         "bandit",
    #         "isort",
    #         "mypy",
    #     ]
    # )

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
        if poketdev_readme:
            f.write(
                f"""# <br />
<div align="center">
  <a href="https://github.com/{github_username}/{project_name}">
    <img src="logo.png" alt="{project_name}" width="500" height="100">
  </a>

  <p align="center">
    {project_description}
    <br/>
  </p>
</div>

<details open>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#prerequisites">Prerequisites</a></li>
    <li><a href="#clone-the-repository">Clone the Repository</a></li>
    <li><a href="#run-the-code">Run the Code</a></li>
    <li><a href="#additional-tools">Additional Tools</a></li>
    <li><a href="#thank-you-for-choosing-poket-dev!">Thank you for choosing Poket Dev!</a></li>
  </ol>
</details>

# Contact
For any project-related questions, bug fixes, feature requests, or communication needs regarding {project_name}, please utilize the comment section within your {project_name} request card on your Trello board. This centralizes all discussions, ensuring efficient and effective communication throughout the project's development.  

# Prerequisites
- [Python](https://www.python.org/downloads/) (latest version)  
  - If using windows, in the python installer make sure to select the "Add Python to PATH" option  
- [Pycharm](https://www.jetbrains.com/pycharm/download/#section=windows) (optional)


# Clone the Repository
## Option 1: via Command Line Interface
- Install [GitHub CLI](https://cli.github.com/) (if not already installed)
  ```
  git clone https://github.com/{github_username}/{project_name}
  ```
## Option 2: via GitHub Desktop
1. Install [GitHub Desktop](https://desktop.github.com/) (if not already installed)  
2. Follow instructions [here](https://docs.github.com/en/desktop/contributing-and-collaborating-using-github-desktop/adding-and-cloning-repositories/cloning-a-repository-from-github-to-github-desktop) to clone
# Run the Code
## Option 1: Docker (recommended)

Docker is a free tool that simplifies the process of running applications by packaging them with everything they need, so you can easily move them between different machines and ensure they work quickly and consistently, saving you time and reducing potential conflicts. If you're not familiar with docker, we STRONGLY recommend taking a few minutes to become familiar [here](https://www.docker.com/blog/getting-started-with-docker-desktop/#:~:text=Docker%20Desktop%20is%20an%20easy,%2C%20Kubernetes%2C%20and%20Credential%20Helper.).  
1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) (if not already installed)

2. Build the Docker image:
```
cd {project_name}
docker build -t {project_name} .
```

3. Run the Docker container:
```
docker run {project_name}
```
## Option 2: Poetry
1. Install Poetry (if not already installed)
```
pip install poetry
```
2. Install {project_name} dependencies
```
cd {project_name}
poetry install
```
3. Run {project_name}
```
poetry run python main.py
```
## Option 3: requirements.txt
1. Create the virtual environment:
```
cd {project_name}
python -m venv venv
```
2. Activate the virtual environment:
- For Windows:
```
venv\Scripts\\activate
```
- For macOS/Linux:
```
source venv/bin/activate
```
Once activated, you will notice that the prompt in your terminal or command prompt changes to indicate that you are now working within the virtual environment.  
3. Install {project_name} dependencies
```
pip install -r requirements.txt
```
4. Run {project_name}
```
python main.py
```

# Additional Tools
All {project_name} code was formatted, linted, and secured with the following tools:
- [black](https://black.readthedocs.io/en/stable/)
- [flake8](https://flake8.pycqa.org/en/latest/)
- [radon](https://radon.readthedocs.io/en/latest/)
- [bandit](https://bandit.readthedocs.io/en/latest/)
- [isort](https://pycqa.github.io/isort/)
- [mypy](https://mypy.readthedocs.io/en/stable/)

# Thank you for choosing Poket Dev!
Thank you for choosing Poket Dev, LLC as your unlimited software development partner. We greatly appreciate you and are committed to delivering exceptional solutions and exceeding your expectations.  

If you'd like to refer someone to Poket Dev, and they subscribe to any of our packages, you'll receive a $1000 referral bonus.  """
            )
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
    project_name = input("Project name (no whitespace, hyphens, or underscores): ")
    project_description = input("Project description: ")
    while True:
        poketdev_readme = int(input("README (0 for personal, 1 for Poket Dev): "))
        if poketdev_readme not in [1, 0]:
            print("Invalid option.")
            continue
        else:
            break
    if poketdev_readme == 0:
        github_username = input("Github Username: ")
    else:
        github_username = input("Organization Name (ex. PoketDev-YourCompanyName): ")
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
