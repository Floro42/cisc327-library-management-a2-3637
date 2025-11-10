import pytest

from unittest.mock import (
    Mock, patch
)

from services.payment_service  import PaymentGateway
from services.library_service import (
    pay_late_fees, refund_late_fee_payment
)


def test_pay_late_fee_successful(mocker):

    mocker.patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": 7.00, "days_overdue": 3})
    mocker.patch("services.library_service.get_book_by_id", return_value={"title": "Sample"})

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, "txn_123", "Success")
    success, msg, txn = pay_late_fees("123456", 1, mock_gateway)

    mock_gateway.process_payment.assert_called_once()
    mock_gateway.process_payment.assert_called_with(patron_id='123456', amount=7.0, description="Late fees for 'Sample'")

    assert success == True
    assert "successful" in msg.lower()
    assert "txn_" in txn.lower()




def test_pay_late_fee_declined_by_gateway(mocker):

    mocker.patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": 10.00, "days_overdue": 3})
    mocker.patch("services.library_service.get_book_by_id", return_value={"title": "Sample"})

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (False, "", "Payment declined: amount exceeds limit")
    success, msg, txn = pay_late_fees("123456", 1, mock_gateway)

    assert success == False
    assert "failed" in msg.lower()
    assert txn is None

    #mock_gateway.process_payment.assert_called_once()
    #mock_gateway.process_payment.assert_called_with("123456", 10.00, "Late fees for 'Sample'")


    



def test_pay_late_fee_invalid_id():
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, "txn_123", "Success")
    success, msg, txn = pay_late_fees("123456789", 1, mock_gateway)

    mock_gateway.process_payment.assert_not_called()

    assert success == False
    assert "invalid" in msg.lower()
    assert txn is None




def test_pay_late_fee_zero_late_fees(mocker):
    mocker.patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": 0, "days_overdue": 0})
    mocker.patch("services.library_service.get_book_by_id", return_value={"title": "Sample"})

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, "txn_123", "Success")
    success, msg, txn = pay_late_fees("123456", 1, mock_gateway)

    mock_gateway.process_payment.assert_not_called()

    assert success == False
    assert "no late" in msg.lower()
    assert txn is None





def test_pay_late_fee_network_error_exception(mocker):
    mocker.patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": 2.00, "days_overdue": 1})
    mocker.patch("services.library_service.get_book_by_id", return_value={"title": "Sample"})

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (Exception)
    success, msg, txn = pay_late_fees("123456", 1, mock_gateway)

    assert success == False
    assert "error" in msg.lower()
    assert txn is None



def test_pay_late_fee_no_fee_amount(mocker):
    mocker.patch("services.library_service.calculate_late_fee_for_book", return_value=None)
    mocker.patch("services.library_service.get_book_by_id", return_value={"title": "Sample"})

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (Exception)
    success, msg, txn = pay_late_fees("123456", 1, mock_gateway)

    assert success == False
    assert "unable" in msg.lower()
    assert txn is None



def test_pay_late_fee_network_no_book(mocker):
    mocker.patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": 2.00, "days_overdue": 1})
    mocker.patch("services.library_service.get_book_by_id", return_value=None)

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (Exception)
    success, msg, txn = pay_late_fees("123456", 1, mock_gateway)

    assert success == False
    assert "not found" in msg.lower()
    assert txn is None











def test_refund_late_fee_payment_successful_refund():
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (True, "Refund of $7.00 processed successfully. Refund ID: txn_1234")
    success, message = refund_late_fee_payment("txn_123", 7.00, mock_gateway)

    assert success == True
    assert "refund of" in message.lower()

    mock_gateway.refund_payment.assert_called_once()
    mock_gateway.refund_payment.assert_called_with("txn_123", 7.00)



def test_refund_late_fee_payment_invalid_transaction_ID():
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (False, "Invalid transaction ID")
    success, message = refund_late_fee_payment("wrong ID", 7.00, mock_gateway)

    assert success == False
    assert "invalid" in message.lower()

    mock_gateway.refund_payment.assert_not_called()



def test_refund_late_fee_payment_invalid_refund_amount():
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (False, "Invalid refund amount")
    success, message = refund_late_fee_payment("txn_123", -1.00, mock_gateway)

    assert success == False
    assert "greater than" in message.lower()
    
    mock_gateway.refund_payment.assert_not_called()



def test_refund_late_fee_payment_invalid_refund_amount_higher():
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (False, "Invalid refund amount")
    success, message = refund_late_fee_payment("txn_123", 16.00, mock_gateway)

    assert success == False
    assert "exceeds" in message.lower()
    
    mock_gateway.refund_payment.assert_not_called()



def test_refund_late_fee_payment_failed_payment():
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (False, "Invalid refund amount")
    success, message = refund_late_fee_payment("txn_123", 7.00, mock_gateway)

    assert success == False
    assert "failed" in message.lower()




def test_refund_late_fee_payment_exception():
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (Exception)
    success, message = refund_late_fee_payment("txn_123", 7.00, mock_gateway)

    assert success == False
    assert "error" in message.lower()
    
    mock_gateway.refund_payment.assert_called_once()
