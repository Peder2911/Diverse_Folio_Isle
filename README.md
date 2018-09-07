# Diverse folio isle

### Description

[Read the docs](https://github.com/Peder2911/Diverse_Folio_Isle/wiki/Manual)

Diverse Folio Isle is a framework for doing text-mining using the Montanus scraper,
or other data sources (currently supports csv-files and sqlite .db-files).

The program has a simple CLI that is accessed through the deScry.py script.

I also need to do some _major_ refactoring, but this has been, and is being developed in “production”, and will thus remain a bit messy until i have some headroom.

### You need two things for the system to work:

_Batteries are not included_

1. A keys.json file must be added to the Montanus-module, containing your API
   keys for the different APIs. The path for this file is:
   ./modules/Montanus/configFiles/keys.json
2. Vectorization (.bin) and classification (.rds) models are currently not included.
   You could either train your own models using sent2vec and R, or send me an email @
   pglandsverk@gmail.com.
   The paths in which to put your models are:
   ./resources/models/classifiers (for .rds classifiers)
   ./resources/models/embedders (for sent2vec .bin-files)

Please don't hesitate to contact me if you have any questions about the project.

Peder Landsverk @ PRIO 2018