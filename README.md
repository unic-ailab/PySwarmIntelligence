# Bachelor Thesis: Swarm Intelligence from nature to applied science
**Author**: Themistoklis Alexandrou  
**Supervisor**: Dr. Demetris Trihinas

## Repository Information  
This repository contains all of the Python scripts written and used in order to be able to make a user-friendly GUI that the user will be able to perform experiments and visualize the three Swarm Inttelligence Algorithms that this Thesis is occupied with: 
1. Ant Colony Optimization Algorithm (ACO) 
2. Bird Swarm Algorithm (BSA) 
3. Firefly Algorithm (FA)  

### File Descriptions

**Main Screen**  
- **[myMain.py](https://github.com/unic-ailab/PySwarmIntelligence/blob/master/ptyxiaki/myMain.py)** - This Python script is the main menu of the program where the user can select which algorithm wants to be vizualized with its own configuration

**Ants**
- **[ants.py](https://github.com/unic-ailab/PySwarmIntelligence/blob/master/ptyxiaki/ants.py)** - This Python script was written for the implementation and visualization of the ACO algorithm. The user can input the configuration that desires based on the variables given, see the visualization of the algorithm in real time and then get the results based on time and CPU performance

**Birds**
- **[birds.py](https://github.com/unic-ailab/PySwarmIntelligence/blob/master/ptyxiaki/birds.py)** - This Python script was written for the implementation of the three main characteristics that birds have when they are forming a swarm:
1. Alignment
2. Cohesion  
3. Separation

- **[drawing_birds.py](https://github.com/unic-ailab/PySwarmIntelligence/blob/master/ptyxiaki/drawing_birds.py)** - This Python script was written for the visualization of the BSA algorithm. The user can input the configuration that desires based on the variables given, see the visualization of the algorithm in real time and then get the results based on time and CPU performance. The user also throught the sliders of each variable can alter the main configuration and create a new one.  

**Fireflies**  
- **[fireflies.py](https://github.com/unic-ailab/PySwarmIntelligence/blob/master/ptyxiaki/fireflies.py)** - This Python script was written for the implementation of the main characteristics that Fireflies have when they are forming a swarm and give the get the results based on time and CPU performance.
- **[data_generator.py](https://github.com/unic-ailab/PySwarmIntelligence/blob/master/ptyxiaki/data_generator.py)** - This Python script is used for the generation of the fireflies in regards to the problem dimension
- **[benchmark_functions.py](https://github.com/unic-ailab/PySwarmIntelligence/blob/master/ptyxiaki/benchmark_functions.py)** - This Python script contains the two benchamark functions of the FA algorithm:    
**1. Ackley**  
        The Ackley function is widely used to test optimization algorithms.
        The function poses a risk for optimization algorithms, particularly hill-climbing algorithms, 
        to be trapped in one of its many local minima.  
**2. Michalewicz**  
        The Michalewicz function is a math function that is used to test the effectiveness of numerical optimization algorithms
        The function can accept one or more input values. The function is tricky because there are 
        several local minimum values and several flat areas which make the one global minimum 
        value hard to find for algorithms.  
- **[visualize_ackley.py](https://github.com/unic-ailab/PySwarmIntelligence/blob/master/ptyxiaki/visualize_ackley.py)** - This Python script was written for the visualization of the FA algorithm. 
- **[visualize_michalewicz.py](https://github.com/unic-ailab/PySwarmIntelligence/blob/master/ptyxiaki/visualize_michalewicz.py)** - This Python script was written for the visualization of the FA algorithm. 

## Abstract  
For artificial intelligence (AI), the past decade, and especially the past few years, has been transformative not so much in terms of what we can do with this technology as what we are doing with it. Smart machines like smart cars, smart houses, smart assistants become more and more a part of our everyday life. All these machines become smarter and smarter by communicating with each other with simple means and rules like a real-life swarm of animals for example. This is based on the AI notion of Swarm Intelligence (SI) which is the direct result of self-organization in which the interactions of lower-level components create a global-level dynamic structure that is regarded as intelligence. The following paper examines three of the most famous SI algorithms Ant Colony Optimization (ACO), Bird Swarm Algorithm (BSA) and Firefly Algorithm (FA) by implementing an experiment testbed, evaluating them under different scenarios by adapting parameterisation and visualizing them. After reading the paper, one realises that nature always is teaching the humanity new things through the simpler means so nature must be respected because it has a lot more to give to the science society.
