"""
Setup script for AQI Monitoring System.

This script handles the installation and distribution of the AQI Monitoring System.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements = []
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="aqi-monitoring",
    version="1.0.0",
    author="AQI Monitoring Team",
    author_email="support@aqimonitoring.com",
    description="A comprehensive air quality monitoring system with real-time data collection, analysis, prediction, and reporting capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aqimonitoring/aqi-monitoring",
    project_urls={
        "Bug Reports": "https://github.com/aqimonitoring/aqi-monitoring/issues",
        "Source": "https://github.com/aqimonitoring/aqi-monitoring",
        "Documentation": "https://aqimonitoring.readthedocs.io/",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
            "pre-commit>=3.4.0",
        ],
        "docs": [
            "mkdocs>=1.5.0",
            "mkdocs-material>=9.4.0",
            "mkdocstrings>=0.23.0",
        ],
        "monitoring": [
            "prometheus-client>=0.17.0",
            "grafana-api>=1.0.3",
        ],
    },
    entry_points={
        "console_scripts": [
            "aqi-monitor=aqi_monitoring.cli:main",
            "aqi-fetch=aqi_monitoring.cli:fetch_data",
            "aqi-report=aqi_monitoring.cli:generate_report",
        ],
    },
    include_package_data=True,
    package_data={
        "aqi_monitoring": [
            "templates/*.html",
            "static/*.css",
            "static/*.js",
            "data/*.json",
            "config/*.yaml",
        ],
    },
    zip_safe=False,
    keywords=[
        "air-quality",
        "aqi",
        "monitoring",
        "environmental",
        "data-analysis",
        "streamlit",
        "machine-learning",
        "prediction",
        "visualization",
    ],
)