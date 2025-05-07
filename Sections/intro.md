# Bottleneck Informed Network Design for Distributed Machine Learning

## Introduction

For a given Network Topology, in this work we aim to find a **wasteless design** for a parallelizable Machine Learning
task.
A network design associates capacities to the links in a Network Topology (i.e. a network slice).
A wasteless design achieves maximal performance at the lowest possible cost.

(**Theorem 1**) For a given Topology (**T**) and Traffic Pattern (**P**), if a Design (**D**) is wasteless, then it is
impossible to improve on the network completion time or network throughput of the design without adding more
capacity. [[1]](https://arxiv.org/abs/2210.03534)

This grants us the following properties:

* No bandwidth wasted;
* All flows terminate at the same time;
* Network completion time is the smallest possible without adding more capacity;
* Network throughput is the highest possible without adding more capacity.
