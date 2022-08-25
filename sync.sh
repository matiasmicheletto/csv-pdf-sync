#!/bin/bash

cd datos                    # Moverse al directorio "datos"  
source venv/bin/activate    # Activar entorno virtual  
python3 analisis.py         # Correr script Python  
deactivate                  # Desactivar entorno virtual  
cp *.png *.tex ../articulo  # Copiar figuras y tablas generadas  
cd ../articulo              # Moverse al directorio del artículo LaTeX  
pdflatex main.tex           # Compilar documento pdf  
cp main.pdf ../articulo.pdf # Copiar al directorio principal  