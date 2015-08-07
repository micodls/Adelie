#!/bin/bash

echo \#!/bin/bash > ./sparco
echo python $PWD/sparco.py \$* >> ./sparco
chmod 777 sparco
