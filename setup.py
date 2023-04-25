import setuptools

setuptools.setup(
    name="tass",
    version="0.1.0",
    author="Statistics Canada",
    author_email="",
    packages=["tass"],
    description="Automation framework",
    url="https://github.com/StatCan/tass-ssat/",
    license='Apache 2.0',
    python_requires='>=3.8',
    install_requires=["jsonschema", "selenium", "webdriver-manager"]
 )
