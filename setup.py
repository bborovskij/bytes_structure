from pathlib import Path
import setuptools

VERSION = "0.1.0"  # PEP-440
NAME = "bytes-structure"

setuptools.setup(
    name=NAME,
    version=VERSION,
    description="Parse raw bytes into Python data structure and create bytes message from Python data structure.",
    url="https://github.com/bborovskij/bytes_structure",
    project_urls={
        "Source Code": "https://github.com/bborovskij/bytes_structure",
    },
    author="Bohdan Borovskyi",
    author_email="bborovskij@gmail.com",
    license="MIT License",  # Ensure consistency; change to "Apache License 2.0" if needed
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Telecommunications Industry",
        "License :: OSI Approved :: MIT License",  # Ensure consistency with the `license` field
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.6",
    packages=setuptools.find_packages(),  # Automatically find packages
    long_description=Path("README").read_text(),  # Assuming your README file is README.md
    long_description_content_type="text/markdown",
)
