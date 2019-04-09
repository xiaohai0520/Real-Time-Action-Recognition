# action_recognition_on_C3D
A small program for action recognition on C3D

<iframe width="560" height="315" src="https://www.youtube.com/embed/6_QowqAsjWs" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
## Content
- [Deployment](#deployment)
- [Usage](#usage)
  - [Input](#input)
  - [Output](#output)
- [Anaylsis](#analysis)
  - [Influence](#influence)
  - [Optimization](#optimization)
- [Reference](#reference)

# Deployment

The program depends on the graph database Neo4j. *[Here is the link for Neo4j on the github](https://github.com/neo4j/neo4j)*


# Usage

```
Clusters unweighted undirected input network (graph) considering overlaps and
building Exact Structural Graph

Usage: RUN_PSCAN [OPTIONS]... [input_network]...

input_network  - the input graph specified as a file in the TXT type.

  -inputnetwork        Path of the data file.
  -outputnetwork       Mode of the graph database.
  -eps                 The threshold of the similar for the clusters.
  -miu                 The least number for the clusters.
```
For example
```
$java RUN_PSCAN ./data/data.txt ./model 0.51 4

```

## Input
The undirected unweighted input network to be clustered is specified in the TXT format files:


```
# Example Network
# Nodes number  
9
# Note that the links in the database
0 1
0 2
2 1
```
## Output
The CNL (clusters nodes list) output is a standard format. For example:
```
eps: 0.51  miu:4

All nodes:
[0,1,2,3,4,5,6,7,8,9]

Core clusters:
[0,1,2,3],[5,6,7,8]

non cores:
[4,9]

All clusters:
No1: [0,1,2,3,4]
No2: [4,5,6,7,8,9]

``` 
<img width="400" height="200" src=https://github.com/xiaohai0520/PSCAN_on_Neo4j/blob/master/image/Picture1.png/>

# Analysis

## Influence
We do the test for running time on different parameters to test the influence for parameters.
<img width="400" height="200" src=https://github.com/xiaohai0520/PSCAN_on_Neo4j/blob/master/image/influence.jpg/>

## Optimization
We implement three optimizations in the pSCAN.

### cross link
- Cut half of the calculate times in process of checking core.
### Pruning rule 
- Find out which vertex pairs are not structure similar before checking.
### Adaptive structure-similar checking 
- Compute the minimum number of common neighbors, terminate early if any vertex can match the minimum condition.

<img width="400" height="200" src=https://github.com/xiaohai0520/PSCAN_on_Neo4j/blob/master/image/op.jpg/>


# Reference
The paper: *["pSCAN: Fast and Exact Structural Graph Clustering"](https://www.cse.unsw.edu.au/~ljchang/pdf/icde16-pscan.pdf) by Lijun Chang, Wei Li, Xuemin Lin,Lu Qin and Wenjie Zhang, ICDE'16*.
