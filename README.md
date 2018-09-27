# Diverse folio isle

This branch is the start of a near total refactoring of the DFI framework to make it easier to write modules, and to facilitate the use of Redis for IPC. (and also to fix some wierdness left over from coding in the summer heat).

Stay tuned! :)

### Requirements

You need to install the [dfitools](https://github.com/peder2911/dfitools) package to use this application.

### Description

Diverse Folio Isle is a framework for doing text-mining.

There is a manual available here: [Read the docs](https://github.com/Peder2911/Diverse_Folio_Isle/wiki/Manual)

#### Usage

The program has a simple CLI that is accessed through Diverse_Folio_Isle.py. This script directs a three-step process where the user specifies a __sourcing__, a __preprocessing__ and  a __classification__ script. These scripts are as orthogonally modular as possible, some are even usable as standalone applications (like the [UFT pdf scraper](https://github.com/peder2911/Unlit_Ferment_Typified)).

Modularity is meant to facilitate scientific comparison of text-mining techniques. For more on this, see my [thesis](https://github.com/peder2911/thesis2018-2019).

