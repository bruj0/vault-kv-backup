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
        'hvac==0.10.11'
    ],
    scripts=['bin/vmb']
)
