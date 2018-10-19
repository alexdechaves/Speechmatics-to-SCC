from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='transcribe',
    version='0.1.0',
    description='Transcription of audio to Closed Captions',
    long_description=readme,
    author='Alex de Chaves',
    author_email='me@kennethreitz.com',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
