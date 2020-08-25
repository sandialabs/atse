#!/bin/bash
llnlver=ldms-plugins-llnl-1.5
llnltar=${llnlver}.tar.gz
LLNLLUSTREURL=https://github.com/LLNL/ldms-plugins-llnl/releases/download/1.5/ldms-plugins-llnl-1.5.tar.gz
shasum="1900d539f6910d6f59deb45219fc2dd5f5f8efc977e3991729166902239f9811"
curl -L -O $LLNLLUSTREURL

