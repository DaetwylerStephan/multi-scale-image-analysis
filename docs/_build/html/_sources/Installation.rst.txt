===============
Getting started
===============

Requirements
============

The analysis code relies on GPU analysis. Therefore, a graphics card with Nvidia
drivers is required for running the code. We tested the code on Linux and Windows.

Get ready
=========


**Setup your Python Environment**

Make sure you have `Python <https://www.python.org/downloads/>`_ and `Anaconda <https://docs.anaconda.com/anaconda/install/>`_ or `Miniconda <https://docs.conda.io/en/latest/miniconda.html#latest-miniconda-installer-links>`_
installed on your system.

**Download the code from Github**

Next, please make sure you have `Git already installed <https://git-scm.com/downloads>`_ installed on your system.
For a user-friendly experience, `GitHub Desktop <https://desktop.github.com/>`_ is a nice software tool.

Next, create a folder and go to this folder. Clone this repository to your local path, e.g. in the Anaconda Prompt.

.. code-block:: console

    (base) C:\Users\Username\Code> $ git clone https://github.com/DaetwylerStephan/multi-scale-image-analysis.git

.. image:: images/anaconda_clonegit.png


Software installation
=====================

**Create and activate a Python environment called imageanalysis_env**

.. code-block:: console

   (base) MyComputer ~ $ conda create -n imageanalysis_env python=3.9 cudatoolkit=11.8.* cudnn==8.* -c anaconda

Note: This environment uses Python version 3.9 and sets the cuda tool kits for GPU-based computation.

Next, activate the environment:

.. code-block:: console

   (base) MyComputer ~ $ conda activate imageanalysis_env

**Installation of the packages**

Now navigate to the folder "multiScaleAnalysis", where the setup.py and requirements.txt file are located,
and install the packages:

.. code-block:: console

   (imageanalysis_env) MyComputer ~$ cd multi-scale-image-analysis
   (imageanalysis_env) MyComputer ~/multiScaleAnalysis $ pip install .


Now you can start executing the scripts and test them using the testdata provided on Synapse.


Running and editing functions with PyCharm
==========================================

After establishing the Conda environment and installing all functions with "pip install ." in the
Anaconda prompt, open your favorite IDE to modify and run code. Here, we use PyCharm.

First open your folder as project in PyCharm in File>Open...

.. image:: images/open_project.png

Next, we want to add the environment to our project. For this go to File>Settings... and choose
your recently established Conda environment.

.. image:: images/add_environment.png

and next

.. image:: images/add_environment2.png

Now the Terminal is ready for input:

.. image:: images/open_commandPrompt.png

And we can change the file path in the script to the location of the downloaded test datasets,
e.g. in the script to analyse :ref:`PSF values <PSFanalysis>`.
To run the script, we need to go to the folder
with the python function and enter "python PSF_measurements.py".

.. code-block:: console

   (imageanalysis_env) MyComputer ~/multiScaleAnalysis $ cd Tools
   (imageanalysis_env) MyComputer ~/multiScaleAnalysis $ python PSF_measurements.py



.. image:: images/run_script.png


Test data location
==================

Data to test our code is available on

:Zenodo: https://doi.org/10.5281/zenodo.12791724

The raw data for all our analysis (several TBs) is available on Synapse,
the official storage of National Institute of Health, MC2 centers:

:Experiment Collection: https://doi.org/10.7303/syn61795837
:Code Example Datasets Collection: https://doi.org/10.7303/syn61795850

If you are interested in it, please check out:
https://help.synapse.org/docs/Getting-Started.2055471150.html