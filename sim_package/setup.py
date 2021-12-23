from setuptools import setup, find_packages


setup(
    name='TrafficSimPATH',
    version='0.0.1',    
    description='A traffic simulation package made by berkeley PATH',
    url='https://github.com/ucbtrans/Fall2021/traffic_sim',
    author='Abhinav Dhulipala',
    author_email='abhinav.dhulipala@berkeley.edu',
    license='MIT',
    install_requires=['numpy',
                      'scipy',
                      'shapely',
                      'pandas'
                      ],
		package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    data_files=[('dlls', ['src/sim_package/dlls/liblsp.so'])],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: POSIX :: Linux', 
        'Programming Language :: Python :: 3.9',
    ],
)
