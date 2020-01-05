import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="userkit",
    version="1.0.0",
    description="Python bindings for UserKit: user login and account management",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/workpail/userkit-python",
    author="Workpail",
    author_email="info@workpail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["userkit"],
    include_package_data=True,
    install_requires=["requests"],
)
