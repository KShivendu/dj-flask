from setuptools import find_packages, setup

setup(
    name="dj_flask",
    packages=find_packages(include=["dj_flask"]),
    version="0.1.0",
    description="A library that allows you to write code that is compatible with Django as well as Flask",
    author="shivendu@iitbhilai.ac.in",
    license="MIT",
    install_requires=["Django==3.2.5", "flask==2.0.1"],
    # setup_requires=["pytest-runner"],
    # tests_require=["pytest==4.4.1"],
    # test_suite="tests",
)
