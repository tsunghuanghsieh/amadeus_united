#!/bin/zsh

ENV_NAME=amadeus

# source this file
conda deactivate
conda env remove -n $ENV_NAME
