## Open Benchmarking Initiative 

This is an effort in [SURF Open InnovationLab](https://www.surf.nl/en/the-surf-cooperative/surf-open-innovation-lab) for open and flexible benchmarking effort for experimental computing architectures. We will be using [Reframe](https://github.com/eth-cscs/reframe), a regression testing framework for HPC systems from [CSCS](https://www.cscs.ch) for this purpose. 

The set of tests are meant to be minimal set of benchmarks to understand first hand performance characteristics of the new ystem. It can help indentify specific bottlenecks and make the way for more specialised bechmarking and testing. These tests are itself complete in a sense that, compilation, execution and extraction of results are automated once the programming envrionment and paths are set. 

Currently, we are supporting following benchmarks. 

1. HPL (High Performance LinPack)
2. HPCG (High Performance Conjugate Gradient)
3. Stream (Memory Bandwidth test)
4. Gromacs
5. Tensorflow-gpu

We will be adding more benchmarks on the requirement basis. It also depends on the qualitative understanding benchmarks provide for a specofic machine architecture and degree of portability of the benchmark. 

### How to use this

Basically there are three simple tests to run the benchmarks

1. Setup the programming environment. 
2. Install the libraries. 
3. Change the configuration files and design the tests.  

#### Programming Environment

#### Software Requirements

#### Changing the configuration file and tests files. 

### Running the test

<> ... more to come

### Test systems 

We have been using these tests to benchmark following three systems. 

1. Cartesius (Dutch National Supercomputer)
2. Intelinx (Experimental system with GPU + FPGA, at **SURFsara**)
3. EPYDIA (Experimental system at **University of Amsterdam** having epyc Naples + NVIDIA GPUs)

#### Contacts 

If you would like to include your test or have any questions regarding the inclusion of the test please do not hesitate to contact us : 

Sagar dolas (sagar.dolas@surfsara.nl)  
Project Lead and HPC Adviser - SURF
