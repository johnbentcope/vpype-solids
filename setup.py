from setuptools import setup


with open("README.md") as f:
    readme = f.read()

setup(
    name="vpype-solids",
    version="0.1.0",
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
    setup_requires=["wheel"],
    install_requires=[
        'click',
        'vpype[all]>=1.10,<2.0',
    ],
    entry_points='''
            [vpype.plugins]
            vpype_solids=vpype_solids.vpype_solids:vpype_solids
        ''',
)
