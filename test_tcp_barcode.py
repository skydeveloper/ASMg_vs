#!/usr/bin/env python3
"""
Тестов скрипт за TCP баркод мениджъра
"""

import sys
import os
import time
import socket
import threading

# Добавяме пътя на проекта към sys.path
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.services.tcp_barcode_manager import TCPBarcodeManager
from backend.config import Config

class MockSocketIO:
    """Mock SocketIO за тестване"""
    def __init__(self):
        self.emitted_messages = []
    
    def emit(self, event, data):
        self.emitted_messages.append((event, data))
        print(f"SocketIO emit: {event} - {data}")
    
    def start_background_task(self, target):
        print(f"Starting background task: {target.__name__}")
        thread = threading.Thread(target=target, daemon=True)
        thread.start()
        return thread
    
    def sleep(self, seconds):
        time.sleep(seconds)

def test_tcp_barcode_manager():
    """Тества TCP баркод мениджъра"""
    print("=== Тест на TCP баркод мениджъра ===")
    
    # Създаваме mock SocketIO
    mock_socketio = MockSocketIO()
    
    # Създаваме TCP мениджър с тестови настройки
    tcp_manager = TCPBarcodeManager(
        host='127.0.0.1',  # Локален хост за тест
        port=9100,         # Стандартен порт за баркод скенери
        socketio=mock_socketio
    )
    
    print(f"TCP мениджър създаден за {tcp_manager.connection_name}")
    
    # Тестваме отварянето на връзката (ще се провали, защото няма сървър)
    print("\n--- Тест 1: Опит за отваряне на връзка към несъществуващ сървър ---")
    result = tcp_manager.open_port()
    print(f"Резултат от open_port(): {result}")
    
    # Проверяваме изпратените съобщения
    print(f"Изпратени съобщения: {len(mock_socketio.emitted_messages)}")
    for event, data in mock_socketio.emitted_messages:
        print(f"  {event}: {data}")
    
    # Тестваме затварянето на връзката
    print("\n--- Тест 2: Затваряне на връзката ---")
    tcp_manager.close_port()
    print("Връзката е затворена")
    
    print("\n=== Тестът приключи ===")

if __name__ == "__main__":
    test_tcp_barcode_manager() 