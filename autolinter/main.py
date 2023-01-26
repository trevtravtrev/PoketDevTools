import subprocess


def run_linters(directory):
    # Run Black
    print("////////////////////////START BLACK////////////////////////")
    subprocess.run(["black", directory])
    print("////////////////////////END BLACK////////////////////////")
    # Run Flake8
    print("\n\n\n\n\n////////////////////////START FLAKE8////////////////////////")
    subprocess.run(["flake8", directory])
    print("////////////////////////END FLAKE8////////////////////////")
    # Run Radon
    print("\n\n\n\n\n////////////////////////START RADON////////////////////////")
    subprocess.run(["radon", "cc", "-s", directory])
    print("\n\n\n\n\n////////////////////////END RADON////////////////////////")
    # Run Bandit
    print("\n\n\n\n\n////////////////////////START BANDIT////////////////////////")
    subprocess.run(["bandit", "-r", directory])
    print("\n\n\n\n\n////////////////////////END BANDIT////////////////////////")
    # Run Isort
    print("\n\n\n\n\n////////////////////////START ISORT////////////////////////")
    subprocess.run(["isort", directory])
    print("\n\n\n\n\n////////////////////////END ISORT////////////////////////")
    # Run Mypy
    print("\n\n\n\n\n////////////////////////START MYPY////////////////////////")
    subprocess.run(["mypy", directory])
    print("\n\n\n\n\n////////////////////////END MYPY////////////////////////")


def main():
    directory = input("Enter the directory or file path to run linters on: ")
    run_linters(directory)
    print("Linting complete.")


if __name__ == "__main__":
    main()
