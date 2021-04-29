import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

from wopsego import __version__

setuptools.setup(
    name="wopsego",
    version=__version__,
    author="Rémi Lafage",
    description="WhatsOpt API for SEGOMOE Onera Optimizer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/OneraHub/wopsego",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: .6",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["wopsego"],
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*",
    install_requires=["future"],
)
