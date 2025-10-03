from setuptools import setup, find_packages
from typing import List
from pathlib import Path

def get_requirements() -> List[str]:
    requirements_list: List[str] = []
    req_path = Path(__file__).parent / "requirements.txt"
    try:
        with req_path.open("r", encoding="utf-8") as f:
            for line in f:
                requirement = line.strip()
                if not requirement or requirement.startswith("#"):
                    continue
                if requirement.startswith("-e"):
                    continue
                requirements_list.append(requirement)
    except Exception as e:
        print(f"Error reading {req_path}: {e}")

    return requirements_list

setup(
    name="NetworkSecurityProject",
    version="0.1.0",
    author="Deepanshu Sharama",
    author_email="44deepanshu@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
)