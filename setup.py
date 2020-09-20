from setuptools import setup, find_packages

with open('requirements.txt') as requirements_file:
    install_requirements = requirements_file.read().splitlines()

setup(
    name = "netns-siml",
    version = "0.0.1",
    description = "network simulation tool by using linux network namespace",
    author = "terassyi",
    packages = find_packages(),
    install_requires = install_requirements,
    entry_points = {
        "console_scripts": [
            "test = test:test",
        ]
    }
)
