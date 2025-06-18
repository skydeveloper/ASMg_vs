# Файл: backend/services/tcp_barcode_manager.py
import socket
import threading
import time
import logging
from queue import Queue

logger = logging.getLogger("ASMg_App")


class TCPBarcodeManager:
    def __init__(self, host, port, socketio):
        self.host = host
        self.port = port
        self.socketio = socketio
        self.socket = None
        self.is_running = False
        self.reader_thread = None
        self.connection_name = f"{self.host}:{self.port}"
        logger.info(f"TCPBarcodeManager initialized for {self.connection_name}")

    def open_port(self):
        """Отваря TCP връзка към баркод скенера"""
        try:
            logger.debug(f"Attempting to open TCP connection to: {self.connection_name}")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)  # 5 секунди timeout за свързване
            self.socket.connect((self.host, self.port))
            self.socket.settimeout(1)  # 1 секунда timeout за четене
            self.is_running = True
            logger.info(f"Successfully opened TCP connection to {self.connection_name}")
            self.socketio.emit('log_message',
                               {'message': f"log.tcpConnectionOpened", 'level': 'success', 'host': self.host, 'port': self.port})
            return True
        except socket.timeout:
            logger.error(f"Timeout connecting to {self.connection_name}")
            self.socketio.emit('log_message',
                               {'message': f"log.tcpConnectionTimeout", 'level': 'error', 'host': self.host, 'port': self.port})
            return False
        except ConnectionRefusedError:
            logger.error(f"Connection refused to {self.connection_name}")
            self.socketio.emit('log_message',
                               {'message': f"log.tcpConnectionRefused", 'level': 'error', 'host': self.host, 'port': self.port})
            return False
        except Exception as e:
            logger.error(f"Generic error opening TCP connection to {self.connection_name}: {e}")
            self.socketio.emit('log_message',
                               {'message': f"log.tcpConnectionOpenError", 'level': 'error', 'host': self.host, 'port': self.port, 'error': str(e)})
            return False

    def start_reading_task(self):
        """Стартира фоновата задача за четене от TCP връзката"""
        if self.is_running and self.socket:
            logger.info("Starting the background task for reading from TCP connection.")
            self.socketio.start_background_task(target=self._read_from_tcp)
        else:
            logger.warning("Attempted to start reading task, but TCP connection is not open or manager not running.")

    def _read_from_tcp(self):
        """Фонова задача за четене на данни от TCP връзката"""
        logger.info(f"Background task started: Now reading from {self.connection_name}...")
        buffer = ""
        
        while self.is_running:
            try:
                if self.socket:
                    # Опитваме да четем данни от сокета
                    data = self.socket.recv(1024)
                    if data:
                        # Декодираме получените данни
                        data_chunk = data.decode('utf-8', errors='ignore')
                        buffer += data_chunk
                        
                        # Обработваме пълните редове (завършващи с \n или \r)
                        while '\n' in buffer or '\r' in buffer:
                            end_pos = -1
                            if '\n' in buffer: 
                                end_pos = buffer.find('\n')
                            if '\r' in buffer:
                                r_pos = buffer.find('\r')
                                if end_pos == -1 or r_pos < end_pos: 
                                    end_pos = r_pos

                            line_to_process = buffer[:end_pos].strip()
                            buffer = buffer[end_pos + 1:]
                            
                            if line_to_process:
                                self._process_barcode_data(line_to_process)
                    else:
                        # Ако не получаваме данни, може би връзката е затворена
                        logger.warning(f"No data received from {self.connection_name}, connection might be closed.")
                        break
                else:
                    # Ако сокетът е затворен междувременно
                    self.is_running = False
                    logger.warning(f"TCP connection {self.connection_name} closed or not available while reading.")
                    break
                    
                self.socketio.sleep(0.05)  # Важно за Socket.IO фонови задачи
                
            except socket.timeout:
                # Timeout при четене - това е нормално, продължаваме
                continue
            except ConnectionResetError:
                logger.error(f"Connection reset by peer for {self.connection_name}")
                self.socketio.emit('log_message',
                                   {'message': f"log.tcpConnectionReset", 'level': 'error', 'host': self.host, 'port': self.port})
                self.is_running = False
                break
            except Exception as e:
                logger.error(f"Unexpected error in _read_from_tcp: {e}", exc_info=True)
                self.is_running = False
                break
                
        logger.info(f"Background task for reading from {self.connection_name} has stopped.")

    def _process_barcode_data(self, data):
        """Обработва получените баркод данни - същата логика като в RS232"""
        logger.info(f"Barcode scanned: '{data}'. Emitting 'barcode_scanned' to frontend.")
        self.socketio.emit('barcode_scanned', {'barcode': data})

    def close_port(self):
        """Затваря TCP връзката"""
        self.is_running = False
        
        if self.socket:
            try:
                self.socket.close()
                logger.info(f"TCP connection {self.connection_name} closed.")
                self.socketio.emit('log_message',
                                   {'message': f"log.tcpConnectionClosed", 'level': 'info', 'host': self.host, 'port': self.port})
            except Exception as e:
                logger.error(f"Error closing TCP connection {self.connection_name}: {e}")
        self.socket = None

    def send_data(self, data):
        """Изпраща данни към баркод скенера (ако е необходимо)"""
        if self.socket and self.is_running:
            try:
                self.socket.send(data.encode('utf-8'))
                logger.info(f"Data sent to {self.connection_name}: {data}")
                return True
            except Exception as e:
                logger.error(f"Error sending data to {self.connection_name}: {e}")
                return False
        else:
            logger.warning(f"TCP connection {self.connection_name} is not open. Cannot send data.")
            return False 