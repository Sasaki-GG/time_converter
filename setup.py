from setuptools import setup
import setuptools

setup(name="time_converter_0.8",
      version="0.8.5",
      keywords=("time", "nlp"),
      author="GG",
      author_email="gg.pan@foxmail.com",
      description="...",
      long_description="...",
      license="MIT Licence",
      packages=setuptools.find_packages(),
      package_data={
          'time_converter':
          ['resource/*.json', 'resource/*.pkl', 'resource/*.txt']
      },
      include_package_data=True,
      install_requires=['regex>=2017', 'arrow>=0.15.2'],
      zip_safe=False,
      classifiers=['Programming Language :: Python :: 3.6'])
