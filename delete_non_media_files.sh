#!/bin/bash

# This script deletes all files that are not MP3, MP4, or WAV in the specified directory

if [ -z "$1" ]; then
  echo "Usage: $0 /path/to/directory"
  exit 1
fi

DIRECTORY=$1

# Find and delete files that are not MP3, MP4, or WAV
find "$DIRECTORY" -type f ! \( -iname "*.mp3" -o -iname "*.mp4" -o -iname "*.wav" \) -delete

echo "Deletion completed for files that are not MP3, MP4, or WAV in $DIRECTORY."
