#!/bin/bash
clear
echo The ZIP - NO MACOSX Archiver

# Ask User for File Dir
read -p "Enter the File Directory to be zipped: " r1

# Change Directory to Specified Dir & List Current Dir
cd "$r1"

# Clear ._ files
dot_clean -m --keep=native $(pwd)
ls

# Ask User for ZIP File Name
read -p "Enter ZIP File Name: " r2 

# ZIP Folder
zip -r "$r1"\ "$r2".zip . -x ".DS_Store" -x "__MACOSX"

# Inform that ZIP Process has completed
echo Compiled and ZIP-ed as "$r2".zip