# API Documentation

## Create Order

### Endpoint

**POST** `http://localhost:8000/orders`

### Request Body

The request body should be a JSON object containing the following fields:


- `type` (string): The type of the order. Accepted values: "limit" & "market"
  - Example: `"market"`
- `side` (string): The side of the order. Accepted value: "buy" & "sell"
  - Example: `"sell"`
- `instrument` (string): The instrument identifier.
  - Example: `"XRPUSDT00006"`
- `quantity` (integer): The quantity of the order.
  - Example: `500`
- `limit_price` (float): The limit price for the order. This field is optional and only applicable for limit orders.
  - Example: `100.0`


**Example Request:**


```JSON
{
    "type": "market",
    "side": "sell",
    "instrument": "XRPUSDT00006",
    "quantity": 500
}
```

### Success Response
```JSON
{
    "data": {
        "id": "ea290e7b-420d-4610-90f1-f1c2c752339a",
        "type": "market",
        "side": "sell",
        "instrument": "XRPUSDT00006",
        "limit_price": null,
        "quantity": 500
    },
    "success": true,
    "version": "0.0"
}
```

### Error Response
400 Error:
```JSON
{
    "error": {
        "message": "Invalid Input"
    },
    "success": false,
    "version": "0.0"
}
```
500 Error:
```JSON
{
    "error": {
        "message": "Invalid order placement"
    },
    "success": false,
    "version": "0.0"
}
```
