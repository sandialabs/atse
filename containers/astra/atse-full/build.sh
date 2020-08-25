#!/bin/bash

time docker build --squash --force-rm -t "atse.sandia.gov:3434/atse/astra:1.2.4" .
