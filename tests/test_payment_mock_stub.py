import pytest
import requests
import unittest

from unittest.mock import (
    Mock, patch
)

from services.payment_service  import PaymentGateway
from services.library_service import (
    pay_late_fees, refund_late_fee_payment
)

"""
def pay_late_fees(patron_id: str, book_id: int, payment_gateway: PaymentGateway = None) -> Tuple[bool, str, Optional[str]]:
    Process payment for late fees using external payment gateway.
    
    NEW FEATURE FOR ASSIGNMENT 3: Demonstrates need for mocking/stubbing
    This function depends on an external payment service that should be mocked in tests.
    
    Args:
        patron_id: 6-digit library card ID
        book_id: ID of the book with late fees
        payment_gateway: Payment gateway instance (injectable for testing)
        
    Returns:
        tuple: (success: bool, message: str, transaction_id: Optional[str])
        
    Example for you to mock:
        # In tests, mock the payment gateway:
        mock_gateway = Mock(spec=PaymentGateway)
        mock_gateway.process_payment.return_value = (True, "txn_123", "Success")
        success, msg, txn = pay_late_fees("123456", 1, mock_gateway)
"""


"""
def refund_late_fee_payment(transaction_id: str, amount: float, payment_gateway: PaymentGateway = None) -> Tuple[bool, str]:
    Refund a late fee payment (e.g., if book was returned on time but fees were charged in error).
    
    NEW FEATURE FOR ASSIGNMENT 3: Another function requiring mocking
    
    Args:
        transaction_id: Original transaction ID to refund
        amount: Amount to refund
        payment_gateway: Payment gateway instance (injectable for testing)
        
    Returns:
        tuple: (success: bool, message: str)
    """




def pay_late_fee_successful(mocker):

    mocker.patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": 7.00, "days_overdue": 3})
    mocker.patch("services.library_service.get_book_by_id", return_value={"title": "Sample"})

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, "txn_123", "Success")
    success, msg, txn = pay_late_fees("123456", 1, mock_gateway)

    assert success == True
    assert "successful" in msg.lower()
    assert "txn_" in txn.lower()

    mock_gateway.process_payment.assert_called_once()

    #Need to stub later
    mock_gateway.process_payment.assert_called_with("123456", 7.00, "Late fees for 'Sample'")



def pay_late_fee_declined_by_gateway(mocker):

    mocker.patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": -1.00, "days_overdue": 3})
    mocker.patch("services.library_service.get_book_by_id", return_value={"title": "Sample"})

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (False, "", "Invalid amount: must be greater than 0")
    success, msg, txn = pay_late_fees("123456", 1, mock_gateway)

    assert success == False
    assert "failed" in msg.lower()
    assert txn is None

    mock_gateway.process_payment.assert_called_once()
    mock_gateway.process_payment.assert_called_with("123456", -1.00, "Late fees for 'Sample'")



def pay_late_fee_invalid_id():
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, "txn_123", "Success")
    success, msg, txn = pay_late_fees("123456789", 1, mock_gateway)

    assert success == False
    assert "invalid" in msg.lower()
    assert txn is None

    mock_gateway.process_payment.assert_not_called()



def pay_late_fee_zero_late_fees(mocker):
    mocker.patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": 0, "days_overdue": 0})
    mocker.patch("services.library_service.get_book_by_id", return_value={"title": "Sample"})

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, "txn_123", "Success")
    success, msg, txn = pay_late_fees("123456", 1, mock_gateway)

    assert success == False
    assert "unable" in msg.lower()
    assert txn is None

    mock_gateway.process_payment.assert_not_called()



def pay_late_fee_network_error_exception(mocker):
    mocker.patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": 2.00, "days_overdue": 1})
    mocker.patch("services.library_service.get_book_by_id", return_value={"title": "Sample"})

    #TODO: Figure out how to do a network error
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, "txn_123", "Success")
    success, msg, txn = pay_late_fees("123456", 1, mock_gateway)

    assert success == False
    assert "error" in msg.lower()
    assert txn is None










def refund_late_fee_payment_successful_refund():
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (True, "Refund of $7.00 processed successfully. Refund ID: txn_1234")
    success, message = refund_late_fee_payment("txn_123", 7.00, mock_gateway)

    assert success == True
    assert "refund of" in message.lower()

    mock_gateway.refund_payment.assert_called_once()
    mock_gateway.refund_payment.assert_called_with("txn_123", 7.00)



def refund_late_fee_payment_invalid_transaction_ID():
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (False, "Invalid transaction ID")
    success, message = refund_late_fee_payment("wrong ID", 7.00, mock_gateway)

    assert success == False
    assert "invalid" in message.lower()

    mock_gateway.refund_payment.assert_not_called()



def refund_late_fee_payment_invalid_refund_amount():
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (False, "Invalid refund amount")
    success, message = refund_late_fee_payment("txn_123", -1.00, mock_gateway)

    assert success == False
    assert "greater than" in message.lower()
    
    mock_gateway.refund_payment.assert_not_called()