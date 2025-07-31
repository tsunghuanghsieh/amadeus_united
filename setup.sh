#!/bin/zsh

ENV_NAME=amadeus

# source this file
conda create --name $ENV_NAME --clone base
conda activate $ENV_NAME
source ./secret.sh
