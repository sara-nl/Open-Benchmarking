## Open Benchmarking Initiative - SURF

This is an effort in [SURF Open Innovation Lab](https://www.surf.nl/en/the-surf-cooperative/surf-open-innovation-lab) for open and flexible benchmarking effort for experimental computing architectures. We will be using [Reframe](https://github.com/eth-cscs/reframe), a regression testing framework for HPC systems from [CSCS](https://www.cscs.ch) for this purpose. 

> The set of tests are meant to be the minimal set of benchmarks to understand performance characteristics of
> the at the node level. It can help identify specific bottlenecks and make the way for more specialised     
> benchmarking and testing. These tests are itself complete in a sense that, compilation, execution and 
> extraction of performance numbers are automated once the programming environment and paths are set properly. 

Currently, the following benchmarks are included. 

1. HPL (High Performance LinPack)
2. HPCG (High Performance Conjugate Gradient)s
3. Stream (Memory Bandwidth test)
4. Gromacs (Molecular Dynamics)
5. Tensorflow-gpu (Deep Learning)
6. [Isogeometric Analysis (Advanced Finite Element Analysis)]( https://github.com/gismo/gismo)
7. [QUEST (Simulating quantum circuits on the Supercomputers )](https://quest.qtechtheory.org)


### How to use ? 

Basically there are three simple tests to run the benchmarks
1. Setup the programming environment. 
2. Install the libraries.
3. Change the configuration files and run / design the tests depending on number of CPU cores. 

#### Programming Environment 

1. C/ C++ Compiler (GCC, Intel, Clang)
2. MPI Implementation available (**OpenMPI, IntelMPI, MPICH and Mvapich**)
3. CUDA (Optional)

#### Software Requirements

1. OpenBLAS Implementation (GCC OpenBLAS, MKL) 
    1. [GCC OpenBLAS](https://github.com/xianyi/OpenBLAS)
    2. [Intel MKL](https://software.intel.com/en-us/mkl)

#### Changing the configuration file and tests files. 

The `Reframe` scripts and configration files work with python and they try to emulate submission of job via a resource manager on a supercomputer (e.g SLURM) or local job submission. The test and configuration files are itself meant to be scalable and easy for extension. 

There are few environment variable which needs to be specified before running the test in the config file. 

1. `ROOTOPENMPI` : Installation directory of MPI library.
2. `ROOTOPENBLAS` : Installation directory of OpenBLAS. 
3. `CUDAHOME`: Installation directory of CUDA.
4. `LD_LIBRARY_PATH` : to make libraries available in the path while executing the application. 

### Running the test

1. Make a virtual environment with Python >= 3.5. 
2. git clone this repository 
3. Activate the virtual environment
4. pip install reframe-hpc

#### Run this command 

**`reframe --config-file /path/to/configuration/file  --checkpath /path/to/tests --recursive -r --performance-report --exec-policy async --system <name of your system> -t <name of the tag if any> --partition <your logical partition>`**

### Test systems 

The benchmark work on the following three systems. 

1. Cartesius nodes (Dutch National Supercomputer)
2. Intelinx (Experimental system with GPU + FPGA, at **SURFsara, Amsterdam**)
3. EPYDIA (Experimental system at **University of Amsterdam** : EPYC Naples + NVIDIA GPUs)

#### Contacts 

If you would like to include your test or have any questions regarding the usage or inclusion of the test please do not hesitate to contact us : 

**Sagar dolas** (sagar.dolas@surfsara.nl)  
Project Lead and HPC Adviser - SURF
