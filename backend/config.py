# Файл: backend/config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_very_secret_key_123!' # Променете това!
    DEBUG = True  # Set to False in production
    PORT = 5000
    HOST = '0.0.0.0' # Позволява достъп от други машини в мрежата
    APP_NAME = "ASMg"

    # Barcode Scanner Configuration - TCP вместо RS232
    BARCODE_SCANNER_HOST = '192.168.0.7'  # IP адрес на баркод скенера
    BARCODE_SCANNER_PORT = 20108  # TCP порт на баркод скенера
    
    # Стари RS232 настройки (запазени за обратна съвместимост)
    BARCODE_SCANNER_COM_PORT = 'COM3'  # Уверете се, че това е правилният порт
    BARCODE_SCANNER_BAUDRATE = 9600

    # OPC UA Server Configuration (примерни стойности)
    OPCUA_SERVER_URL = "opc.tcp://localhost:4840/freeopcua/server/"
    OPCUA_NAMESPACE = "http://example.com/RaspberryPi" 

    # Supported Languages: code: "Display Name"
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'bg': 'Български',
        'sr': 'Srpski'
    }
    DEFAULT_LANGUAGE = 'bg' # Език по подразбиране

    # Конфигурация за Traceability API
    TRACEABILITY_API_URL = os.environ.get('TRACEABILITY_API_URL', "http://oracleapi:3000")
    TRACEABILITY_API_KEY = os.environ.get('TRACEABILITY_API_KEY', "2512A449C4B001DBE0639F2B230AF06F")
    TRACEABILITY_WORKPLACE_ID = os.environ.get('TRACEABILITY_WORKPLACE_ID', "2400") # Използвахме "2400" в тестовете

    # --- Barcode Cameras Configuration ---
    # Всяка камера има два TCP порта:
    # - Порт за команди (TRG): 2006
    # - Порт за получаване на баркод: 2005
    # Пример за получени данни: PDE6N01HM0;334000;203500;-3493
    # Първата стойност е баркодът, останалите са данни за качеството (ще бъдат уточнени допълнително)
    BARCODE_CAMERAS = [
        {
            'name': 'Camera 1',
            'ip': '192.168.0.3',
            'command_port': 2006,
            'barcode_port': 2005,
            'carousel': 1,
            'position': 1
        },
        {
            'name': 'Camera 2',
            'ip': '192.168.0.4',
            'command_port': 2006,
            'barcode_port': 2005,
            'carousel': 1,
            'position': 2
        },
        {
            'name': 'Camera 3',
            'ip': '192.168.0.5',
            'command_port': 2006,
            'barcode_port': 2005,
            'carousel': 1,
            'position': 3
        }
    ]