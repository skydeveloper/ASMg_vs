#!/usr/bin/env python3
"""
TCP сървър симулатор за баркод скенер
Този скрипт създава прост TCP сървър, който симулира баркод скенер
"""

import socket
import threading
import time
import random

class BarcodeScannerSimulator:
    def __init__(self, host='0.0.0.0', port=9100):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []
        self.is_running = False
        
    def start_server(self):
        """Стартира TCP сървъра"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.is_running = True
            
            print(f"Баркод скенер симулатор стартиран на {self.host}:{self.port}")
            print("Очаквам връзки от клиенти...")
            
            while self.is_running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    print(f"Нова връзка от {client_address}")
                    
                    # Създаваме отделна нишка за всеки клиент
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address),
                        daemon=True
                    )
                    client_thread.start()
                    self.clients.append(client_socket)
                    
                except socket.error:
                    if self.is_running:
                        print("Грешка при приемане на връзка")
                    break
                    
        except Exception as e:
            print(f"Грешка при стартиране на сървъра: {e}")
        finally:
            self.stop_server()
    
    def handle_client(self, client_socket, client_address):
        """Обработва връзка с клиент"""
        print(f"Обработвам клиент {client_address}")
        
        try:
            while self.is_running and client_socket in self.clients:
                # Симулираме сканиране на баркод на всеки 5-10 секунди
                time.sleep(random.uniform(5, 10))
                
                if not self.is_running or client_socket not in self.clients:
                    break
                
                # Генерираме случайни баркод данни
                barcode_data = self.generate_barcode()
                print(f"Изпращам баркод към {client_address}: {barcode_data}")
                
                try:
                    # Изпращаме баркода с CR+LF терминатор
                    client_socket.send(f"{barcode_data}\r\n".encode('utf-8'))
                except socket.error:
                    print(f"Грешка при изпращане към {client_address}")
                    break
                    
        except Exception as e:
            print(f"Грешка при обработка на клиент {client_address}: {e}")
        finally:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            client_socket.close()
            print(f"Връзката с {client_address} е затворена")
    
    def generate_barcode(self):
        """Генерира случайни баркод данни"""
        barcode_types = [
            "123456789012",  # EAN-12
            "1234567890123", # EAN-13
            "123456789012345", # EAN-15
            "ABC123456789",  # Code 128
            "XYZ987654321",  # Code 128
            "QR123456789",   # QR Code
            "DATA123456",    # Data Matrix
        ]
        return random.choice(barcode_types)
    
    def stop_server(self):
        """Спира сървъра"""
        print("Спирам баркод скенер симулатора...")
        self.is_running = False
        
        # Затваряме всички клиентски връзки
        for client in self.clients[:]:
            try:
                client.close()
            except:
                pass
        self.clients.clear()
        
        # Затваряме сървърния сокет
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        print("Баркод скенер симулаторът е спрян")

def main():
    """Главна функция"""
    print("=== TCP Баркод Скенер Симулатор ===")
    print("Този скрипт създава симулатор на баркод скенер, който изпраща случайни баркодове")
    print("Стартира се на порт 9100 (стандартен за баркод скенери)")
    print("Натиснете Ctrl+C за спиране\n")
    
    simulator = BarcodeScannerSimulator()
    
    try:
        simulator.start_server()
    except KeyboardInterrupt:
        print("\nПолучен сигнал за спиране...")
    finally:
        simulator.stop_server()

if __name__ == "__main__":
    main() 