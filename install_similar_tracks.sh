#!/bin/bash
SCRIPT_NAME=`basename "$0"`
SCRIPT_PATH=${0%`basename "$0"`}/similar_tracks
PLUGIN_PATH="${HOME}/.local/share/rhythmbox/plugins/similar_tracks/"

#build the dirs
mkdir -p $PLUGIN_PATH

#copy the files
cp -r "${SCRIPT_PATH}"/* "$PLUGIN_PATH"
