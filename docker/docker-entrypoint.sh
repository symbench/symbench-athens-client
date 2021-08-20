#!/bin/sh

. /opt/conda/etc/profile.d/conda.sh
conda activate base
conda activate symbench-athens-client-dev

if [ "$@" == "jupyter" ]; then
      jupyter lab --no-browser --notebook-dir /home/anaconda/data --NotebookApp.password='argon2:$argon2id$v=19$m=10240,t=10,p=8$vZQDFkQ5hPMqcjK2d1WKZA$Og5dVFCmw6IchwKNJMLaKg' --ip="0.0.0.0"
else
      $@
fi