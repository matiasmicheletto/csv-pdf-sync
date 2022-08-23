#!/bin/bash

cd datos
source venv/bin/activate
python3 analisis.py 
deactivate
cp *.png *.tex ../articulo
cd ../articulo
pdflatex main.tex