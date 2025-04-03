# Manual do Usuário - Gerador de Certificados

## Sumário
1. [Introdução](#introdução)
2. [Requisitos do Sistema](#requisitos-do-sistema)
3. [Instalação](#instalação)
4. [Interface Principal](#interface-principal)
5. [Gerando Certificados](#gerando-certificados)
6. [Validando Certificados](#validando-certificados)
7. [Distribuição dos Certificados](#distribuição-dos-certificados)
8. [Perguntas Frequentes](#perguntas-frequentes)
9. [Solução de Problemas](#solução-de-problemas)

## Introdução

O Gerador de Certificados é uma aplicação desktop desenvolvida para facilitar a criação de certificados em massa a partir de uma lista de nomes. Cada certificado gerado recebe um código único de autenticação, permitindo verificar sua validade posteriormente. O sistema é ideal para instituições de ensino, organizadores de eventos, cursos e treinamentos que precisam emitir certificados para múltiplos participantes.

### Principais Recursos

- Geração em massa de certificados a partir de lista CSV
- Código de autenticação único para cada certificado
- Sistema integrado de validação de certificados
- Interface intuitiva e fácil de usar
- Personalização de texto, fonte e cores
- Exportação de certificados em formato PDF

## Requisitos do Sistema

- Sistema Operacional: Windows 7/8/10/11
- Memória RAM: Mínimo 2GB (4GB recomendado)
- Espaço em Disco: 100MB disponíveis
- Tela com resolução mínima de 1024x768

## Instalação

### Instalação a partir do Executável

1. Baixe o arquivo executável "Gerador de Certificados.exe"
2. Execute o arquivo baixado
3. Não é necessário instalar - o programa é portátil e pode ser executado diretamente

### Instalação a partir do Código-Fonte

Se você deseja executar o programa a partir do código-fonte, siga estas etapas:

1. Certifique-se de ter o Python 3.12 ou superior instalado
2. Instale as dependências necessárias:
   ```
   uv add pillow pandas tk
   ```
3. Execute o arquivo principal:
   ```
   uv run python build.py
   ```

## Interface Principal

Ao iniciar o programa, você verá uma interface com duas abas:

- **Gerar Certificados**: Para configurar e gerar novos certificados
- **Validar Certificado**: Para verificar a autenticidade de certificados já emitidos

## Gerando Certificados

### 1. Preparar a Imagem de Fundo

Prepare uma imagem PNG que servirá como fundo do certificado. Recomendações:
- Formato paisagem (horizontal)
- Resolução mínima de 3508 x 2480 pixels (equivalente a A4 em 300 DPI)
- Inclua na imagem elementos como logotipos, bordas decorativas e assinaturas
- Reserve espaço para o texto do certificado na área central

### 2. Preparar o Arquivo CSV

Crie um arquivo CSV contendo a lista de nomes dos participantes. O arquivo deve:
- Ter uma coluna chamada "nome" ou "Nome"
- Usar vírgula como separador de campos
- Estar codificado preferencialmente em UTF-8

Exemplo de conteúdo do arquivo CSV:
```
Nome
João da Silva
Maria Oliveira
Pedro Santos
```

### 3. Configurar os Campos do Certificado

Na aba "Gerar Certificados", preencha os campos:

1. **Imagem de Fundo**: Clique em "Selecionar" e escolha o arquivo PNG preparado
2. **Texto Principal**: Digite o texto do certificado que virá após o nome do participante
   - Exemplo: "participou do curso de Excel Avançado, realizado nos dias 10 e 11 de abril de 2025, com aproveitamento satisfatório."
3. **Carga Horária**: Digite a carga horária do curso (opcional)
4. **Cor da Fonte**: Selecione a cor do texto
5. **Estilo de Fonte**: Escolha a fonte a ser utilizada
6. **Espaçamento entre Linhas**: Ajuste o espaçamento conforme necessário
7. **Data de Emissão**: Informe a data no formato "Cidade-UF, dia de mês de ano"
8. **Arquivo CSV**: Clique em "Selecionar" e escolha o arquivo CSV com a lista de nomes

### 4. Gerar os Certificados

1. Após preencher todos os campos, clique no botão "Gerar Certificados"
2. Aguarde o processamento - o progresso será exibido na barra inferior
3. Quando concluído, uma mensagem de sucesso será exibida
4. Clique em "Baixar Certificados" para salvar o arquivo ZIP contendo todos os certificados gerados

## Validando Certificados

Para verificar a autenticidade de um certificado:

1. Acesse a aba "Validar Certificado"
2. Digite o código de autenticação impresso no canto inferior direito do certificado
   - O código segue o formato XXXX-XXXX-XXXX
3. Clique no botão "Validar"
4. O resultado da validação será exibido:
   - Se o certificado for válido, os detalhes como nome, data de emissão e carga horária serão mostrados
   - Se o certificado não for reconhecido, uma mensagem de erro será exibida

## Distribuição dos Certificados

Após gerar os certificados, você pode distribuí-los das seguintes formas:

### Distribui o Arquivo ZIP Completo

Ideal para enviar todos os certificados para um coordenador ou responsável que fará a distribuição individual.

### Extrair e Enviar Certificados Individuais

1. Extraia o conteúdo do arquivo ZIP
2. Envie a cada participante apenas o seu certificado específico por e-mail ou outra plataforma

### Distribuição do Validador de Certificados

Se desejar que outras pessoas possam validar os certificados:

1. Distribua o executável do validador junto com o arquivo do banco de dados
2. Alternativamente, informe o endereço de um validador online, se disponível

## Perguntas Frequentes

### Como alterar o tamanho da fonte?

O tamanho da fonte é predefinido para garantir a melhor legibilidade. Se precisar ajustar, será necessário modificar o código-fonte.

### Posso usar uma imagem de fundo em formato JPG?

Recomendamos o uso de arquivos PNG para melhor qualidade. Se precisar usar JPG, converta-o para PNG antes de usá-lo no programa.

### Os certificados gerados são válidos legalmente?

A validade legal dos certificados depende da autoridade da instituição emissora. O sistema apenas fornece uma ferramenta para geração e validação.

### Como atualizar o banco de dados de certificados validáveis?

O banco de dados é atualizado automaticamente durante a geração de certificados. Se precisar compartilhar o validador, distribua também o arquivo JSON de banco de dados.

## Solução de Problemas

### O programa não inicia

- Verifique se seu sistema atende aos requisitos mínimos
- Tente executar o programa como administrador
- Verifique se todas as dependências estão instaladas (se executando via código-fonte)

### Erro ao gerar certificados

- Verifique se a imagem de fundo está no formato correto e com resolução adequada
- Confira se o arquivo CSV está formatado corretamente com a coluna "nome" ou "Nome"
- Certifique-se de que há espaço suficiente no disco para salvar os certificados

### Erro na validação de certificados

- Verifique se digitou o código exatamente como aparece no certificado
- Confirme se está usando o mesmo arquivo de banco de dados que foi gerado junto com os certificados
- Certifique-se de que o código não está danificado ou parcialmente visível no certificado

---

Para suporte adicional ou dúvidas não abordadas neste manual, entre em contato com o desenvolvedor.
