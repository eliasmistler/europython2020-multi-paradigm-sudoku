# Multi-paradigm programming
Talk and code examples for EuroPython 2020, using Sudoku as an example.

## Synopsis
Python is a powerful multi-paradigm language which combines elements of object-orientation and functional programming. Both concepts can be really powerful if used right. But what if you use them together? It can be pragmatic and very efficient, but things can also get messy really quickly.

This talk explores peaceful co-existence of oo-classes and pure functions in the same code base. The focus is on identifying the right tool for the right job and bringing together the best of both. The main topics are:

* Code Structure
* Data Structures
* State Handling
* Multiple implementations

## Links
* [Talk in EuroPython schedule](https://ep2020.europython.eu/talks/83SnxW9-how-to-write-multi-paradigm-code/)
* [PDF Slides](./multi-paradigm%20slides.pdf)

## Run and explore

You can run all talk code, as well as the whole Sudoku solver implementation on Binder: 
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/eliasmistler/europython2020-multi-paradigm-sudoku/master)

Alternatively, install the required libraries and run locally (preferably inside a `virtualenv`):

```bash
pip install --upgrade -r requirements.txt
jupyter lab
```

## PDF Export

To run the presentation:
```bash
jupyter nbconvert --to slides multi-paradigm.ipynb --post serve
```

Then go to 
[http://127.0.0.1:8000/multi-paradigm.slides.html?print-pdf](http://127.0.0.1:8000/multi-paradigm.slides.html?print-pdf)
and print the site.
