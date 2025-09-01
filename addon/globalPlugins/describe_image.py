import os
import sys
import ctypes
import tempfile
import api
import globalPluginHandler
import speech
import logHandler
import struct
import subprocess
import time

addon_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(addon_dir, '..', 'lib')
addon_root = os.path.abspath(os.path.join(addon_dir, '..'))

for path in (lib_dir, addon_root):
    if path not in sys.path:
        sys.path.insert(0, path)

from stackspot.stackspot import Stackspot
import addonConfig

client_id = addonConfig.getPref("client_id")
client_secret = addonConfig.getPref("client_secret")
realm = addonConfig.getPref("realm")
slug = addonConfig.getPref("slug")


def capture_screen(rect):
    """Captura uma região da tela e retorna como arquivo BMP"""
    x, y, width, height = rect

    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32

    # Obter handle da área de trabalho
    hdesktop = user32.GetDesktopWindow()
    desktop_dc = user32.GetWindowDC(hdesktop)
    img_dc = gdi32.CreateCompatibleDC(desktop_dc)

    # Criar bitmap
    bmp = gdi32.CreateCompatibleBitmap(desktop_dc, width, height)
    gdi32.SelectObject(img_dc, bmp)

    # Copiar região da tela
    SRCCOPY = 0x00CC0020
    success = gdi32.BitBlt(img_dc, 0, 0, width, height, desktop_dc, x, y, SRCCOPY)

    if not success:
        raise Exception("Falha ao capturar tela")

    # Salvar como BMP
    tmp_bmp = os.path.join(tempfile.gettempdir(), f"focused_image_{int(time.time())}.bmp")
    save_as_bmp(tmp_bmp, img_dc, bmp, width, height)

    # Limpar recursos
    gdi32.DeleteObject(bmp)
    gdi32.DeleteDC(img_dc)
    user32.ReleaseDC(hdesktop, desktop_dc)

    return tmp_bmp


def save_as_bmp(filename, img_dc, bmp, width, height):
    """Salva o bitmap como arquivo BMP"""

    # Obter informações do bitmap
    class BITMAP(ctypes.Structure):
        _fields_ = [
            ("bmType", ctypes.c_long),
            ("bmWidth", ctypes.c_long),
            ("bmHeight", ctypes.c_long),
            ("bmWidthBytes", ctypes.c_long),
            ("bmPlanes", ctypes.c_ushort),
            ("bmBitsPixel", ctypes.c_ushort),
            ("bmBits", ctypes.c_void_p)
        ]

    bmp_info = BITMAP()
    gdi32 = ctypes.windll.gdi32
    gdi32.GetObjectW(bmp, ctypes.sizeof(bmp_info), ctypes.byref(bmp_info))

    # Calcular tamanho dos dados
    buffer_size = bmp_info.bmHeight * bmp_info.bmWidthBytes
    buffer = ctypes.create_string_buffer(buffer_size)
    gdi32.GetBitmapBits(bmp, buffer_size, buffer)

    # Escrever arquivo BMP
    with open(filename, 'wb') as f:
        # File header (14 bytes)
        file_header = struct.pack('<2sLHHHL',
                                  b'BM',  # Signature
                                  14 + 40 + buffer_size,  # File size
                                  0, 0,  # Reserved
                                  14 + 40,  # Pixel data offset
                                  )
        f.write(file_header)

        # Info header (40 bytes)
        info_header = struct.pack('<LLLHHLLLLLL',
                                  40,  # Header size
                                  width,  # Width
                                  height,  # Height
                                  1,  # Planes
                                  24,  # Bits per pixel
                                  0,  # Compression
                                  buffer_size,  # Image size
                                  0, 0,  # XPelsPerMeter, YPelsPerMeter
                                  0,  # Colors used
                                  0  # Colors important
                                  )
        f.write(info_header)

        # Pixel data (BGR format, bottom-to-top)
        for y in range(height - 1, -1, -1):
            start = y * bmp_info.bmWidthBytes
            end = start + width * 3
            line_data = buffer[start:end]
            f.write(line_data)

            # Padding para múltiplo de 4 bytes
            padding = (4 - (width * 3) % 4) % 4
            if padding:
                f.write(b'\x00' * padding)

