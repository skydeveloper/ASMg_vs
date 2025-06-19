import socket
import logging
from backend.config import Config

logger = logging.getLogger("barcode_camera")

class BarcodeCameraManager:
    def __init__(self, cameras_config=None):
        self.cameras = cameras_config or Config.BARCODE_CAMERAS

    def trigger_and_read_barcode(self, camera):
        """
        Изпраща команда TRG към камерата и чете баркод от съответния порт.
        Връща dict: {'status': 'success'|'fail'|'timeout', 'value': ...}
        """
        ip = camera['ip']
        command_port = camera['command_port']
        barcode_port = camera['barcode_port']
        name = camera.get('name', 'Unknown')
        position = camera.get('position', '?')
        carousel = camera.get('carousel', '?')
        
        # 1. Изпращане на TRG команда
        try:
            with socket.create_connection((ip, command_port), timeout=2) as s:
                s.sendall(b'TRG\r\n')
        except Exception as e:
            logger.error(f"[Camera {name}] Грешка при изпращане на TRG: {e}")
            return {'status': 'timeout', 'value': None}
        
        # 2. Четене на баркод от другия порт
        try:
            with socket.create_connection((ip, barcode_port), timeout=2) as s:
                s.settimeout(2)
                data = s.recv(1024).decode('utf-8').strip()
                if data.upper().startswith('FAIL'):
                    logger.warning(f"[Карусел {carousel} Позиция {position}] Камерата върна FAIL")
                    return {'status': 'fail', 'value': None}
                barcode = data.split(';')[0] if ';' in data else data
                logger.info(f"[Карусел {carousel} Позиция {position}] Прочетен баркод: {barcode}")
                return {'status': 'success', 'value': barcode}
        except socket.timeout:
            logger.error(f"[Camera {name}] Timeout при четене на баркод!")
            return {'status': 'timeout', 'value': None}
        except Exception as e:
            logger.error(f"[Camera {name}] Грешка при четене на баркод: {e}")
            return {'status': 'timeout', 'value': None}

    def read_all_cameras(self):
        """
        Стартира TRG и чете баркод от всички камери. Връща dict: позиция -> {'status', 'value'}
        """
        results = {}
        for cam in self.cameras:
            res = self.trigger_and_read_barcode(cam)
            pos = cam.get('position', '?')
            results[pos] = res
        return results 