import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os
import zipfile
from datetime import datetime
import sys
import hashlib
import json
import re
import uuid
import webbrowser

class GeradorCertificados:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Certificados")
        self.root.geometry("800x730")  # Aumentada a altura para acomodar o rodapé
        self.root.resizable(False, False)
        
        # Dicionário de cores para uso no certificado
        self.cores = {
            "Preto": "black",
            "Azul Escuro": "#000080",
            "Verde Escuro": "#006400",
            "Verde Claro": "#2E8B57",
            "Branco": "white"
        }
        
        # Lista de fontes disponíveis para seleção
        self.fontes_disponiveis = [
            "Arial",
            "Times New Roman",
            "Calibri",
            "Georgia",
            "Verdana"
        ]
        
        # Mapeamento de nomes de fontes para arquivos de fonte
        self.mapeamento_fontes = {
            "Arial": "arial.ttf",
            "Times New Roman": "times.ttf",
            "Calibri": "calibri.ttf",
            "Georgia": "georgia.ttf",
            "Verdana": "verdana.ttf"
        }
        
        # Mapeamento de nomes de fontes para arquivos de fonte itálica
        self.mapeamento_fontes_italicas = {
            "Arial": "ariali.ttf",
            "Times New Roman": "timesi.ttf",
            "Calibri": "calibrii.ttf",
            "Georgia": "georgiai.ttf",
            "Verdana": "verdanai.ttf"
        }
        
        # Configuração para ícone do aplicativo quando for executável
        try:
            if getattr(sys, 'frozen', False):
                application_path = sys._MEIPASS
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))
                
            # Definir ícone se existir
            icone_path = os.path.join(application_path, "icone.ico")
            if os.path.exists(icone_path):
                self.root.iconbitmap(icone_path)
        except Exception:
            pass  # Ignora erros de ícone
        
        # Variáveis para armazenar caminhos de arquivos
        self.imagem_fundo_path = None
        self.csv_path = None
        
        # Criar pasta de saída
        self.output_dir = self.get_output_dir()
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Criar pasta de banco de dados de certificados
        self.db_dir = os.path.join(self.output_dir, "db")
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)
        
        # Criar ou carregar o arquivo de banco de dados de certificados
        self.db_path = os.path.join(self.db_dir, "certificados.json")
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=4)
        
        # Carregar certificados existentes
        self.certificados_db = self.carregar_banco_dados()
        
        # Frame principal
        frame_principal = ttk.Frame(root, padding=20)
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Estilo
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 11))
        style.configure("TButton", font=("Arial", 11))
        style.configure("TEntry", font=("Arial", 11))
        style.configure("Link.TLabel", font=("Arial", 10, "underline"), foreground="blue")
        
        # Título da aplicação
        titulo_app = ttk.Label(frame_principal, text="Gerador de Certificados", font=("Arial", 16, "bold"))
        titulo_app.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Notebook para separar geração e validação
        self.notebook = ttk.Notebook(frame_principal)
        self.notebook.grid(row=1, column=0, columnspan=3, sticky="nsew")
        
        # Tab de geração
        self.tab_geracao = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_geracao, text="Gerar Certificados")
        
        # Tab de validação
        self.tab_validacao = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_validacao, text="Validar Certificado")
        
        # ========================== CONTEÚDO DA TAB DE GERAÇÃO ==========================
        
        # Imagem de fundo
        ttk.Label(self.tab_geracao, text="Imagem de Fundo:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.label_imagem_fundo = ttk.Label(self.tab_geracao, text="Nenhum arquivo selecionado")
        self.label_imagem_fundo.grid(row=0, column=1, sticky=tk.W, pady=5)
        ttk.Button(self.tab_geracao, text="Selecionar", command=self.selecionar_imagem_fundo).grid(row=0, column=2, pady=5, padx=5)
        
        # Texto principal
        ttk.Label(self.tab_geracao, text="Texto Principal:").grid(row=1, column=0, sticky=tk.W + tk.N, pady=5)
        self.texto_principal = tk.Text(self.tab_geracao, width=50, height=5)
        self.texto_principal.grid(row=1, column=1, columnspan=2, sticky=tk.W, pady=5)
        ttk.Label(self.tab_geracao, text="Nota: O nome do participante aparecerá automaticamente acima deste texto.", 
                font=("Arial", 9, "italic")).grid(row=2, column=1, columnspan=2, sticky=tk.W)
        
        # Carga horária
        ttk.Label(self.tab_geracao, text="Carga Horária:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.carga_horaria = tk.StringVar()
        ttk.Entry(self.tab_geracao, textvariable=self.carga_horaria, width=40).grid(row=3, column=1, columnspan=2, sticky=tk.W, pady=5)
        
        # Seleção de cor da fonte
        ttk.Label(self.tab_geracao, text="Cor da Fonte:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.cor_fonte = tk.StringVar(value="Preto")
        ttk.Combobox(self.tab_geracao, 
                     textvariable=self.cor_fonte, 
                     values=list(self.cores.keys()),
                     state="readonly",
                     width=15).grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Seleção de estilo de fonte
        ttk.Label(self.tab_geracao, text="Estilo de Fonte:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.estilo_fonte = tk.StringVar(value="Arial")
        ttk.Combobox(self.tab_geracao, 
                     textvariable=self.estilo_fonte, 
                     values=self.fontes_disponiveis,
                     state="readonly",
                     width=15).grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # Espaçamento entre linhas
        ttk.Label(self.tab_geracao, text="Espaçamento entre Linhas:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.espacamento_linhas = tk.DoubleVar(value=1.5)
        valores_espacamento = [1.0, 1.15, 1.5, 2.0, 2.5]
        ttk.Combobox(self.tab_geracao, 
                     textvariable=self.espacamento_linhas, 
                     values=valores_espacamento,
                     state="readonly",
                     width=15).grid(row=6, column=1, sticky=tk.W, pady=5)
        
        # Data de emissão
        ttk.Label(self.tab_geracao, text="Data de Emissão:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.data_emissao = tk.StringVar()
        self.data_emissao.set(self.obter_data_atual())
        ttk.Entry(self.tab_geracao, textvariable=self.data_emissao, width=40).grid(row=7, column=1, columnspan=2, sticky=tk.W, pady=5)
        ttk.Label(self.tab_geracao, text="Formato: Cidade-UF, dia de mês de ano (ex: Macapá-AP, 01 de abril de 2025)", 
                 font=("Arial", 9, "italic")).grid(row=8, column=1, columnspan=2, sticky=tk.W)
        
        # Arquivo CSV
        ttk.Label(self.tab_geracao, text="Arquivo CSV:").grid(row=9, column=0, sticky=tk.W, pady=5)
        self.label_csv = ttk.Label(self.tab_geracao, text="Nenhum arquivo selecionado")
        self.label_csv.grid(row=9, column=1, sticky=tk.W, pady=5)
        ttk.Button(self.tab_geracao, text="Selecionar", command=self.selecionar_csv).grid(row=9, column=2, pady=5, padx=5)
        
        # Frame para botões de ação
        frame_botoes = ttk.Frame(self.tab_geracao)
        frame_botoes.grid(row=10, column=0, columnspan=3, pady=20)
        
        # Botão para gerar certificados
        self.botao_gerar = ttk.Button(frame_botoes, text="Gerar Certificados", command=self.gerar_certificados)
        self.botao_gerar.pack(side=tk.LEFT, padx=10)
        
        # Botão para baixar certificados
        self.botao_baixar = ttk.Button(frame_botoes, text="Baixar Certificados", command=self.baixar_certificados)
        self.botao_baixar.pack(side=tk.LEFT, padx=10)
        self.botao_baixar.config(state=tk.DISABLED)
        
        # Status de progresso
        self.frame_progresso = ttk.Frame(self.tab_geracao)
        self.frame_progresso.grid(row=11, column=0, columnspan=3, pady=10, sticky=tk.W+tk.E)
        
        self.label_status = ttk.Label(self.frame_progresso, text="")
        self.label_status.pack()
        
        self.barra_progresso = ttk.Progressbar(self.frame_progresso)
        self.barra_progresso.pack(fill=tk.X, pady=5)
        
        # ========================== CONTEÚDO DA TAB DE VALIDAÇÃO ==========================
        
        # Frame central para validação
        self.frame_validacao = ttk.Frame(self.tab_validacao, padding=20)
        self.frame_validacao.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(self.frame_validacao, text="Validação de Certificados", 
                 font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Instruções
        ttk.Label(self.frame_validacao, text="Insira o código de autenticação do certificado:").grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Entrada do código
        self.codigo_validacao = tk.StringVar()
        self.entrada_codigo = ttk.Entry(self.frame_validacao, textvariable=self.codigo_validacao, width=40)
        self.entrada_codigo.grid(row=2, column=0, sticky=tk.W+tk.E, padx=(0, 10))
        
        # Botão de validação
        self.botao_validar = ttk.Button(self.frame_validacao, text="Validar", command=self.validar_certificado)
        self.botao_validar.grid(row=2, column=1, sticky=tk.W)
        
        # Resultado da validação
        self.frame_resultado = ttk.LabelFrame(self.frame_validacao, text="Resultado", padding=10)
        self.frame_resultado.grid(row=3, column=0, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S, pady=20)
        
        # Mensagem de status
        self.label_status_validacao = ttk.Label(self.frame_resultado, text="")
        self.label_status_validacao.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        # Detalhes do certificado (se for válido)
        self.frame_detalhes = ttk.Frame(self.frame_resultado)
        self.frame_detalhes.grid(row=1, column=0, sticky=tk.W+tk.E, pady=5)
        
        # Inicialmente oculto
        self.frame_detalhes.grid_remove()
        
        # Detalhes específicos
        self.label_nome = ttk.Label(self.frame_detalhes, text="")
        self.label_nome.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.label_data = ttk.Label(self.frame_detalhes, text="")
        self.label_data.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.label_carga = ttk.Label(self.frame_detalhes, text="")
        self.label_carga.grid(row=2, column=0, sticky=tk.W, pady=2)
        
        # ========================== RODAPÉ COM LINK PARA LINKEDIN ==========================
        
        # Separador
        ttk.Separator(frame_principal, orient='horizontal').grid(row=2, column=0, columnspan=3, sticky=tk.E+tk.W, pady=10)
        
        # Frame para o rodapé
        frame_rodape = ttk.Frame(frame_principal)
        frame_rodape.grid(row=3, column=0, columnspan=3, sticky=tk.E+tk.W)
        
        # Label com link para o LinkedIn
        self.label_linkedin = ttk.Label(frame_rodape, text="AMPereira", style="Link.TLabel", cursor="hand2")
        self.label_linkedin.pack(side=tk.RIGHT, padx=5)
        self.label_linkedin.bind("<Button-1>", lambda e: self.abrir_linkedin())
        
        # Label de copyright
        ttk.Label(frame_rodape, text="© 2025 Gerador de Certificados - Desenvolvido por ").pack(side=tk.RIGHT)
        
        # Caminho do arquivo zip
        self.zip_file_path = None
    
    def abrir_linkedin(self):
        """Abre o perfil do LinkedIn do desenvolvedor"""
        webbrowser.open("https://www.linkedin.com/in/antoniomarcos-pereira/")
    
    def get_output_dir(self):
        """Retorna o diretório de saída dependendo se é executável ou script"""
        try:
            if getattr(sys, 'frozen', False):
                # Se for executável, usa a pasta de documentos do usuário
                import ctypes.wintypes
                CSIDL_PERSONAL = 5  # Documentos
                SHGFP_TYPE_CURRENT = 0
                buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
                ctypes.windll.shell32.SHGetFolderPathW(0, CSIDL_PERSONAL, 0, SHGFP_TYPE_CURRENT, buf)
                return os.path.join(buf.value, "GeradorCertificados")
            else:
                # Se for script, usa a pasta local
                return os.path.join(os.path.dirname(os.path.abspath(__file__)), "certificados_gerados")
        except Exception:
            # Fallback para pasta local
            return os.path.join(os.path.dirname(os.path.abspath(__file__)), "certificados_gerados")
    
    def carregar_banco_dados(self):
        """Carrega o banco de dados de certificados"""
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar banco de dados: {str(e)}")
            return {}
    
    def salvar_banco_dados(self):
        """Salva o banco de dados de certificados"""
        try:
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(self.certificados_db, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Erro ao salvar banco de dados: {str(e)}")
    
    def gerar_codigo_autenticacao(self, nome_participante, data_emissao):
        """Gera um código único para autenticação do certificado"""
        # Criar um identificador único
        id_unico = str(uuid.uuid4())
        
        # Criar uma string com os dados do certificado
        dados = f"{nome_participante}|{data_emissao}|{id_unico}"
        
        # Gerar um hash SHA-256 dos dados
        hash_obj = hashlib.sha256(dados.encode('utf-8'))
        hash_completo = hash_obj.hexdigest()
        
        # Usar os primeiros 12 caracteres do hash para criar um código mais curto
        codigo_curto = hash_completo[:12].upper()
        
        # Formatar o código em grupos para facilitar a leitura e digitação
        codigo_formatado = f"{codigo_curto[:4]}-{codigo_curto[4:8]}-{codigo_curto[8:12]}"
        
        return codigo_formatado, id_unico
    
    def obter_data_atual(self):
        """Retorna a data atual formatada como 'Cidade-UF, dia de mês de ano'"""
        meses = {
            1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril",
            5: "maio", 6: "junho", 7: "julho", 8: "agosto",
            9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro"
        }
        hoje = datetime.now()
        return f"Macapá-AP, {hoje.day:02d} de {meses[hoje.month]} de {hoje.year}"
    
    def selecionar_imagem_fundo(self):
        """Seleciona a imagem de fundo do certificado"""
        arquivo = filedialog.askopenfilename(
            title="Selecione a imagem de fundo",
            filetypes=[("Arquivos PNG", "*.png"), ("Todos os arquivos", "*.*")]
        )
        if arquivo:
            self.imagem_fundo_path = arquivo
            self.label_imagem_fundo.config(text=os.path.basename(arquivo))
    
    def selecionar_csv(self):
        """Seleciona o arquivo CSV com os nomes dos participantes"""
        arquivo = filedialog.askopenfilename(
            title="Selecione o arquivo CSV",
            filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")]
        )
        if arquivo:
            self.csv_path = arquivo
            self.label_csv.config(text=os.path.basename(arquivo))
    
    def validar_certificado(self):
        """Valida um certificado com base no código de autenticação"""
        # Limpar resultados anteriores
        self.label_status_validacao.config(text="")
        self.frame_detalhes.grid_remove()
        self.label_nome.config(text="")
        self.label_data.config(text="")
        self.label_carga.config(text="")
        
        # Obter o código de validação
        codigo = self.codigo_validacao.get().strip()
        
        # Validar formato do código
        if not re.match(r"^[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$", codigo):
            self.label_status_validacao.config(
                text="Código inválido. O formato correto é XXXX-XXXX-XXXX.",
                foreground="red"
            )
            return
        
        # Procurar o código no banco de dados
        certificado = self.certificados_db.get(codigo)
        
        if certificado:
            # Certificado encontrado
            self.label_status_validacao.config(
                text="✓ CERTIFICADO VÁLIDO",
                foreground="green",
                font=("Arial", 12, "bold")
            )
            
            # Mostrar detalhes
            self.label_nome.config(text=f"Nome: {certificado['nome']}")
            self.label_data.config(text=f"Data de emissão: {certificado['data_emissao']}")
            
            if certificado.get('carga_horaria'):
                self.label_carga.config(text=f"Carga horária: {certificado['carga_horaria']}")
            else:
                self.label_carga.config(text="")
            
            # Mostrar frame de detalhes
            self.frame_detalhes.grid()
        else:
            # Certificado não encontrado
            self.label_status_validacao.config(
                text="✗ CERTIFICADO NÃO RECONHECIDO",
                foreground="red",
                font=("Arial", 12, "bold")
            )
    
    def gerar_certificados(self):
        """Gera os certificados para cada participante"""
        # Verificar campos obrigatórios
        if not self.imagem_fundo_path:
            messagebox.showerror("Erro", "Selecione uma imagem de fundo para o certificado.")
            return
        
        if not self.texto_principal.get("1.0", tk.END).strip():
            messagebox.showerror("Erro", "Preencha o texto principal do certificado.")
            return
        
        if not self.csv_path:
            messagebox.showerror("Erro", "Selecione o arquivo CSV com os nomes dos participantes.")
            return
        
        # Desabilitar botões durante o processamento
        self.botao_gerar.config(state=tk.DISABLED)
        self.botao_baixar.config(state=tk.DISABLED)
        self.label_status.config(text="Gerando certificados...")
        self.root.update()
        
        try:
            # Limpar a pasta de saída
            for file in os.listdir(self.output_dir):
                file_path = os.path.join(self.output_dir, file)
                if os.path.isfile(file_path) and file.endswith(".pdf"):
                    try:
                        os.unlink(file_path)
                    except Exception:
                        pass
            
            # Carregar dados do CSV
            try:
                df = pd.read_csv(self.csv_path, encoding='utf-8')
            except UnicodeDecodeError:
                # Tentar outros encodings se utf-8 falhar
                try:
                    df = pd.read_csv(self.csv_path, encoding='latin1')
                except UnicodeDecodeError:
                    df = pd.read_csv(self.csv_path, encoding='ISO-8859-1')
            
            # Verificar se existe a coluna de nomes
            if 'nome' not in df.columns and 'Nome' not in df.columns:
                messagebox.showerror("Erro", "O arquivo CSV deve conter uma coluna 'nome' ou 'Nome'.")
                self.botao_gerar.config(state=tk.NORMAL)
                self.label_status.config(text="")
                return
            
            # Usar a coluna de nome, independente de ser 'nome' ou 'Nome'
            nome_coluna = 'nome' if 'nome' in df.columns else 'Nome'
            
            # Configuração da barra de progresso
            total_participantes = len(df)
            self.barra_progresso["maximum"] = total_participantes
            
            # Lista para armazenar caminhos dos certificados gerados
            certificados_gerados = []
            
            # Obter o texto principal original
            texto_original = self.texto_principal.get("1.0", tk.END).strip()
            
            # Data de emissão para todos os certificados
            data_emissao = self.data_emissao.get()
            
            # Carga horária
            carga_horaria = self.carga_horaria.get()
            
            # Gerar certificados para cada participante
            for idx, row in df.iterrows():
                nome_participante = str(row[nome_coluna]).strip()
                
                # Atualizar status
                self.label_status.config(text=f"Gerando certificado para: {nome_participante}")
                self.barra_progresso["value"] = idx + 1
                self.root.update()
                
                # Gerar código de autenticação
                codigo_autenticacao, id_unico = self.gerar_codigo_autenticacao(nome_participante, data_emissao)
                
                # Armazenar informações do certificado no banco de dados
                self.certificados_db[codigo_autenticacao] = {
                    "id": id_unico,
                    "nome": nome_participante,
                    "data_emissao": data_emissao,
                    "carga_horaria": carga_horaria,
                    "data_geracao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # O texto_completo agora não precisa incluir o nome do participante
                # pois ele será exibido separadamente
                texto_completo = texto_original
                
                # Gerar certificado
                certificado_path = self.criar_certificado(nome_participante, texto_completo, codigo_autenticacao)
                certificados_gerados.append(certificado_path)
            
            # Salvar o banco de dados atualizado
            self.salvar_banco_dados()
            
            # Criar arquivo ZIP com os certificados
            self.label_status.config(text="Compactando certificados...")
            self.root.update()
            
            # Nome do arquivo ZIP baseado na data e hora atual
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.zip_file_path = os.path.join(self.output_dir, f"certificados_{timestamp}.zip")
            
            with zipfile.ZipFile(self.zip_file_path, 'w') as zipf:
                for certificado in certificados_gerados:
                    zipf.write(certificado, os.path.basename(certificado))
            
            # Atualizar interface
            self.label_status.config(text=f"Certificados gerados com sucesso: {total_participantes} certificados")
            self.botao_gerar.config(state=tk.NORMAL)
            self.botao_baixar.config(state=tk.NORMAL)
            
            messagebox.showinfo("Sucesso", f"{total_participantes} certificados foram gerados com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao gerar os certificados: {str(e)}")
            self.label_status.config(text="Erro ao gerar certificados")
            self.botao_gerar.config(state=tk.NORMAL)
    
    def aplicar_italico(self, imagem, texto, fonte, posicao, cor, skew_factor=0.15):
        """
        Renderiza texto em estilo itálico usando transformação de imagem
        
        Args:
            imagem: Imagem PIL
            texto: Texto a ser renderizado
            fonte: Objeto de fonte PIL
            posicao: Tupla (x, y) para posicionamento
            cor: Cor do texto
            skew_factor: Fator de inclinação (0.1-0.2 para itálico sutil)
        """
        try:
            # Tentar obter dimensões do texto usando getbbox (Pillow recente)
            try:
                texto_tamanho = fonte.getbbox(texto)
                largura_texto = texto_tamanho[2] - texto_tamanho[0]
                altura_texto = texto_tamanho[3] - texto_tamanho[1]
            except AttributeError:
                # Fallback para versões mais antigas do Pillow
                largura_texto, altura_texto = self.get_text_dimensions(texto, fonte)
            
            # Adicionar espaço para a transformação
            largura_extra = int(altura_texto * skew_factor)
            
            # Criar imagem para o texto com fundo transparente
            texto_img = Image.new('RGBA', (largura_texto + largura_extra, altura_texto), (0, 0, 0, 0))
            texto_draw = ImageDraw.Draw(texto_img)
            
            # Desenhar o texto na imagem temporária
            texto_draw.text((0, 0), texto, font=fonte, fill=cor)
            
            # Aplicar transformação para criar o efeito itálico
            matriz = [1, 0, skew_factor, 0, 1, 0]
            texto_italico = texto_img.transform(
                texto_img.size, 
                Image.AFFINE, 
                matriz,
                Image.BICUBIC
            )
            
            # Colar a imagem transformada na imagem principal
            if imagem.mode == 'RGBA':
                imagem.paste(texto_italico, posicao, texto_italico)
            else:
                # Converter para RGBA temporariamente se necessário
                imagem_temp = imagem.convert('RGBA')
                imagem_temp.paste(texto_italico, posicao, texto_italico)
                imagem = imagem_temp.convert(imagem.mode)
            
            return imagem
        except Exception as e:
            # Em caso de erro, usar o método padrão de desenho de texto
            print(f"Erro ao aplicar itálico: {str(e)}")
            draw = ImageDraw.Draw(imagem)
            draw.text(posicao, texto, font=fonte, fill=cor)
            return imagem

    def desenhar_texto_centralizado(self, draw, texto, fonte, x_inicio, y_inicio, largura_max, cor, espacamento, italico=False):
        """
        Desenha o texto centralizado na imagem com espaçamento controlado entre linhas
        
        Args:
            draw: Objeto ImageDraw
            texto: Texto a ser renderizado
            fonte: Objeto de fonte PIL
            x_inicio: Posição X inicial (margem esquerda)
            y_inicio: Posição Y inicial (topo)
            largura_max: Largura máxima do texto
            cor: Cor do texto
            espacamento: Fator de espaçamento entre linhas
            italico: Se True, aplica transformação para simular itálico
        """
        # Altura da linha com espaçamento personalizado
        altura_linha = self.get_text_dimensions("Tg", fonte)[1] * espacamento
        
        # Dividir o texto em parágrafos
        paragrafos = texto.split('\n')
        y_atual = y_inicio
        
        for paragrafo in paragrafos:
            if not paragrafo.strip():
                # Pular linhas vazias
                y_atual += altura_linha
                continue
            
            # Dividir o parágrafo em palavras
            palavras = paragrafo.split()
            linha_atual = []
            largura_atual = 0
            espaco_normal = self.get_text_dimensions(" ", fonte)[0]
            
            for palavra in palavras:
                largura_palavra = self.get_text_dimensions(palavra, fonte)[0]
                
                # Verificar se adicionar esta palavra excederia a largura máxima
                if linha_atual and largura_atual + espaco_normal + largura_palavra > largura_max:
                    # Desenhar a linha atual centralizada
                    texto_linha = " ".join(linha_atual)
                    largura_texto = self.get_text_dimensions(texto_linha, fonte)[0]
                    x_centralizado = x_inicio + (largura_max - largura_texto) / 2
                    
                    if italico:
                        # Aplica a transformação itálica
                        self.aplicar_italico(draw.im, texto_linha, fonte, (int(x_centralizado), int(y_atual)), cor)
                    else:
                        # Desenho normal
                        draw.text((x_centralizado, y_atual), texto_linha, font=fonte, fill=cor)
                    
                    # Avançar para a próxima linha
                    y_atual += altura_linha
                    linha_atual = [palavra]
                    largura_atual = largura_palavra
                else:
                    # Adicionar a palavra à linha atual
                    if linha_atual:  # Se não for a primeira palavra da linha
                        largura_atual += espaco_normal
                    linha_atual.append(palavra)
                    largura_atual += largura_palavra
            
            # Processar a última linha do parágrafo (também centralizada)
            if linha_atual:
                texto_linha = " ".join(linha_atual)
                largura_texto = self.get_text_dimensions(texto_linha, fonte)[0]
                x_centralizado = x_inicio + (largura_max - largura_texto) / 2
                
                if italico:
                    # Aplica a transformação itálica
                    self.aplicar_italico(draw.im, texto_linha, fonte, (int(x_centralizado), int(y_atual)), cor)
                else:
                    # Desenho normal
                    draw.text((x_centralizado, y_atual), texto_linha, font=fonte, fill=cor)
                
                y_atual += altura_linha
        
        return y_atual

    def desenhar_texto_justificado(self, draw, texto, fonte, x_inicio, y_inicio, largura_max, cor, espacamento):
        """Desenha o texto justificado na imagem com espaçamento controlado entre palavras"""
        # Parâmetros para controle de espaçamento
        espaco_normal = self.get_text_dimensions(" ", fonte)[0]  # Largura do espaço normal
        espaco_maximo = espaco_normal * 2.5  # Limitar o espaçamento máximo entre palavras
        min_palavras_justificar = 3  # Mínimo de palavras para justificar uma linha
        
        # Determinar a largura média dos caracteres para cálculo de quebra de linha
        char_width_avg = self.get_text_dimensions("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", fonte)[0] / 52
        chars_per_line = int(largura_max / char_width_avg) - 2  # Margem de segurança
        
        # Altura da linha com espaçamento personalizado
        altura_linha = self.get_text_dimensions("Tg", fonte)[1] * espacamento
        
        # Dividir o texto em parágrafos
        paragrafos = texto.split('\n')
        y_atual = y_inicio
        
        for paragrafo in paragrafos:
            if not paragrafo.strip():
                # Pular linhas vazias
                y_atual += altura_linha
                continue
            
            # Dividir o parágrafo em palavras
            palavras = paragrafo.split()
            linha_atual = []
            largura_atual = 0
            
            for palavra in palavras:
                largura_palavra = self.get_text_dimensions(palavra, fonte)[0]
                
                # Verificar se adicionar esta palavra excederia a largura máxima
                if linha_atual and largura_atual + espaco_normal + largura_palavra > largura_max:
                    # Verificar se há palavras suficientes para justificar
                    if len(linha_atual) >= min_palavras_justificar:
                        # Calcular o espaço extra total
                        espaco_extra = largura_max - largura_atual
                        espacos_entre_palavras = len(linha_atual) - 1
                        
                        # Calcular o espaço entre palavras, com limite máximo
                        if espacos_entre_palavras > 0:
                            espaco_entre = min(espaco_normal + espaco_extra / espacos_entre_palavras, espaco_maximo)
                        else:
                            espaco_entre = espaco_normal
                        
                        # Desenhar as palavras da linha justificada
                        x_atual = x_inicio
                        for i, p in enumerate(linha_atual):
                            draw.text((x_atual, y_atual), p, font=fonte, fill=cor)
                            x_atual += self.get_text_dimensions(p, fonte)[0]
                            
                            # Adicionar espaço após cada palavra exceto a última
                            if i < len(linha_atual) - 1:
                                x_atual += espaco_entre
                    else:
                        # Alinhar à esquerda se houver poucas palavras
                        x_atual = x_inicio
                        for i, p in enumerate(linha_atual):
                            draw.text((x_atual, y_atual), p, font=fonte, fill=cor)
                            x_atual += self.get_text_dimensions(p, fonte)[0] + espaco_normal
                    
                    # Avançar para a próxima linha
                    y_atual += altura_linha
                    linha_atual = [palavra]
                    largura_atual = largura_palavra
                else:
                    # Adicionar a palavra à linha atual
                    if linha_atual:  # Se não for a primeira palavra da linha
                        largura_atual += espaco_normal
                    linha_atual.append(palavra)
                    largura_atual += largura_palavra
            
            # Processar a última linha do parágrafo (sempre alinhada à esquerda)
            if linha_atual:
                x_atual = x_inicio
                for p in linha_atual:
                    draw.text((x_atual, y_atual), p, font=fonte, fill=cor)
                    x_atual += self.get_text_dimensions(p, fonte)[0] + espaco_normal
                
                y_atual += altura_linha
        
        return y_atual

    def get_text_dimensions(self, text, font):
        """Obtém as dimensões do texto de forma compatível com diferentes versões do Pillow"""
        try:
            # Método mais recente: usar textbbox
            left, top, right, bottom = font.getbbox(text)
            return right - left, bottom - top
        except AttributeError:
            try:
                # Método intermediário: usar getsize
                return font.getsize(text)
            except AttributeError:
                try:
                    # Método antigo: usar textsize do ImageDraw
                    from PIL import ImageDraw
                    dummy_draw = ImageDraw.Draw(Image.new('RGB', (1, 1)))
                    return dummy_draw.textsize(text, font=font)
                except Exception:
                    # Método de fallback: estimativa básica baseada no tamanho da fonte
                    return len(text) * font.size // 2, font.size

    def criar_certificado(self, nome_participante, texto_completo, codigo_autenticacao):
        """Cria um certificado individual para um participante"""
        # Carregar a imagem de fundo
        imagem_fundo = Image.open(self.imagem_fundo_path)
        
        # Redimensionar para tamanho A4 PAISAGEM (297mm x 210mm)
        # Converter mm para pixels (assumindo 300 DPI)
        width_px = int(297 * 300 / 25.4)  # 3508 pixels
        height_px = int(210 * 300 / 25.4)  # 2480 pixels
        
        # Redimensionar a imagem de fundo para o tamanho A4 paisagem
        imagem_fundo = imagem_fundo.resize((width_px, height_px), Image.LANCZOS)
        
        # Preparar para desenhar no certificado
        draw = ImageDraw.Draw(imagem_fundo)
        
        # Obter o nome do arquivo de fonte selecionada
        nome_arquivo_fonte = self.mapeamento_fontes.get(self.estilo_fonte.get(), "arial.ttf")
        nome_arquivo_fonte_italica = self.mapeamento_fontes_italicas.get(self.estilo_fonte.get(), "ariali.ttf")
        
        # Fontes para cada seção do certificado
        try:
            try:
                # Tenta carregar fontes do diretório do executável
                if getattr(sys, 'frozen', False):
                    base_path = sys._MEIPASS
                else:
                    base_path = os.path.dirname(os.path.abspath(__file__))
                
                # Tenta carregar fontes itálicas para nome e texto principal
                try:
                    # Primeiro tenta carregar a fonte itálica do sistema
                    fonte_nome = ImageFont.truetype(os.path.join(base_path, "fonts", nome_arquivo_fonte_italica), 135)
                    fonte_texto = ImageFont.truetype(os.path.join(base_path, "fonts", nome_arquivo_fonte_italica), 45)
                    
                    # Para as demais fontes usa normal
                    fonte_data = ImageFont.truetype(os.path.join(base_path, "fonts", nome_arquivo_fonte), 45)
                    fonte_codigo = ImageFont.truetype(os.path.join(base_path, "fonts", nome_arquivo_fonte), 30)
                    
                    # Marca que conseguimos carregar as fontes itálicas
                    fontes_italicas_carregadas = True
                except Exception:
                    # Se falhar ao carregar fontes itálicas, usar fontes normais
                    fonte_nome = ImageFont.truetype(os.path.join(base_path, "fonts", nome_arquivo_fonte), 135)
                    fonte_texto = ImageFont.truetype(os.path.join(base_path, "fonts", nome_arquivo_fonte), 45)
                    fonte_data = ImageFont.truetype(os.path.join(base_path, "fonts", nome_arquivo_fonte), 40)
                    fonte_codigo = ImageFont.truetype(os.path.join(base_path, "fonts", nome_arquivo_fonte), 30)
                    
                    # Marca que não conseguimos carregar as fontes itálicas
                    fontes_italicas_carregadas = False
            except Exception:
                # Se falhar, tenta carregar do sistema
                try:
                    try:
                        # Tenta carregar fontes itálicas do sistema
                        fonte_nome = ImageFont.truetype(nome_arquivo_fonte_italica, 135)
                        fonte_texto = ImageFont.truetype(nome_arquivo_fonte_italica, 45)
                        fonte_data = ImageFont.truetype(nome_arquivo_fonte, 40)
                        fonte_codigo = ImageFont.truetype(nome_arquivo_fonte, 30)
                        
                        # Marca que conseguimos carregar as fontes itálicas
                        fontes_italicas_carregadas = True
                    except Exception:
                        # Se falhar, usa fontes normais
                        fonte_nome = ImageFont.truetype(nome_arquivo_fonte, 135)
                        fonte_texto = ImageFont.truetype(nome_arquivo_fonte, 45)
                        fonte_data = ImageFont.truetype(nome_arquivo_fonte, 40)
                        fonte_codigo = ImageFont.truetype(nome_arquivo_fonte, 30)
                        
                        # Marca que não conseguimos carregar as fontes itálicas
                        fontes_italicas_carregadas = False
                except Exception:
                    # Se tudo falhar, usa fontes padrão
                    fonte_nome = ImageFont.load_default()
                    fonte_texto = ImageFont.load_default()
                    fonte_data = ImageFont.load_default()
                    fonte_codigo = ImageFont.load_default()
                    
                    # Marca que não conseguimos carregar as fontes itálicas
                    fontes_italicas_carregadas = False
        except Exception:
            # Como última opção, usa a fonte padrão
            fonte_nome = ImageFont.load_default()
            fonte_texto = ImageFont.load_default()
            fonte_data = ImageFont.load_default()
            fonte_codigo = ImageFont.load_default()
            
            # Marca que não conseguimos carregar as fontes itálicas
            fontes_italicas_carregadas = False
        
        # Obter a cor da fonte selecionada
        cor_texto = self.cores[self.cor_fonte.get()]
        
        # Obter o fator de espaçamento entre linhas
        fator_espacamento = float(self.espacamento_linhas.get())
        
        # Posição inicial do texto principal e sua largura máxima (para justificação)
        x_inicio_texto = width_px * 0.20  # 20% da largura (margem esquerda)
        largura_max_texto = width_px * 0.6  # 60% da largura (restante para margem direita)
        
        # Posicionar o nome do participante acima do texto principal
        y_inicio_nome = height_px * 0.47  # Ajustado para ficar adequadamente acima do texto principal
        
        # Centralizar o nome do participante
        w_nome, h_nome = self.get_text_dimensions(nome_participante, fonte_nome)
        x_nome = (width_px - w_nome) / 2
        
        # Desenhar o nome do participante centralizado e em itálico
        if fontes_italicas_carregadas:
            # Se temos fontes itálicas, usamos diretamente
            draw.text((x_nome, y_inicio_nome), nome_participante, font=fonte_nome, fill=cor_texto)
        else:
            # Caso contrário, aplicamos a transformação
            try:
                imagem_fundo = self.aplicar_italico(imagem_fundo, nome_participante, fonte_nome, (int(x_nome), int(y_inicio_nome)), cor_texto)
            except Exception:
                # Fallback para desenho normal em caso de erro
                draw.text((x_nome, y_inicio_nome), nome_participante, font=fonte_nome, fill=cor_texto)
        
        # Posicionar o texto principal após o nome do participante
        y_inicio_texto = y_inicio_nome + h_nome + 100  # Espaço entre o nome e o texto principal
        
        # Texto original do campo de texto (sem o nome do participante)
        texto_principal = texto_completo
        
        # Desenhar o texto centralizado e em itálico 
        if fontes_italicas_carregadas:
            # Se temos fontes itálicas, usamos o método de centralização sem a transformação
            y_final_texto = self.desenhar_texto_centralizado(
                draw, texto_principal, fonte_texto, 
                x_inicio_texto, y_inicio_texto, 
                largura_max_texto, cor_texto,
                fator_espacamento,
                italico=False  # Não precisamos da transformação aqui
            )
        else:
            # Caso contrário, aplicamos a transformação durante a centralização
            y_final_texto = self.desenhar_texto_centralizado(
                draw, texto_principal, fonte_texto, 
                x_inicio_texto, y_inicio_texto, 
                largura_max_texto, cor_texto,
                fator_espacamento,
                italico=True  # Aplica a transformação itálica
            )
        
        # Carga horária (se fornecida) - alinhada à esquerda, abaixo do texto principal
        y_final_texto_com_espaco = y_final_texto + 80
        if self.carga_horaria.get():
            texto_carga = f"Carga horária: {self.carga_horaria.get()}"
            # Usando a mesma margem esquerda do texto principal
            posicao_carga = (x_inicio_texto, y_final_texto_com_espaco)
            draw.text(posicao_carga, texto_carga, font=fonte_texto, fill=cor_texto)
        
            # Atualiza a posição vertical para o próximo elemento
            y_final_texto_com_espaco += self.get_text_dimensions(texto_carga, fonte_texto)[1] + 50
        
        # Data de emissão - agora alinhada à direita
        data = self.data_emissao.get()
        w_data, h_data = self.get_text_dimensions(data, fonte_data)
        # Nova posição: alinhado à direita e entre carga horária e assinatura
        posicao_data = (width_px - x_inicio_texto - w_data, y_final_texto_com_espaco)
        draw.text(posicao_data, data, font=fonte_data, fill=cor_texto)
        
        # Adicionar código de autenticação no canto inferior direito
        texto_codigo = f"Código de autenticação: {codigo_autenticacao}"
        w_codigo, h_codigo = self.get_text_dimensions(texto_codigo, fonte_codigo)
        
        # Posicionar no canto inferior direito com margens
        margem_direita = 100
        margem_inferior = 100
        posicao_codigo = (width_px - w_codigo - margem_direita, height_px - h_codigo - margem_inferior)
        
        # Desenhar retângulo semi-transparente para destacar o código
        padding = 10
        retangulo = [
            posicao_codigo[0] - padding,
            posicao_codigo[1] - padding,
            posicao_codigo[0] + w_codigo + padding,
            posicao_codigo[1] + h_codigo + padding
        ]
        
        # Cor de fundo com transparência (necessário criar uma nova camada)
        overlay = Image.new('RGBA', imagem_fundo.size, (0, 0, 0, 0))
        draw_overlay = ImageDraw.Draw(overlay)
        draw_overlay.rectangle(retangulo, fill=(255, 255, 255, 180))
        
        # Sobrepor a camada do retângulo na imagem principal
        if imagem_fundo.mode == 'RGBA':
            imagem_fundo = Image.alpha_composite(imagem_fundo, overlay)
            draw = ImageDraw.Draw(imagem_fundo)
        else:
            imagem_fundo_rgba = imagem_fundo.convert('RGBA')
            imagem_fundo = Image.alpha_composite(imagem_fundo_rgba, overlay)
            draw = ImageDraw.Draw(imagem_fundo)
        
        # Desenhar o texto do código
        draw.text(posicao_codigo, texto_codigo, font=fonte_codigo, fill='black')
        
        # Salvar certificado
        nome_arquivo = f"{nome_participante.replace(' ', '_')}_certificado.pdf"
        caminho_completo = os.path.join(self.output_dir, nome_arquivo)
        
        # Converter de RGBA para RGB se necessário (para PDF)
        if imagem_fundo.mode == 'RGBA':
            imagem_fundo_rgb = Image.new('RGB', imagem_fundo.size, (255, 255, 255))
            imagem_fundo_rgb.paste(imagem_fundo, mask=imagem_fundo.split()[3])
            imagem_fundo = imagem_fundo_rgb
        
        # Salvar como PDF
        imagem_fundo.save(caminho_completo, "PDF", resolution=300)
        
        return caminho_completo

    def baixar_certificados(self):
        """Abre diálogo para salvar o arquivo ZIP dos certificados"""
        if not self.zip_file_path or not os.path.exists(self.zip_file_path):
            messagebox.showerror("Erro", "Nenhum arquivo ZIP disponível. Gere os certificados primeiro.")
            return
        
        destino = filedialog.asksaveasfilename(
            title="Salvar arquivo ZIP",
            defaultextension=".zip",
            filetypes=[("Arquivos ZIP", "*.zip")],
            initialfile=os.path.basename(self.zip_file_path)
        )
        
        if destino:
            # Copiar o arquivo ZIP para o destino escolhido
            import shutil
            try:
                shutil.copy2(self.zip_file_path, destino)
                messagebox.showinfo("Sucesso", "Certificados baixados com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar o arquivo: {str(e)}")

# Verificar se está sendo executado como script principal
if __name__ == "__main__":
    # Tratar exceções não capturadas
    def handle_exception(exc_type, exc_value, exc_traceback):
        messagebox.showerror(
            "Erro inesperado",
            f"Ocorreu um erro inesperado:\n{exc_value}\n\nPor favor, entre em contato com o suporte."
        )
        # Registrar em arquivo de log
        import logging
        logging.basicConfig(
            filename='error_log.txt',
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.error(
            "Exceção não tratada:",
            exc_info=(exc_type, exc_value, exc_traceback)
        )
    
    # Configurar tratamento de exceção
    sys.excepthook = handle_exception
    
    try:
        # Iniciar a aplicação
        root = tk.Tk()
        app = GeradorCertificados(root)
        
        # Centralizar a janela
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        # Iniciar loop principal
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Erro ao iniciar", f"Falha ao iniciar o aplicativo: {str(e)}")