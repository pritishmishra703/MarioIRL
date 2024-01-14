from setuptools import setup, find_packages

setup(
    name='MarioIRL',
    version='1.0',
    author='Pritish Mishra',
    author_email='pritishjan@gmail.com',
    description='Play Mario In Real Life',
    packages=find_packages(),
    install_requires=[
        'streamlit',
        'pandas',
        'matplotlib'
    ],
)
