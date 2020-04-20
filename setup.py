import setuptools
with open('README.md', 'r') as fh:
	long_description = fh.read()
setuptools.setup(
	name='stockquotes',
	version='1.0.5',
	description='A simple module for retreiving stock data',
	long_description=long_description,
	long_description_content_type="text/markdown",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"Operating System :: OS Independent"
	],
	python_requires='>=3.0'
)
