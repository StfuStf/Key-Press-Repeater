from setuptools import setup, find_packages

setup(
    name='key-press-repeater',
    version='1.0.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pynput',
        'Xlib',
    ],
    entry_points={
        'console_scripts': [
            'key-press-repeater=key_press_repeater:main',
        ],
    },
    include_package_data=True,
    description='A tool to automate key presses at specified intervals.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/key-press-repeater',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ],
)
