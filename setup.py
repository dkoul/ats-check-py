from setuptools import setup, find_packages

setup(
    name="ats-check",
    version="1.0.0",
    description="CLI tool to check resume ATS compatibility",
    packages=find_packages(),
    install_requires=[
        "PyPDF2>=3.0.0",
        "python-docx>=1.1.0",
        "scikit-learn>=1.3.0",
    ],
    entry_points={
        "console_scripts": [
            "ats-check=ats_check.cli:main",
        ],
    },
    python_requires=">=3.8",
)
