from setuptools import setup, find_packages


def read(filename):
    with open(filename, encoding='utf-8') as file:
        return file.read()


setup(
    name='ttbotapi',
    version='0.3.0',
    description='TamTam Bot API library',
    long_description=read("README.md"),
    long_description_content_type='text/markdown',
    author='Mustafa Asaad',
    author_email='ma24th@yahoo.com',
    url='https://github.com/MA24th/ttbotapi',
    packages=find_packages(),
    classifiers=['Development Status :: 5 - Production/Stable',
                   'Framework :: ttbotapi'
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   'Programming Language :: Python :: 3.9'],
    license='GNU GPLv2',
    install_requires=['requests']
)
