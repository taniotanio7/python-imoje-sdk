import pytest
import re
import uuid
from datetime import datetime
import imoje_sdk


def transaction_callback(request, context):
    context.status_code = 200
    content = request.json()
    return {
        "transaction": {
            "id": str(uuid.uuid4()),
            "type": "sale",
            "status": "pending",
            "source": "api",
            "created": datetime.now().timestamp(),
            "modified": datetime.now().timestamp(),
            "notificationUrl": "",
            "serviceId": content["serviceId"],
            "amount": content["amount"],
            "currency": content["currency"],
            "title": content["title"],
            "orderId": content["orderId"],
            "paymentMethod": content["paymentMethod"],
            "paymentMethodCode": content["paymentMethodCode"],
        },
        "action": {
            "type": "redirect",
            "url": "https://login.ingbank.pl/mojeing/rest/rensetdirtrn",
            "method": "POST",
            "contentType": "application/x-www-form-urlencoded",
            "contentBodyRaw": ""
        }
    }


def test_creating_transaction(requests_mock):
    matcher = re.compile('^https://api.imoje.pl/v1/merchant/.+/transaction$')
    requests_mock.post(matcher, json=transaction_callback)
    api_client = imoje_sdk.Client("clientID",
                                  "clientSecret")
    customer = imoje_sdk.ClientDetails(first_name="Janusz", last_name="Januszowski", email="janusz@example.com")
    transaction = imoje_sdk.Transaction(amount=1, currency="PLN", order_id="test",
                                        store_id="some-random-store-number",
                                        payment_method=imoje_sdk.enums.PaymentMethod.ING,
                                        payment_method_details=imoje_sdk.enums.PayByLinkBank.ING,
                                        customer=customer, failure_return_url="http://example.com/payment_fail",
                                        success_return_url="http://example.com/success_fail")
    transaction.make_payment(api_client=api_client)
