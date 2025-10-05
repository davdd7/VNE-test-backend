from app.models.products import Product


def test_create_product(db_session, client):
    data = {
        "name":"Item4",
        "price":6000,
        "description":"descriprion some",
        "category_name":"Cat2",
        "sizes":[
            {"size_name": "M"},
            {"size_name": "L", "quantity": 5}
        ]
    }

    response = client.post("/products", json=data)
    assert response.get_json()["result"] == True

    product = db_session.get(Product, 1)

    assert product.name == "Item4"