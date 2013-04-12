fansiteSubmission
=================

Python wrapper for Tyrant Fansite deck simulation and submission

## Installation (Windows)

* Download and install Python 2.7 from http://www.python.org/download/
* Download the latest version of your favorite simulator
 * iteratedecks from http://www.hunterthinks.com/id/
 * Tyrant Optimize from http://www.hunterthinks.com/to/
* Download the fansiteSubmission source from https://nodeload.github.com/iteratedecks/fansiteSubmission/zip/master
* Put the fansiteSubmission folder inside of the correct folder, usually iteratedecks or tyrant_optimize

## Configuring fansiteSubmission for the first time

* Open a command prompt (Start -> Cmd)
* cd into your simulator's folder
* Call "fansiteSubmission-master\fansiteSims.py" (without the quotes)
* It will create a fansite_config.txt file inside of your simulator's folder
* Open fansite_config.txt (located in the simulator folder) and:
  * Edit the simulator paramter to match the simulator you will be using (e.g. "iteratedecks")
  * Add your simulator token (obtain token from the Fansite, your profile page, settings tab)

## Using fansiteSubmission

* Run fansiteSims.py again and it will automatically connect to the Fansite and start simulating decks
* To see available options for fansiteSubmission, use "fansiteSims.py -h" (without the quotes)
* Especially note the option "fansiteSims.py --runForever" to have the simulator run until you hit CTRL+C
