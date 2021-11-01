from setuptools import setup, find_packages

with open("requirements.txt") as fd:
    install_requires = fd.read().splitlines()

setup(
    name="gitgeo",
    version="1.0.0",
    description="Discover the geography of open-source software. Explore the geographic locations of software developers associated with a GitHub repository or a Python (PyPI) package.",
    long_description=open("README.rst").read(),
    keywords="open_source github",
    author="John Speed Meyers",
    author_email="54914994+jspeed-meyers@users.noreply.github.com",
    python_requires=">=3.6",
    url="https://github.com/IQTLabs/GitGeo",
    license="Apache",
    classifiers=[
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: System :: Software Distribution",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    tests_require=["pytest"],
    entry_points={"console_scripts": ["gitgeo = gitgeo.main:main"]},
)