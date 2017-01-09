#!/usr/bin/env bash

set -x
pwd
jarfile=$1
cur="$(cd "`dirname "$0"`"; pwd)"
cd $cur
pwd
echo "jarfile: $jarfile"
echo "metaparentdir: $metaparentdir"
echo jar -uvf ../build/libs/$jarfile -C ../changemeta  META-INF
set +x