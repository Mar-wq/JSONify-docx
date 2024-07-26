from setuptools import setup, find_packages

setup(
    name='JSONify-docx',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'lxml==5.2.2',
        'more-itertools==10.3.0',
        'pillow==10.4.0',
        'python-docx==1.1.2',
        'setuptools==69.5.1',
        'typing_extensions==4.12.2',
        'wheel==0.43.0',
        'webcolors==24.6.0',
    ],
    author='Hdy',
    author_email='977648857@qq.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
)
