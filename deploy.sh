#!/usr/bin/env bash

# Enable API mode config in index.html
sed -i 's/\(src="js\/\)conf-[a-z]*.js/\1conf-api.js/g' missal1962/static/index.html