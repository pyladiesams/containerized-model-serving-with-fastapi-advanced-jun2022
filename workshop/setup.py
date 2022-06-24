from setuptools import find_packages, setup

setup(
    name="src",
    packages=find_packages(include=["src"]),
    version="0.0.1",
    description="Clustering Spotify listeners by music style",
    long_description="README.md",
    author="Nikki & Karlijn",
    python_requires=">3.5",
    setup_requires=["pytest-runner", "flake8"],
    tests_require=["pytest"],
    license="MIT",
)
