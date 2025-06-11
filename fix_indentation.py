# Script para corregir la indentación
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Reemplazamos las líneas problemáticas específicas
old_section = '''    for i, genero in enumerate(generos):
        if genero != 'Desconocido':
                         satisfaccion_gen = df[df['genero_cliente'] == genero]['calificación_satisfaccion'].dropna()
             
             color_rgb_genero = hex_to_rgb(colores_genero[i % len(colores_genero)])
             fig_violin_genero.add_trace(go.Violin('''

new_section = '''    for i, genero in enumerate(generos):
        if genero != 'Desconocido':
            satisfaccion_gen = df[df['genero_cliente'] == genero]['calificación_satisfaccion'].dropna()
            
            color_rgb_genero = hex_to_rgb(colores_genero[i % len(colores_genero)])
            fig_violin_genero.add_trace(go.Violin('''

content = content.replace(old_section, new_section)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('¡Archivo corregido exitosamente!') 