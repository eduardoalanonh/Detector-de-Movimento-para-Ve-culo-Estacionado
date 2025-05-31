# 🚗 Detector de Movimento em Estacionamento

![Python](https://img.shields.io/badge/Python-3.6%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-success)

## 📋 Descrição

Aplicativo Python que analisa vídeos de estacionamento para detectar movimento em uma área específica e registra timestamps dos eventos. Ideal para verificar se alguém se aproximou do seu veículo enquanto estava estacionado.

## ✨ Funcionalidades

- Interface interativa para selecionar a área de interesse (ROI)
- Detecção de movimento apenas na área selecionada
- Registro de timestamps de início e fim dos movimentos
- Processamento otimizado para vídeos longos
- Opção para interromper a análise e salvar resultados parciais

## 🔧 Requisitos

- Python 3.6+
- OpenCV (`opencv-python`)
- NumPy

## 📥 Instalação

```bash
# Clone o repositório
git clone https://github.com/eduardoalanonh/Detector-de-Movimento-para-Veiculo-Estacionado.git
cd Detector-de-Movimento-para-Ve-culo-Estacionado

# Instale as dependências
pip install opencv-python numpy
```

## 🚀 Como usar

1. Coloque seu vídeo na pasta do script (nome padrão: `estacionamento.mp4`)

2. Execute o script:
```bash
python detectar_movimento2.py
```

3. Siga as instruções na tela:
   - Clique e arraste para desenhar ao redor do seu carro
   - Solte o botão para finalizar
   - Pressione 'S' para confirmar
   - Pressione 'Q' para cancelar

4. Aguarde a análise ser concluída (pode levar algum tempo dependendo do tamanho do vídeo)

5. Verifique os resultados em `movimentos_detectados.txt`

## ⚙️ Configuração

Para personalizar o comportamento do detector, você pode modificar os seguintes parâmetros no código:

- Sensibilidade de detecção (`movement_ratio > 0.001`)
- Intervalo de amostragem (`frame_count % int(fps * 5) == 0`)
- Nome do arquivo de entrada (`video_path = "estacionamento.mp4"`)


## 📄 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

## 📊 Exemplo de Resultado

```
Horários com movimento detectado:
0:05:23 - 0:06:12
0:15:45 - 0:16:03
0:37:22 - 0:38:01
```

---
