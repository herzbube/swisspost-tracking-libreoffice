#!/bin/bash

SCRIPT_NAME="$(basename "$0")"
SCRIPT_FOLDER="$(dirname "$0")"
case "$SCRIPT_FOLDER" in
  /*) BASE_FOLDER="$SCRIPT_FOLDER/.." ;;
  *) BASE_FOLDER="$(pwd)/$SCRIPT_FOLDER/.." ;;
esac
SRC_FOLDER="$BASE_FOLDER/src"
BUILD_FOLDER="$BASE_FOLDER/build"
EXTENSION_FILE_NAME="swisspost-tracking.oxt"
EXTENSION_FILE_PATH="$BUILD_FOLDER/$EXTENSION_FILE_NAME"

cd "$SRC_FOLDER"
if test $? -ne 0; then
  echo "Could not change directory to source folder: $SRC_FOLDER"
  exit 1
fi

if test -f "$EXTENSION_FILE_PATH"; then
  echo "Deleting previously built extension file ..."
  rm "$EXTENSION_FILE_PATH"
  if test $? -ne 0; then
    echo "Could not delete previously built extension file: $EXTENSION_FILE_PATH"
    exit 1
  fi
fi

if test ! -d "$BUILD_FOLDER"; then
  echo "Creating build folder ..."
  mkdir -p "$BUILD_FOLDER"
  if test $? -ne 0; then
    echo "Could not create build folder: $BUILD_FOLDER"
    exit 1
  fi
fi

echo "Building extension file ..."
zip -r "$EXTENSION_FILE_PATH" *
if test $? -ne 0; then
  echo "Could not create extension file: $EXTENSION_FILE_PATH"
  exit 1
fi

echo "Successfully built extension file: $EXTENSION_FILE_PATH"
