## Open Benchmarking Initiative 

This is an effort in [SURF Open InnovationLab](https://www.surf.nl/en/the-surf-cooperative/surf-open-innovation-lab) for open and flexible benchmarking effort for experimental computing architectures. We will be using [Reframe](https://github.com/eth-cscs/reframe), a regression testing framework for HPC systems from [CSCS](https://www.cscs.ch) for this purpose. 

The set of tests are meant to be minimal set of benchmarks to understand first hand performance characteristics of the new system at the node level. It can help indentify specific bottlenecks and make the way for more specialised bechmarking and testing. These tests are itself complete in a sense that, compilation, execution and extraction of performance numbers are automated once the programming envrionment and paths are set properly. 

Currently, we are supporting following benchmarks. 

1. HPL (High Performance LinPack)
2. HPCG (High Performance Conjugate Gradient)
3. Stream (Memory Bandwidth test)
4. Gromacs (Molecular Dynamics)
5. Tensorflow-gpu (Deep Learning)
6. Isogeometric Analysis (Advanced Finite Element Analysis) : https://github.com/gismo/gismo
7. QUEST (Simulating quantum circuits on a supercomputers ) : https://quest.qtechtheory.org

We will be adding more benchmarks on the requirement basis. It also depends on the qualitative understanding the benchmarks provides us for a specific machine architecture and degree of portability and easy of use of the benchmark. 

### How to use this

Basically there are three simple tests to run the benchmarks

1. Setup the programming environment. 
2. Install the libraries. 
3. Change the configuration files and run / design the tests.  

#### Programming Environment

1. C/ C++ Compiler (GCC, Intel, Clang)
2. MPI Implementation available (**OpenMPI, IntelMPI, MPICH and Mvapich**)
3. CUDA (Optional)

#### Software Requirements

1. OpenBLAS Implementation (GCC OpenBLAS, MKL) 
    1. GCC OpenBLAS :   https://github.com/xianyi/OpenBLAS
    2. Intel MKL : https://software.intel.com/en-us/mkl

#### Changing the configuration file and tests files. 

The `Reframe` scripts and configration files work with python and they try to emulate submission of job via a resource manager on a supercomputer (e.g SLURM) or local job submission. The test and configuration files are itself meant to be scalable and easy for extension. 

### Running the test

<description of the test>

### Test systems 

The benchmark work on the following three systems. 

1. Cartesius nodes (Dutch National Supercomputer)
2. Intelinx (Experimental system with GPU + FPGA, at **SURFsara, Amsterdam**)
3. EPYDIA (Experimental system at **University of Amsterdam** : EPYC Naples + NVIDIA GPUs)

#### Contacts 

If you would like to include your test or have any questions regarding the usage or inclusion of the test please do not hesitate to contact us : 

Sagar dolas (sagar.dolas@surfsara.nl)  
Project Lead and HPC Adviser - SURF
