#!/bin/bash

#curl -L -O https://sourceware.org/pub/valgrind/valgrind-3.15.0.tar.bz2

# Checkout upstream on 20200315
git clone http://sourceware.org/git/valgrind.git
mv valgrind valgrind-20200315
tar -zcvf valgrind-20200315.tar.gz ./valgrind-20200315
