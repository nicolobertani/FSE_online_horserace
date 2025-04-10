# Fast and Simple Adaptive Elicitations
## Software for Online Experiments

### Introduction

This repo contains the code to implement the Fast and Simple Elicitation method of [Bertani, Diecidue, Perny, and Viappiani (WP)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3569625).
More specifically, it provides Python code to run an online experiment with FSE and the competing methods described in Section 4.3 and in Online Appendix OA.E.
If you are interested in running these methods locally (e.g. for a laboratory experiment), please refer to [this different repo](https://github.com/nicolobertani/FSE), where you can find a more suitable implementation using just Python.


### Installation

After cloning/forking, and assuming you have Python installed, ensure that you have the required packages by running:

```bash
pip install -r requirements.txt
```


### Usage

Usage requires familiarity with otree.
In case you are new to otree, here is the link to the [project homepage](https://www.otree.org/).



### Personalization

Two modules can be modified to control and personalize the experiment.

The module [`binary_choices/config.py`](binary_choices/config.py) includes customizable variables to control the elicitation procedure to be used, as well as whether to show instructions and results of the random incentive scheme to the participants.

The module [`binary_choices/backend/shared_info.py`](binary_choices/backend/shared_info.py) conveniently gathers and defines several experimental details that the researcher might wish to alter. 
These include stimuli, participation fee, currency, and instructions. 
Changes to this file are automatically reflected in the experimental interface.


### Acknowledgments

The software was developed starting from a fork of [this implementation of binary choices](https://github.com/felixholzmeister/icl) by Felix Holzmeister, to whom I am gradeful for sharing his code.


### License

Copyright (C) 2023-present  Nicolò Bertani

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

This program is distributed in the hope that it will be useful, but without any warranty; without even the implied warranty of merchandability or fitness for a particular purpose.  See the GNU General Public License for more details.

For the GNU General Public License see <https://www.gnu.org/licenses/>. You should also find a [copy](LICENSE) of this license in this repository.

If you use this software, please cite the associated paper. You can find the [BibTeX citation](cite.bib) in this repository.