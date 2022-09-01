#!/bin/bash
clear
echo The ZIP - Remove MACOSX Tool
echo Make the ZIP file fully cross-compatible!

# Ask User for File Dir
read -p "Enter the File Directory with ZIP file for metadata removal: " r1

# Change Directory to Specified Dir & List Current Dir
cd "$r1"
ls

# Ask User for ZIP File Name
read -p "Enter ZIP File Name: " r2 

# Command to Remove MACOSX File
zip -d "$r2" ".DS_Store" "__MACOSX"

# Inform that ZIP Process has completed
echo The __MACOSX folder and the .DS_Store file has been removed from "$r2".