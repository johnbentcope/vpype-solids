from setuptools import setup

with open("README.md") as f:
    readme = f.read()

setup(
    name="vpype-solids",
    version="0.0.1",
    description="vpype plugin to generate renders of three dimensional scenes",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="John Cope",
    url="https://github.com/johnbentcope/vpype-solids",
    packages=["vpype_solids"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Topic :: Multimedia :: Graphics",
        "Environment :: Plugins",
    ],
    install_requires=[
        'click',
        'vpype>=1.9,<2.0',
        'numpy',
    ],
    entry_points='''
            [vpype.plugins]
            vpype_solids=vpype_solids.vpype_solids:vpype_solids
        ''',
)
