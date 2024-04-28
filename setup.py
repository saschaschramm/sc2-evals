from setuptools import setup, find_packages

setup(
    name="sc2-evals", # name in pip list
    package_dir={"": "src"},  # tells setuptools that src is the root for all packages
    packages=find_packages(where="src") # finds all packages that contain an __init__.py file
)