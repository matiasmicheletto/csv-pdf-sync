import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt


#### Inspección de los datos ####

# Cargar el dataset, traducir columnas y datos e imprimir resumen
data = pd.read_csv("insurance.csv")
data.rename(columns = {
    'age': 'Edad', 
    'sex': 'Sexo',
    'bmi': 'BMI',
    'smoker': 'Fumador',
    'region': 'Región',
    'children': 'Hijos',
    'charges': 'Costos'
    }, inplace = True)
data.replace({
    'Sexo': {
        'male': 'Masculino',
        'female': 'Femenino'
    }, 
    'Fumador': {
        'yes': 'Si',
        'no': 'No'
    },
    'Región': {
        'northeast': 'Noreste',
        'southeast': 'Sudeste',
        'southwest': 'Sudoeste',
        'northwest': 'Noroeste'
    }
}, inplace = True)
print(data.shape, end = '\n\n')
print(data.head(), end = '\n\n')
print(data.describe(), end = '\n\n')


#### Gráficos ####

# Configurar una fuente compatible con la de documentos latex
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'
mpl.rcParams['font.size'] = 12

# Gráfico 1: matriz de correlación
ax = sns.heatmap(data.corr(), annot = True, cmap = "YlGnBu", linewidths = .2)
plt.savefig("correlacion.png")
#plt.show()

# Gráfico 2: Distribucion de edades
plt.figure(figsize=(10, 5))
sns.histplot(data["Edad"], color = 'lightblue', stat = "density", linewidth = 0.5)
sns.kdeplot(data["Edad"], color = 'blue', linewidth = 2, shade = True)
plt.ylabel("Frecuencia")
plt.savefig("edades.png")
#plt.show()


#### Procesamiento de los datos ####

# Agrupar por rango etario en intervalos de 5 años, desde los 15 a los 70
bins = np.arange(15, 70, 5)
labels = [str(bins[i]) + "-" + str(bins[i+1]) for i in range(len(bins)-1)]
data['Grupo etario'] = pd.cut(data['Edad'], bins=bins, labels=labels, right=False)

# Calcular promedios
averages = data.groupby(['Grupo etario', 'Sexo', 'Fumador'])[['BMI', 'Costos']].mean()

# Mostrar tabla diferenciando sexo y condicion de fumador, una fila por grupo etario
bmidata = averages['BMI'].unstack().unstack()
chargesdata = averages['Costos'].unstack().unstack()

# Imprimir por consola
print(bmidata)
print(chargesdata)


#### Tablas ####

# Inprimir en formato LaTeX usando funcion de pandas
#print(bmidata.to_latex(caption="Promedios de BMI por edad, sexo y fumador", label="tab:bmi"))

# Usando una funcion personalizada
def to_latex(df, caption, label, filename):
    header = ('\\begin{table}[htb]\n' 
        '\t\\label{'+label+'} \n'
        '\t\\caption{'+caption+'} \n'
        '\t\\centering\n'        
        '\t\\begin{tabular}{ |c|c|c|c|c| } \n'
        '\t\t\\hline\n'
        '\t\t\\multirow{2}{*}{Edad} & \\multicolumn{2}{c|}{No fumador} & \\multicolumn{2}{c|}{Fumador} \\\\ \n'
        '\t\t\\cline{2-5} \n'
        '& Masculino & Femenino & Masculino & Femenino \\\\ \n'
        '\t\t\\hline\n')
    footer = ('\t\t\\hline \n'
        '\t\\end{tabular} \n'        
        '\\end{table} \n')
    content = ''
    for row in df.index:
        columndata = " & ".join([str(round(df.loc[row, col],2)) for col in df.columns])
        content = content + "\t\t" + row + " & " + columndata + " \\\\ \n"
    with open(filename, 'w') as latexfile:
        latexfile.write(header+content+footer)

to_latex(bmidata, "Promedios de BMI por edad, sexo y fumador", "tab:bmi", "bmi.tex")
to_latex(chargesdata, "Promedios de costos por edad, sexo y fumador", "tab:costos", "costos.tex")
