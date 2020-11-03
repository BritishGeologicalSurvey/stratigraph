import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stratigraph",
    version="0.0.2",
    author="BGS Geosemantics",
    author_email="enquiries+geosemantics@bgs.ac.uk",
    description="Query and visualise network stratigraphy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BritishGeologicalSurvey/stratigraph",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: LGPL v3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'python-Levenshtein',
        'rdflib',
        'terminusdb-client',
        'SPARQLWrapper'
        ]

)

