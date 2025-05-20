## Network Model

> **(Definition: Network)** We say that a tuple $\mathcal{N} = \langle \mathcal{L}, \mathcal{F}, \{c_l, \forall l\in \mathcal{L}\} \rangle$ is a network
> if:
> * $\mathcal{L}$ is a set of links of the form $\{l_1, l_2, ..., l_{\mathcal{|L|}} \}$,
> * $\mathcal{F}$ is a set of flows of the form $\{f_1, f_2, ..., f_{\mathcal{|F|}} \}$,
> * $c_l$ is the capacity of link $l$, for all $l \in \mathcal{L}$.

> **(Definition: Network Design)** Let $\mathcal{L}$ be the set of links in  a given data center network. A network design 
> (or simply a  design) is a function $c : \mathcal{L} \rightarrow \mathbb{R}_{> 0}$ mapping each link to its capacity. 
> We use the notation $c_l$ interchangeably with $c(l)$.

> **(Definition: Network Completion Time)** Let $\mathcal{L}$ and $\mathcal{F}$ be the sets of links and flows, and let 
> $b$ be the traffic pattern. Assume all flows start transmitting data at the same time. For a given design $c$, let $fct(b, c, f)$ be 
> the time it takes for flow $f$ to complete transmitting its $b(f)$ units of data. Then,  $\mu(b, c) = max_{f \in \mathcal{F}} fct(b,c,f)$ is 
> the completion time of the  network for the given traffic pattern and design.
> 
> **(Definition: Network Throughput)** For a given traffic pattern $b$ and design $c$, let $bct(b, c, n)$ be the smallest possible  
> time to complete transmitting $n$ batches when using the best scheduling. Then, the *network throughput* of the design is  
> $T(b, c) = \lim\limits_{n \rightarrow \infty}  \frac{n}{bct(b, c, n)}$.

> **(Definition: Traffic Pattern)** Let $\mathcal{H}$ be the set of hosts in a given interconnect. Then a *traffic pattern*
> is a function $b: \mathcal{H} \times \mathcal{H} \rightarrow \mathbb{R}_{\geq 0}$ mapping each ordered pair of hosts to  
> the amount of data (e.g., in bits) to be transmitted from the  first to the second.

> **(Definition: Wasteless designs)** For a given topology and traffic pattern $b$, a design $c$ is wasteless if 
> all the bandwidth of each link is used throughout the transmission. That is, $\forall t \in [0, \mu(b, c)], \sum_{f \in \mathcal{F_l}}r_{c,b}(f, t) = c(l)$, 
> where $\mathcal{F}_l$ is the set of flows that traverse $l$ and $r_{c,b}(f, t)$ is the rate of flow $f$ at time $t$ for design $c$ and traffic pattern $b$ according
> to the congestion control algorithm.
> 
> **(Theorem: Optimality of Wasteless Design)** Optimality of wasteless designs. For a given topology and traffic pattern, 
> if a design c is wasteless, then it is impossible to improve on the network completion time or network throughput of the design 
> without adding more capacity. That is, if $c'$ is an alternative design for which $\mu(b, c') < \mu(b, c)$ or $T(b, c') > T(b, c)$, 
> then $\sum_{l \in \mathcal{L}} c'(l) > \sum_{l \in \mathcal{L}} c(l)$.

> **(Definition: Proportional Designs)**. For a given traffic pattern b, a design c is proportional if each link’s capacity 
> is proportional to the sum of the sizes of the flows that traverse it. That is,
> $$\begin{aligned}c(l) = \alpha \sum_{f \in \mathcal{F}_l} b(f)\end{aligned}$$
> 
> **(Theorem: Non-proportional designs waste bandwidth)**. If a design wastes no bandwidth on a given traffic pattern, 
> then it is the proportional design for that traffic pattern.

> **(Definition: Interference-free)**. For a given topology, a traffic pattern b is said to be interference-free if each
> flow $f$ traverses some link $l$ that is traversed by no flow that transmits more bits than $f$. That is, $\forall f \in \mathcal{F}, \exists l \in \mathcal{L}$ s.t. $f \in arg max_{f'\in\mathcal{F}_l}b(f')$.
> 
> **(Theorem: Interference-free proportional designs are wasteless)**. If the traffic pattern is interference free, 
> then the proportional design wastes no bandwidth and all flows finish transmitting at the same time.

## References

* Jordi Ros-Giralt, Noah Amsel, Sruthi Yellamraju, James Ezick, Richard Lethin,
Yuang Jiang, Aosong Feng, and Leandros Tassiulas. 2022. A Quantitative Theory
of Bottleneck Structures for Data Networks. arXiv:2210.03534 [cs.NI] https:
//arxiv.org/abs/2210.03534

* Jordi Ros-Giralt, Noah Amsel, Sruthi Yellamraju, James Ezick, Richard Lethin,
Yuang Jiang, Aosong Feng, Leandros Tassiulas, Zhenguo Wu, Min Yee Teh, and
Keren Bergman. 2021. Designing data center networks using bottleneck structures.
In Proceedings of the 2021 ACM SIGCOMM 2021 Conference (Virtual Event, USA)
(SIGCOMM ’21). Association for Computing Machinery, New York, NY, USA,
319–348. doi:10.1145/3452296.3472898