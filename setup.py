import setuptools
import tess_sn_pipeline

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="tess_sn_pipeline",
    version=piscola.__version__,
    author="XXX",
    author_email="xxx@abc.com",
    license="MIT",
    description="TESS SN pipeline for lightcurve extraction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xxxx",
    packages=['tess_sn_pipeline'],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    include_package_data=True,
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    zip_safe=True,
)
