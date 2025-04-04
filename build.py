# -*- coding: utf-8 -*-
# build.py
# Script para criar o executável com PyInstaller incluindo fontes normais e itálicas
# Execute este script após instalar o PyInstaller com: pip install pyinstaller

import os
import PyInstaller.__main__
import shutil

# Cria pasta para fontes se não existir
if not os.path.exists('fonts'):
    os.makedirs('fonts')

# Lista de pares de fontes (normal e itálica) para copiar
fontes_para_copiar = [
    # Arial
    {
        "normal": "C:\\Windows\\Fonts\\arial.ttf", 
        "italica": "C:\\Windows\\Fonts\\ariali.ttf", 
        "destino_normal": "fonts\\arial.ttf", 
        "destino_italica": "fonts\\ariali.ttf"
    },
    # Times New Roman
    {
        "normal": "C:\\Windows\\Fonts\\times.ttf", 
        "italica": "C:\\Windows\\Fonts\\timesi.ttf", 
        "destino_normal": "fonts\\times.ttf", 
        "destino_italica": "fonts\\timesi.ttf"
    },
    # Calibri (para Windows mais recentes)
    {
        "normal": "C:\\Windows\\Fonts\\calibri.ttf", 
        "italica": "C:\\Windows\\Fonts\\calibrii.ttf", 
        "destino_normal": "fonts\\calibri.ttf", 
        "destino_italica": "fonts\\calibrii.ttf"
    },
    # Georgia
    {
        "normal": "C:\\Windows\\Fonts\\georgia.ttf", 
        "italica": "C:\\Windows\\Fonts\\georgiai.ttf", 
        "destino_normal": "fonts\\georgia.ttf", 
        "destino_italica": "fonts\\georgiai.ttf"
    },
    # Verdana
    {
        "normal": "C:\\Windows\\Fonts\\verdana.ttf", 
        "italica": "C:\\Windows\\Fonts\\verdanai.ttf", 
        "destino_normal": "fonts\\verdana.ttf", 
        "destino_italica": "fonts\\verdanai.ttf"
    }
]

# Contadores para estatísticas
fontes_normais_copiadas = 0
fontes_italicas_copiadas = 0

# Tentar copiar cada par de fontes
for fonte in fontes_para_copiar:
    # Tentar copiar a fonte normal
    if os.path.exists(fonte["normal"]):
        try:
            shutil.copy2(fonte["normal"], fonte["destino_normal"])
            print(f"Copiada a fonte normal: {fonte['normal']}")
            fontes_normais_copiadas += 1
        except Exception as e:
            print(f"Erro ao copiar fonte normal {fonte['normal']}: {str(e)}")
    
    # Tentar copiar a fonte itálica
    if os.path.exists(fonte["italica"]):
        try:
            shutil.copy2(fonte["italica"], fonte["destino_italica"])
            print(f"Copiada a fonte itálica: {fonte['italica']}")
            fontes_italicas_copiadas += 1
        except Exception as e:
            print(f"Erro ao copiar fonte itálica {fonte['italica']}: {str(e)}")

# Se nenhuma fonte foi copiada, tentar caminhos alternativos para fontes
if fontes_normais_copiadas == 0:
    # Caminhos alternativos para sistemas operacionais diferentes
    caminhos_alternativos = [
        "/System/Library/Fonts",  # macOS
        "/usr/share/fonts",        # Linux
        "C:/Windows/Fonts"         # Windows (caminho alternativo)
    ]
    
    for caminho in caminhos_alternativos:
        if os.path.exists(caminho):
            print(f"Tentando encontrar fontes em: {caminho}")
            # Listar arquivos na pasta de fontes
            try:
                arquivos_fontes = os.listdir(caminho)
                for arquivo in arquivos_fontes:
                    if arquivo.lower().endswith('.ttf'):
                        # Se for uma fonte TTF, verificar se é uma das que precisamos
                        nome_baixo = arquivo.lower()
                        if 'arial' in nome_baixo and not 'italic' in nome_baixo and not 'bold' in nome_baixo:
                            try:
                                shutil.copy2(os.path.join(caminho, arquivo), "fonts\\arial.ttf")
                                print(f"Copiada a fonte Arial alternativa: {arquivo}")
                                fontes_normais_copiadas += 1
                            except Exception:
                                pass
                        elif 'arial' in nome_baixo and ('italic' in nome_baixo or 'itali' in nome_baixo):
                            try:
                                shutil.copy2(os.path.join(caminho, arquivo), "fonts\\ariali.ttf")
                                print(f"Copiada a fonte Arial Itálica alternativa: {arquivo}")
                                fontes_italicas_copiadas += 1
                            except Exception:
                                pass
            except Exception as e:
                print(f"Erro ao listar diretório {caminho}: {str(e)}")

# Informar o resultado da cópia de fontes
print(f"\nFontes copiadas para a pasta 'fonts':")
print(f"- Fontes normais: {fontes_normais_copiadas}")
print(f"- Fontes itálicas: {fontes_italicas_copiadas}")

# Verificar se pelo menos uma fonte foi copiada para o funcionamento mínimo
if fontes_normais_copiadas == 0:
    print("\nAVISO: Nenhuma fonte normal foi encontrada. O executável usará fontes padrão do sistema.")
    
    # Criar um arquivo vazio para Arial para evitar erros
    try:
        with open("fonts\\arial.ttf", 'wb') as f:
            pass
        print("Criado um arquivo vazio para arial.ttf como fallback.")
    except Exception:
        print("Não foi possível criar arquivo de fallback.")

# Configuração do PyInstaller
print("\nIniciando a criação do executável...")
try:
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
    print("\nExecutável criado com sucesso!")
except Exception as e:
    print(f"\nErro ao criar o executável: {str(e)}")

print("\nProcesso concluído!")