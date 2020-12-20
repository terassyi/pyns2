from setuptools import setup, find_packages

with open('requirements.txt') as requirements_file:
    install_requirements = requirements_file.read().splitlines()

setup(
    name="pyns2",
    version="0.0.3",
    description="network simulation tool by using linux network namespace",
    author="terassyi",
    packages=find_packages(),
    install_requires=install_requirements,
    entry_points={
        "console_scripts": [
            "pyns2 = pyns2.cli.main:main"
        ]
    }
)
