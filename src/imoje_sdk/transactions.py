from dataclasses import field, asdict
from typing import Union
import json

from marshmallow_dataclass import dataclass
from marshmallow import validate, Schema, post_dump

from imoje_sdk.enums import PaymentMethod, PayByLinkBank, PayByCardMethod, BlikMethod, TransactionStatus, \
    AllowedHTTPMetohds
from imoje_sdk.client import Client


class BaseSchema(Schema):
    @post_dump(pass_many=False)
    def remove_skip_values(self, data, **kwargs):
        data = {
            key: value for key, value in data.items()
            if value is not None and value != ""
        }
        return data


@dataclass(base_schema=BaseSchema)
class ClientDetails:
    """
    Customer details required to make the payment
    """
    first_name: str = field(metadata={"required": True, "data_key": "firstName", "validate": validate.Length(max=100)})
    last_name: str = field(metadata={"required": True, "data_key": "lastName", "validate": validate.Length(max=100)})
    email: str = field(metadata={"required": True, "validate": [validate.Length(max=200), validate.Email()]})
    client_id: str = field(default="", metadata={"data_key": "cid", "validate": [validate.Length(max=100)]})
    company: str = field(default="", metadata={"validate": [validate.Length(max=200)]})
    phone: str = field(default="", metadata={"validate": [validate.Length(max=20)]})


@dataclass(base_schema=BaseSchema)
class ClientAddress(ClientDetails):
    """
    Used to store data about clients' shipping and billing information
    """
    street: str = field(default="", metadata={"validate": [validate.Length(max=200)]})
    city: str = field(default="", metadata={"validate": [validate.Length(max=100)]})
    region: str = field(default="", metadata={"validate": [validate.Length(max=100)]})
    postal_code: str = field(default="", metadata={"data_key": "postalCode", "validate": [validate.Length(max=30)]})
    country_code: str = field(default="",
                              metadata={"data_key": "countryCodeAlpha2", "validate": [validate.Length(max=2)]})


@dataclass
class Action:
    type: str
    url: str
    method: str
    contentType: str
    contentBodyRaw: str


class Transaction:
    def __init__(self, amount: int, currency: str, store_id: str, order_id: str, payment_method: PaymentMethod,
                 payment_method_details: Union[PayByLinkBank, PayByCardMethod, BlikMethod], success_return_url: str,
                 failure_return_url: str, customer: ClientDetails, title="",
                 status=TransactionStatus.NOT_SEND, billing: ClientAddress = None,
                 shipping: ClientAddress = None, id: str = None):
        super().__init__()
        # Validating data
        assert len(currency) <= 3
        assert len(store_id) <= 36
        assert len(order_id) <= 100
        if title:
            assert len(title) <= 255
        if success_return_url:
            assert len(success_return_url) <= 300
        if failure_return_url:
            assert len(failure_return_url) <= 300
        if payment_method == payment_method.PAY_BY_LINK:
            assert isinstance(payment_method_details, PayByLinkBank)
        if payment_method == payment_method.CREDIT_CARD:
            assert isinstance(payment_method_details, PayByCardMethod)

        self.id = id
        self.amount = amount
        self.currency = currency
        self.store_id = store_id
        self.order_id = order_id
        self.title = title
        self.status = status
        self.payment_method = payment_method
        self.payment_method_details = payment_method_details
        self.success_return_url = success_return_url
        self.failure_return_url = failure_return_url
        self.customer = customer
        self.billing = billing
        self.shipping = shipping

    def asdict(self):
        customer = ClientDetails.Schema().dump(self.customer)
        billing = ClientAddress.Schema().dump(self.billing)
        shipping = ClientAddress.Schema().dump(self.shipping)
        dict = {
            "serviceId": self.store_id,
            "amount": self.amount,
            "currency": self.currency,
            "orderId": self.order_id,
            "title": self.title,
            "paymentMethod": self.payment_method.value,
            "paymentMethodCode": "" if self.payment_method_details is None else self.payment_method_details.value,
            "successReturnUrl": self.success_return_url,
            "failureReturnUrl": self.failure_return_url,
        }
        if customer:
            dict.update({"customer": customer})
        if billing:
            dict.update({"billing": billing})
        if shipping:
            dict.update({"shipping": shipping})

        return dict

    def make_payment(self, api_client: Client) -> Action:
        """
        Make the payment
        @param api_client: Client instance used to communicate with the imoje API
        @return: Action instance
        """
        if self.status is not TransactionStatus.NOT_SEND:
            raise Exception("Payment was already initialized")

        payload = {**self.asdict(), "type": "sale"}

        print("request")
        print(json.dumps(payload, indent=4, sort_keys=True))

        request = api_client.request(path="transaction", payload=payload)
        response = request.json()

        print("response")
        print(json.dumps(response, indent=4, sort_keys=True))

        request.raise_for_status()
        self.status = TransactionStatus(response["transaction"]["status"])
        self.id = response["transaction"]["id"]
        return Action(**response["action"])

    @staticmethod
    def return_payment(api_client: Client, amount: int, transaction_id: str, store_id) -> None:
        """
        Return the payment that was made by the client
        @param api_client: Client instance used to communicate with the imoje API
        @param amount: Specify an amount to return other than was made
        @return: None
        """
        payload = {
            "type": "refund",
            "serviceId": store_id,
            "amount": amount,
        }
        request = api_client.request(path=f"transaction/{transaction_id}/refund", payload=payload)
        request.raise_for_status()

    @classmethod
    def fetch(cls, api_client: Client, transaction_id: str):
        """
        Create the Transaction instance from the API data based on provided ID
        @param api_client: Client instance used to communicate with the imoje API
        @param transaction_id: Transaction ID to fetch data from
        @return: Transaction instance
        """
        request = api_client.request(path=f"transaction/{transaction_id}", payload={}, method=AllowedHTTPMetohds.GET)
        request.raise_for_status()
        transaction = request.json()["transaction"]

        payment_method = PaymentMethod(transaction["paymentMethod"])
        if payment_method is PaymentMethod.PAY_BY_LINK or payment_method is PaymentMethod.ING:
            payment_method_details = PayByLinkBank(transaction["paymentMethodCode"])
        elif payment_method is PaymentMethod.CREDIT_CARD:
            payment_method_details = PayByCardMethod(transaction["paymentMethodCode"])
        elif payment_method is PaymentMethod.BLIK:
            payment_method_details = BlikMethod.BLIK
        else:
            raise Exception("Received payment method is not supported")

        customer = ClientDetails.Schema().load(transaction["customer"])
        billing = ClientAddress.Schema().load(transaction["billing"])
        shipping = ClientAddress.Schema().load(transaction["shipping"])

        return cls(amount=transaction["amount"], currency=transaction["currency"], store_id=transaction["serviceId"],
                   order_id=transaction["orderId"], payment_method=payment_method,
                   payment_method_details=payment_method_details, success_return_url=transaction["notificationUrl"],
                   failure_return_url=transaction["notificationUrl"],
                   customer=customer, title=transaction["title"], status=TransactionStatus(transaction["status"]),
                   billing=billing, shipping=shipping, id=transaction_id)
