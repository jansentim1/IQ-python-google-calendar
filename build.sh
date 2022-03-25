#! /bin/bash

# run from project root
NAME=gws-meets-matching
REGISTRY=worksuite
IMAGE=$REGISTRY/$NAME
HASH=$(git log -1 --pretty=%H)
TAG=${1:-latest} # first argument or latest

echo "THE HASH FOR THIS BUILD IS: $HASH"

docker build -t $IMAGE:$HASH -t $IMAGE:$TAG .
