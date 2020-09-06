# Adamsplantprocessing


You will need the lastest version of Anaconda.
you will need unity 2019.2.5f1 from the unity hub arcive. 
you will need Visual Studio 2017 and 2019.

Pc is the only build enviroment supported at the moment. but can be deployed to the following:

    Linux: CentOS 7 (RedHat Enterprise Linux)
    Linux: Ubuntu 12.04, 14.04, and 16.04
    Linux: Raspbian "Jessie"
    Mac OSX 10.11 and macOS 10.12+
    Windows 10
    Cloud9 IDE


you will need to pip install the following though it is included in the unity projects. just save your breath and have it installed first.

    Python (tested with versions 2.7, 3.6, and 3.7)
        argparse
        cv2 (a.k.a. OpenCV; some functions require 3.0+, we recommend 3.3+. We install it via the PyPI package opencv-python)
        matplotlib (requires at least 1.5, works with 2+)
        numpy (requires at least 1.11)
        pandas
        python-dateutil
        scikit-image
        scikit-learn
        scipy
        plotnine
        setuptools
        pytest (only used for running tests)

Optional but recommended

    conda (Anaconda or Miniconda)
    git
    Jupyter
    spyder IDE
    Rider IDE
    
    
    then you will need to do the following
    
    PyPI

To install from PyPI run the following in any type of virtual environment, as an administrator, or add the --user flag if needed.

pip install plantcv

Conda

To install using conda first install Anaconda or Miniconda if you have not already. If needed, add the following channels to your conda configuration.

conda config --add channels bioconda
conda config --add channels conda-forge
conda config --add channels defaults
conda config --set channel_priority strict

Then create an environment and install PlantCV.

conda create -n plantcv plantcv

Or install PlantCV in your current environment.

conda install plantcv

Fellow Developers and not script kitties see here for Advanced documentation on the dependency. They are an amazing team.
https://plantcv.readthedocs.io/en/stable/installation/


Next you will need to go to the following links and install IronPython and  ironclad. its so we can use certain DLL files and pyd files.
https://ironpython.net/download/
https://code.google.com/archive/p/ironclad/



after all this is done, navigate and open the unity hub.
Open the unity project and Bam edit and deploy to your hearts content. 
    

