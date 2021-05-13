import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vmb",
    version="0.0.1",
    author="Rodrigo Diaz Leven",
    author_email="ramakandra@gmail.com",
    license = "MIT",
    # license_file = "LICENSE",
    description="HashiCorp Vault utility that backups a KV backend and other configuration, encrypting it via the transit secret engine.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bruj0/yapi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'certifi>=2019.9.11',
        'chardet>=3.0.4',
        'flatten-json>=0.1.7',
        'idna>=2.8',
        'python-box>=3.4.5',
        'PyYAML>=5.1.2',
        'requests>=2.22.0',
        'requests-toolbelt>=0.9.1',
        'six>=1.13.0',
        'urllib3>=1.25.6',
    ],
    scripts=['bin/vmb']
)
