import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-your-username",
    version="0.0.1",
    author="Velis d.o.o.",
    author_email="klemen.spruk@velis.si",
    description="PaySera payments python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KlemenSpruk/paysera_webtopay",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)