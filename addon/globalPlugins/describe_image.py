import os
import sys
import ctypes
import tempfile
import api
import globalPluginHandler
import speech
import logHandler
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
    """Captura uma região da tela usando API nativa do Windows"""
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
        # Limpar recursos antes de sair
        gdi32.DeleteObject(bmp)
        gdi32.DeleteDC(img_dc)
        user32.ReleaseDC(hdesktop, desktop_dc)
        raise Exception("Falha ao capturar tela")

    # Salvar como BMP usando função nativa do Windows (se disponível)
    tmp_bmp = os.path.join(tempfile.gettempdir(), f"focused_image_{int(time.time())}.bmp")

    # Tenta usar SaveBitmap se disponível
    try:
        # Define a função SaveBitmap se não estiver definida
        if not hasattr(gdi32, 'SaveBitmap'):
            gdi32.SaveBitmap = getattr(gdi32, 'SaveBitmap', None)

        if gdi32.SaveBitmap:
            gdi32.SaveBitmap.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_wchar_p]
            gdi32.SaveBitmap.restype = ctypes.c_bool

            if gdi32.SaveBitmap(img_dc, bmp, tmp_bmp):
                # Sucesso ao salvar
                gdi32.DeleteObject(bmp)
                gdi32.DeleteDC(img_dc)
                user32.ReleaseDC(hdesktop, desktop_dc)
                return tmp_bmp
    except:
        pass  # Fallback para método alternativo

    # Método alternativo: usa PowerShell para captura direta
    try:
        # Limpar recursos primeiro
        gdi32.DeleteObject(bmp)
        gdi32.DeleteDC(img_dc)
        user32.ReleaseDC(hdesktop, desktop_dc)

        # Usar PowerShell para captura direta
        return capture_with_powershell(rect)
    except Exception as e:
        raise Exception(f"Falha na captura: {str(e)}")


def capture_with_powershell(rect):
    """Captura tela usando PowerShell nativo"""
    x, y, width, height = rect
    tmp_bmp = os.path.join(tempfile.gettempdir(), f"focused_image_{int(time.time())}.bmp")

    ps_script = f"""
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing

    $bounds = [System.Drawing.Rectangle]::new({x}, {y}, {width}, {height})
    $bmp = New-Object System.Drawing.Bitmap({width}, {height})
    $graphics = [System.Drawing.Graphics]::FromImage($bmp)
    $graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
    $bmp.Save('{tmp_bmp}', [System.Drawing.Imaging.ImageFormat]::Bmp)
    $graphics.Dispose()
    $bmp.Dispose()
    Write-Output "SUCCESS"
    """

    try:
        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            check=True,
            capture_output=True,
            text=True,
            timeout=10
        )

        if "SUCCESS" in result.stdout and os.path.exists(tmp_bmp):
            return tmp_bmp
        else:
            raise Exception("Falha na captura via PowerShell")
    except subprocess.TimeoutExpired:
        raise Exception("Timeout na captura de tela")
    except Exception as e:
        raise Exception(f"Erro no PowerShell: {str(e)}")


def convert_bmp_to_png(bmp_path):
    """Converte BMP para PNG usando PowerShell"""
    if not os.path.exists(bmp_path):
        raise Exception("Arquivo BMP não encontrado")

    png_path = bmp_path.replace('.bmp', '.png')

    ps_script = f"""
    try {{
        Add-Type -AssemblyName System.Drawing
        $bitmap = [System.Drawing.Bitmap]::FromFile('{bmp_path}')
        $bitmap.Save('{png_path}', [System.Drawing.Imaging.ImageFormat]::Png)
        $bitmap.Dispose()
        Write-Output "SUCCESS"
    }} catch {{
        Write-Output "ERROR"
    }}
    """

    try:
        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            check=True,
            capture_output=True,
            text=True,
            timeout=10
        )

        if "SUCCESS" in result.stdout and os.path.exists(png_path):
            # Remove o BMP temporário
            try:
                os.remove(bmp_path)
            except:
                pass
            return png_path
        else:
            # Retorna o BMP original se conversão falhar
            return bmp_path

    except:
        # Fallback: retorna o BMP original
        return bmp_path


def capture_and_convert(rect):
    """Captura a tela e converte para PNG"""
    bmp_file = None
    try:
        # Captura como BMP
        bmp_file = capture_screen(rect)

        if not bmp_file or not os.path.exists(bmp_file):
            raise Exception("Arquivo BMP não foi criado")

        # Converte para PNG
        final_file = convert_bmp_to_png(bmp_file)

        if not os.path.exists(final_file):
            raise Exception("Arquivo final não foi criado")

        return final_file

    except Exception as e:
        logHandler.log.error(f"Erro na captura/conversão: {e}")
        # Tenta retornar o BMP se existir
        if bmp_file and os.path.exists(bmp_file):
            speech.speakText("Usando formato BMP")
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

            # Captura e converte
            tmp_file = capture_and_convert(rect)

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
            speech.speakText(f"Erro: {str(e)}")

        finally:
            # Limpa arquivo temporário
            if tmp_file and os.path.exists(tmp_file):
                try:
                    os.remove(tmp_file)
                except:
                    pass

    __gestures = {
        "kb:NVDA+i": "descreverImagem"
    }