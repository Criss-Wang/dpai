from setuptools import setup, find_packages


setup(
    name="app",
    version="0.0.1",
    description="application",
    include_package_data=True,
    packages=find_packages(exclude=["tests"]),
    entry_points={
        "console_scripts": [
            "application = application.__main__:cli",
        ]
    },
)
