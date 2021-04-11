from setuptools import setup

setup(
    name="datasync",
    version="0.1.0",
    packages=["dasy"],
    entry_points={"console_scripts": ["dasy = dasy.__main__:checkCommand"]},
    install_requires=["click"],
)

