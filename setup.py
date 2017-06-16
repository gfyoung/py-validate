from setuptools import setup
from py_validate import __version__ as validate_version

setup(
    name="py_validate",
    version=validate_version,
    packages=["py_validate",
              "py_validate.backend",
              "py_validate.tests",
              "py_validate.tests.backend",
              "py_validate.tests.validator"],
    include_package_data=True,
    license="MIT License",
    description="Python function validators",
    long_description="py-validate is a library that provides easy-to-use\n"
                     "wrappers for checking inputs and outputs of a function\n"
                     "without cluttering implementation with verification\n"
                     "checks. Wrappers nicely abstract away these checks\n"
                     "and are very customizable for each function.",
    download_url="https://github.com/gfyoung/py-validate",
    url="https://github.com/gfyoung/py-validate",
    author="G. Young",
    bugtrack_url="https://github.com/gfyoung/py-validate/issues",
    keywords="python validate wrapper function",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Pre-processors",
    ]
)
