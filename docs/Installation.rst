===============
Getting started
===============

Get ready
=========


**Setup your Python Environment**

Make sure you have `Python <https://www.python.org/downloads/>`_ and `Anaconda <https://docs.anaconda.com/anaconda/install/>`_ or `Miniconda <https://docs.conda.io/en/latest/miniconda.html#latest-miniconda-installer-links>`_
installed on your system.

**Download the code from Github**

Next, please make sure you have `Git already installed <https://git-scm.com/downloads>`_ installed on your system.
For a user-friendly experience, `GitHub Desktop <https://desktop.github.com/>`_ is a nice software tool.

Next, create a folder and go to this folder. Clone this repository to your local path.

.. code-block:: console

    (base) C:\Users\Username\Code> $ git clone https://github.com/DaetwylerStephan/multi-scale-image-analysis.git


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

   (imageanalysis_env) MyComputer ~/multiScaleAnalysis $ pip install .


Now you can start executing the scripts and test them using the testdata provided on Synapse.

Synapse account
===============

Our data is available on Synapse, the official storage of National Institute of Health, MC2 centers.
If you are interested in it, please check out:
https://help.synapse.org/docs/Getting-Started.2055471150.html