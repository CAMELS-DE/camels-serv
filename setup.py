from setuptools import setup, find_packages


def requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()


def readme():
    with open('README.md') as f:
        return f.read()


def version():
    with open('camels_serv/__version__.py') as f:
        loc = dict()
        exec(f.read(), loc, loc)
        return loc['__version__']

setup(
    name='camels_serv',
    author='Mirko Mälicke',
    author_email='mirko@hydrocode.de',
    version=version(),
    packages=find_packages(),
    install_requires=requirements(),
    description='Camels server data API',
    long_description=readme(),
    long_description_content_type='text/markdown',
    license='GPL v3'
)
