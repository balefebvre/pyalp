from setuptools import setup


packages = ['pyalp']

setup(
    name='pyalp',
    version='0.1.0',
    packages=packages,
    install_requires=[
        'matplotlib',
        'numpy',
        'pandas', 'IPython', 'traitlets'
    ],
)
