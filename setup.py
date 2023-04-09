from setuptools import find_packages, setup

setup(
    name='bennie',
    version='0.1.0',
    author='Michael Lamertz',
    author_email='michael.lamertz@gmail.com',
    url='https://github.com/dickerdackel/bennie',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'bennie = bennie.app:main',
            'tbennie = bennie.terminal:main',
            'hex2json = bennie.hex2json:main',
        ],
    },
)
