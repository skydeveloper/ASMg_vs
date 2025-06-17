# Файл: backend/services/device_communicator.py
import requests
import json
import logging

# Вземаме логера, който вече е конфигуриран в app.py
logger = logging.getLogger("ASMg_App")  # Уверете се, че името съвпада с това в app.py


class DeviceCommunicator:
    def __init__(self):
        # Създаваме сесия с keep-alive връзки
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
        # Настройваме keep-alive
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=100,
            pool_maxsize=100,
            max_retries=3,
            pool_block=False
        )
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        logger.info("DeviceCommunicator initialized with keep-alive session.")

    def _send_request(self, method, url, payload=None, headers=None):
        try:
            logger.debug(
                f"Sending {method} request to {url} with payload: {json.dumps(payload) if payload else 'None'}")

            if headers:
                self.session.headers.update(headers)

            if method.upper() == 'POST':
                response = self.session.post(url, json=payload, timeout=2)
            elif method.upper() == 'GET':
                response = self.session.get(url, params=payload, timeout=2)
            else:
                logger.error(f"Unsupported HTTP method: {method}")
                return None

            response.raise_for_status()  # Хвърля грешка за 4xx/5xx HTTP статуси

            logger.debug(
                f"Received response from {url}: {response.status_code} - {response.text[:200]}")  # Първите 200 символа
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logger.error(
                f"HTTP error occurred: {http_err} - URL: {url} - Response: {http_err.response.text if http_err.response else 'N/A'}")
        except requests.exceptions.ConnectionError as conn_err:
            logger.error(f"Connection error occurred: {conn_err} - URL: {url}")
        except requests.exceptions.Timeout as timeout_err:
            logger.error(f"Timeout error occurred: {timeout_err} - URL: {url}")
        except requests.exceptions.RequestException as req_err:
            logger.error(f"An error occurred: {req_err} - URL: {url}")
        except json.JSONDecodeError as json_err:
            logger.error(
                f"JSON decode error for response from {url}: {json_err} - Response was: {response.text if 'response' in locals() else 'N/A'}")
        return None

    def start_test_on_device(self, device_ip, device_port, module_id, test_sequence_name):
        """
        Изпраща команда за стартиране на тест към конкретно устройство.
        """
        url = f"http://{device_ip}:{device_port}/api/start_test"  # Примерно URL
        payload = {
            "module_id": module_id,
            "test_sequence_name": test_sequence_name
        }
        return self._send_request('POST', url, payload)

    def start_programming_on_device(self, device_ip, device_port, module_id, firmware_details):
        """
        Изпраща команда за стартиране на програмиране към конкретно устройство.
        """
        url = f"http://{device_ip}:{device_port}/api/start_programming"  # Примерно URL
        payload = {
            "module_id": module_id,
            "firmware": firmware_details
            # firmware_details може да е обект с име на файл, версия и т.н.
        }
        return self._send_request('POST', url, payload)

    def get_device_status(self, device_ip, device_port):
        """
        Изпраща заявка за получаване на статуса на устройство.
        """
        url = f"http://{device_ip}:{device_port}/api/status"  # Примерно URL
        return self._send_request('GET', url)

    def send_task_to_device_client(self, device_ip, device_port, task_payload):
        """
        Изпраща обща задача към /api/start_task ендпойнта на DeviceClientApp.
        task_payload трябва да съдържа ключовете, които DeviceClientApp очаква,
        например: module_serial_numbers, active_slots, item_name, firmware_details
        """
        url = f"http://{device_ip}:{device_port}/api/start_task"
        logger.info(f"DeviceCommunicator: Изпращане на задача към {url} с payload: {task_payload}")
        return self._send_request('POST', url, payload=task_payload)