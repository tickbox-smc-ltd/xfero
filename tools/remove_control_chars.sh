#!/bin/bash
for file in $(find /xfero/CENT1/src/xfero -type f); do
tr -d '\r' <$file >temp.$$ && mv temp.$$ $file
done
