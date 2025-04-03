# build.py
# Script para criar o executável com PyInstaller sem exigir um ícone
# Execute este script após instalar o PyInstaller com: pip install pyinstaller

import os
import PyInstaller.__main__
import shutil

# Cria pasta para fontes se não existir
if not os.path.exists('fonts'):
    os.makedirs('fonts')

# Copia fontes Arial para a pasta (tenta vários caminhos possíveis)
fontes_possiveis = [
    "C:\\Windows\\Fonts\\arial.ttf",
    "C:\\Windows\\Fonts\\Arial.ttf"
]

for fonte in fontes_possiveis:
    if os.path.exists(fonte):
        shutil.copy2(fonte, "fonts\\arial.ttf")
        print(f"Copiada a fonte: {fonte}")
        break
else:
    print("AVISO: Fonte Arial não encontrada. O executável usará fontes padrão.")

# Configuração do PyInstaller
# Removido o parâmetro --icon que estava causando o erro
PyInstaller.__main__.run([
    'gerador_certificados.py',
    '--name=Gerador de Certificados',
    '--windowed',
    '--onefile',
    '--noconsole',
    '--add-data=fonts;fonts',  # Inclui a pasta de fontes
    '--clean',
    '--log-level=INFO'
])

print("Executável criado com sucesso!")