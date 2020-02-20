# Chilean Top AI Conference Publications

We report the total publication count from 2015 to 2020 of Chilean authors in top AI conferences, and compare this number with the total number of publications on that conferences by researchers in our "AI & Society" institute proposal. 
The researchers in the proposal are:

* Associate Researchers: Barbara Poblete, Jorge Pérez, Felipe Tobar, Denis Parra, Marcelo Mendoza, Jorge Silva, Alex Bergel, Valeria Herskovic, Jorge Baier, Fernando Rosenblatt, Claudia Lopez, Claudia Prieto, Monica Gerber 
* Young Researchers (to be completed): Jocelyn Dunstan, Felipe Bravo, Julio Godoy 


Our results show that as of February 2020, **91.7% of all AI top-conference publications by Chileans have a co-author that is part of our proposal**.
Below we show our methods, a summary of our results and the code to replicate this numbers.




## Methods

We consider the following international conferences that are listed by Google Scholar as the [top 5 conferences in AI](https://scholar.google.com/citations?view_op=top_venues&hl=en&vq=eng_artificialintelligence)

|rank|conference|name|h5-index|h5-median|
|:--:|:---------|:---|:------:|:-------:|
|1|NeurIPS|Neural Information Processing Systems (ex NIPS)|169|334|
|2|ICLR| International Conference on Learning Representations    |150 |276|
|3|ICML| International Conference on Machine Learning|135 |254|
|4|AAAI| AAAI Conference on Artificial Intelligence  |95  |153|
|5|IJCAI|International Joint Conference on Artificial Intelligence| 67 |100|

To construct the data for Chilean authors in AI we consider all authors listed at [Google Scholar](https://scholar.google.com/citations?view_op=search_authors) that have a verified email ending with `.cl` (which means  authors are currently affiliated with a Chilean institution) and that declare any of the following keywords as research topics.

* `artificial_intelligence`
* `machine_learning`
* `computational_intelligence`
* `computer_vision`
* `natural_language_processing`
* `data_science`
* `data_mining`

To search for publications for everyone of the authors found above, we consider all the publications listed by [DBLP](https://dblp.uni-trier.de/) between 2015 and 2020.

## Results

We found a total of 24 publications with at least one Chilean author for the above listed conferences. From them, 22 are co-authored by at least one researcher in our proposal. 
This gives a total of 91.7% of all AI top-conference publications by Chileans attributed to researchers in our proposal.
The total list of publications, sorted by date of publication, is shown below.

* AAAI 2020 Solving Sum-of-Costs Multi-Agent Pathfinding with Answer-Set Programming. Rodrigo Gómez, **Jorge Baier**, Carlos Hernandez
* NeurIPS 2019 Band-Limited Gaussian Processes: The Sinc Kernel. **Felipe Tobar**
* ICLR 2019 On the Turing Completeness of Modern Neural Network Architectures. **Jorge Pérez**, Javier Marinkovic, Pablo Barceló
* NeurIPS 2018 Bayesian Nonparametric Spectral Estimation. **Felipe Tobar**
* IJCAI 2018 A Model of Distributed Query Computation in Client-Server Scenarios on the Semantic Web. Olaf Hartig, Ian Letter, **Jorge Pérez**
* IJCAI 2018 LTL Realizability via Safety and Reachability Games. Alberto Camacho, Christian J. Muise, **Jorge A. Baier**, Sheila A. McIlraith
* IJCAI 2018 SynKit: LTL Synthesis as a Service. Alberto Camacho, Christian J. Muise, **Jorge A. Baier**, Sheila A. McIlraith
* NIPS 2017 Spectral Mixture Kernels for Multi-Output Gaussian Processes. Gabriel Parra, **Felipe Tobar**
* AAAI 2017 Grid Pathfinding on the 2k Neighborhoods. Nicolas Rivera, Carlos Hernández, **Jorge A. Baier**
* AAAI 2017 Non-Deterministic Planning with Temporally Extended Goals: LTL over Finite and Infinite Traces. Alberto Camacho, Eleni Triantafillou, Christian J. Muise, **Jorge A. Baier**, Sheila A. McIlraith
* IJCAI 2017 How a General-Purpose Commonsense Ontology can Improve Performance of Learning-Based Image Retrieval. Rodrigo Toro Icarte, **Jorge A. Baier**, Cristian Ruz, Alvaro Soto
* IJCAI 2017 Unified Representation and Lifted Sampling for Generative Models of Social Networks. Pablo Robles-Granda, Sebastián Moreno, Jennifer Neville
* IJCAI 2017 Online Bridged Pruning for Real-Time Search with Arbitrary Lookaheads. Carlos Hernández, Adi Botea, **Jorge A. Baier**, Vadim Bulitko
* AAAI 2016 Implicit Coordination in Crowded Multi-Agent Navigation. **Julio Erasmo Godoy**, Ioannis Karamouzas, Stephen J. Guy, Maria L. Gini
* AAAI 2016 Monte Carlo Tree Search for Multi-Robot Task Allocation. Bilal Kartal, Ernesto Nunes, **Julio Godoy**, Maria L. Gini
* IJCAI 2016 Incomplete Causal Laws in the Situation Calculus Using Free Fluents. Marcelo Arenas, **Jorge A. Baier**, Juan S. Navarro, Sebastian Sardiña
* IJCAI 2016 Moving in a Crowd: Safe and Efficient Navigation among Heterogeneous Agents. **Julio Godoy**, Ioannis Karamouzas, Stephen J. Guy, Maria L. Gini
* IJCAI 2016 Action Selection Methods for Multi-Agent Navigation in Crowded Environments. **Julio Godoy**
* NIPS 2015 Learning Stationary Time Series using Gaussian Processes with Nonparametric Kernels. **Felipe A. Tobar**, Thang D. Bui, Richard E. Turner
* AAAI 2015 Reusing Previously Found A* Paths for Fast Goal-Directed Navigation in Dynamic Terrain. Carlos Hernández, Roberto Asín, **Jorge A. Baier**
* AAAI 2015 RoboCup@Home - Benchmarking Domestic Service Robots. Sven Wachsmuth, Dirk Holz, Maja Rudinac, Javier Ruiz-del-Solar
* IJCAI 2015 Positive, Negative, or Neutral: Learning an Expanded Opinion Lexicon from Emoticon-Annotated Tweets. **Felipe Bravo-Marquez**, Eibe Frank, Bernhard Pfahringer
* IJCAI 2015 Bidirectional Constraints for Exchanging Data: Beyond Monotone Queries. Marcelo Arenas, Gabriel Diéguez, **Jorge Pérez**
* IJCAI 2015 Polynomial-Time Reformulations of LTL Temporally Extended Goals into Final-State Goals. Jorge Torres, **Jorge A. Baier**

## Code

The search for authors in Google Scholar is done using the [`get_author_dict_from_scholar`](blob/master/script.py#L8) script.
The search for publications for every author was done using the [`add_dblp_publications`](blob/master/script.py#L9) script. 
A summary of the results can be obtained by runing 
```
python script.py
```

