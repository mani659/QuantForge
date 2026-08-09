import unittest
from types import MappingProxyType
from unittest.mock import Mock, patch

from boe.execution import (
    DefaultMT5Transport,
    MT5TransportConfig,
    MT5InitializationError,
    MT5ConnectionError,
    MT5CommunicationError
)

class MockMT5SDK:
    def __init__(self, init_success=True, term_info_success=True, order_success=True):
        self.init_success = init_success
        self.term_info_success = term_info_success
        self.order_success = order_success
        self.shutdown_called = False
        
    def initialize(self, path):
        return self.init_success
        
    def terminal_info(self):
        return Mock() if self.term_info_success else None
        
    def shutdown(self):
        self.shutdown_called = True
        
    def order_send(self, request):
        if not self.order_success:
            return None
        mock_result = Mock()
        mock_result.retcode = 10009
        mock_result.deal = 123
        mock_result.order = 456
        mock_result.volume = 1.0
        mock_result.price = 1.1000
        mock_result.comment = "mock"
        return mock_result

class TestMT5Transport(unittest.TestCase):

    def setUp(self):
        self.config = MT5TransportConfig(
            terminal_path="dummy/path",
            metadata=MappingProxyType({})
        )

    def test_initialization_success(self):
        mock_sdk = MockMT5SDK()
        transport = DefaultMT5Transport(self.config, mt5_module=mock_sdk)
        
        self.assertTrue(transport.initialize())

    def test_initialization_failure(self):
        mock_sdk = MockMT5SDK(init_success=False)
        transport = DefaultMT5Transport(self.config, mt5_module=mock_sdk)
        
        with self.assertRaisesRegex(MT5InitializationError, "Failed to initialize MT5"):
            transport.initialize()

    def test_connection_failure(self):
        mock_sdk = MockMT5SDK(term_info_success=False)
        transport = DefaultMT5Transport(self.config, mt5_module=mock_sdk)
        
        with self.assertRaisesRegex(MT5ConnectionError, "MT5 terminal is not connected"):
            transport.initialize()

    def test_shutdown(self):
        mock_sdk = MockMT5SDK()
        transport = DefaultMT5Transport(self.config, mt5_module=mock_sdk)
        transport.initialize()
        
        transport.shutdown()
        self.assertTrue(mock_sdk.shutdown_called)
        
    def test_mocked_sdk_interaction(self):
        mock_sdk = MockMT5SDK()
        transport = DefaultMT5Transport(self.config, mt5_module=mock_sdk)
        transport.initialize()
        
        req = {"action": 1}
        resp = transport.send_request(req)
        
        self.assertEqual(resp["retcode"], 10009)
        self.assertEqual(resp["deal"], 123)
        self.assertEqual(resp["order"], 456)
        self.assertIsInstance(resp, dict)

    def test_transport_error_propagation(self):
        mock_sdk = MockMT5SDK(order_success=False)
        transport = DefaultMT5Transport(self.config, mt5_module=mock_sdk)
        transport.initialize()
        
        with self.assertRaisesRegex(MT5CommunicationError, "Order send failed"):
            transport.send_request({})
            
    def test_uninitialized_communication(self):
        mock_sdk = MockMT5SDK()
        transport = DefaultMT5Transport(self.config, mt5_module=mock_sdk)
        
        with self.assertRaisesRegex(MT5CommunicationError, "Transport is not initialized"):
            transport.send_request({})

if __name__ == '__main__':
    unittest.main()
