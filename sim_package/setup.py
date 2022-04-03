from setuptools import setup, find_packages
from Cython.Build import cythonize


setup(
    name='TrafficSimPATH',
    version='0.0.3',    
    description='A traffic simulation package made by berkeley PATH',
    url='https://github.com/ucbtrans/Fall2021/traffic_sim',
    author='Abhinav Dhulipala',
    author_email='abhinav.dhulipala@berkeley.edu',
    license='MIT',
    install_requires=['numpy',
                      'shapely',
                      'pandas',
                      'cython'
                      ],
		package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    data_files=[('dlls', ['src/sim_package/dlls/liblsp.so', 'src/sim_package/dlls/liblsp.dylib'])],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: POSIX :: Linux', 
        'Programming Language :: Python :: 3.9',
    ],
    ext_modules=cythonize("src/queue_model.pyx", language_level='3')
)