def convert_bmp_to_png(bmp_path):
    """Converte BMP para PNG usando PowerShell nativo do Windows"""
    if not bmp_path or not os.path.exists(bmp_path):
        raise Exception("Arquivo BMP não encontrado")

    png_path = bmp_path.replace('.bmp', '.png')

    # Script PowerShell para conversão
    ps_script = f"""
    try {{
        Add-Type -AssemblyName System.Drawing
        $bitmap = [System.Drawing.Bitmap]::FromFile('{bmp_path}')
        $bitmap.Save('{png_path}', [System.Drawing.Imaging.ImageFormat]::Png)
        $bitmap.Dispose()
        Write-Output "SUCCESS"
    }} catch {{
        Write-Output "ERROR: $($_.Exception.Message)"
        exit 1
    }}
    """

    # Executar conversão
    try:
        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            check=True,
            capture_output=True,
            text=True,
            timeout=15
        )

        if "SUCCESS" in result.stdout:
            # Limpar arquivo BMP temporário
            try:
                os.remove(bmp_path)
            except:
                pass
            return png_path
        else:
            raise Exception(f"Falha na conversão: {result.stdout}")

    except subprocess.TimeoutExpired:
        raise Exception("Timeout na conversão de imagem")
    except subprocess.CalledProcessError as e:
        raise Exception(f"Erro no PowerShell: {e.stderr}")
    except Exception as e:
        raise Exception(f"Erro na conversão: {str(e)}")


def capture_and_convert(rect):
    """Captura a tela e converte para PNG"""
    bmp_file = None
    try:
        # Captura como BMP
        bmp_file = capture_screen(rect)

        # Converte para PNG
        png_file = convert_bmp_to_png(bmp_file)

        # Verifica se o PNG foi criado
        if os.path.exists(png_file) and os.path.getsize(png_file) > 0:
            return png_file
        else:
            raise Exception("Arquivo PNG não foi criado corretamente")

    except Exception as e:
        logHandler.log.error(f"Erro na captura/conversão: {e}")
        # Fallback: tenta usar o BMP se a conversão falhar
        if bmp_file and os.path.exists(bmp_file):
            speech.speakText("Usando formato BMP como fallback")
            return bmp_file
        raise


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

    def script_descreverImagem(self, gesture):
        tmp_file = None
        try:
            obj = api.getFocusObject()
            rect = obj.location if obj and obj.location else None

            if not rect:
                x, y = api.getMousePosition()
                rect = (x - 100, y - 100, 200, 200)
                speech.speakText("Capturando área do cursor.")

            # Captura e converte para PNG
            tmp_file = capture_and_convert(rect)

            # Verifica o formato do arquivo
            file_ext = os.path.splitext(tmp_file)[1].lower()
            if file_ext == '.bmp':
                speech.speakText("Aviso: usando formato BMP")

            # Envia para o Stackspot
            stackspot = Stackspot.instance().credential(
                client_id=client_id,
                client_secret=client_secret,
                realm=realm
            )

            result = stackspot.send_file_stackspot(tmp_file, "CONTEXT", "").transcription(slug)

            speech.speakText(result)

        except Exception as e:
            logHandler.log.error(f'Error: {e}')
            speech.speakText(f"Erro ao processar imagem: {str(e)}")

        finally:
            # Limpa arquivo temporário (se existir)
            if tmp_file and os.path.exists(tmp_file):
                try:
                    os.remove(tmp_file)
                except:
                    pass

    __gestures = {
        "kb:NVDA+i": "descreverImagem"
    }