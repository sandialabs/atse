#!/bin/bash

OUTPUT="$(tx2mon -q -t -d .0001 -f /dev/stdout)"

echo $OUTPUT | awk -F, '{CPU[0]=$148;MEM[0]=$204;CPU[1]=$221;MEM[1]=$277};END{print CPU[0], CPU[1], MEM[0], MEM[1]}'
