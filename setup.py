import setuptools


package_data = {"dpai": ["models/*", "model_files/*", "static/*", "templates/*"]}

setuptools.setup(
    packages=setuptools.find_namespace_packages("src"),
    package_dir={"": "src"},
    package_data=package_data,
)
