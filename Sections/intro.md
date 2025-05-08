# Bottleneck Informed Network Design for Distributed Machine Learning

## Introduction

For a given Network Topology, in this work we aim to find a **wasteless design** for a parallelizable Machine Learning
task.
A network design associates capacities to the links in a Network Topology (i.e. a network slice).
A wasteless design achieves maximal performance at the lowest possible cost.

Network Model:
* Links      
* Design
* Traffic Pattern

> **(Definition: Wasteless designs)**. For a given topology and traffic pattern **b**, a design **c** is wasteless if 
> all the bandwidth of each link is used throughout the transmission.
> 
> **(Theorem: Optimality of Wasteless Design)** For a given Topology and Traffic Pattern, if a Design **c** is 
> wasteless, then it is impossible to improve on the network completion time or network throughput of the design 
> without adding more capacity. 

> **(Definition: Proportional Designs)**. For a given traffic pattern b, a design c is proportional if each link’s capacity 
> is proportional to the sum of the sizes of the flows that traverse it. That is,
> $$\begin{aligned}c(l) = \alpha \sum_{f \in \mathcal{F}_l} b(f)\end{aligned}$$
> 
> **(Theorem: Non-proportional designs waste bandwidth)**. If a design wastes no bandwidth on a given traffic pattern, 
> then it is the proportional design for that traffic pattern.

> **(Definition: Interference-free)**. For a given topology, a traffic pattern b is said to be interference-free if each 
> flow **f** traverses some link **l** that is traversed by no flow that transmits more bits than **f**. 
> 
> **(Theorem: Interference-free proportional designs are wasteless)**. If the traffic pattern is interference free, 
> then the proportional design wastes no bandwidth and all flows finish transmitting at the same time.

This grants us the following properties:

* No bandwidth wasted;
* All flows terminate at the same time;
* Network completion time is the smallest possible without adding more capacity;
* Network throughput is the highest possible without adding more capacity.
