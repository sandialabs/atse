#!/bin/bash

git clone https://github.com/pwrapi/pwrapi-ref.git powerapi-20200529
cd powerapi-20200529
git checkout devel
cd ..
tar -zcvf powerapi-20200529.tar.gz ./powerapi-20200529
