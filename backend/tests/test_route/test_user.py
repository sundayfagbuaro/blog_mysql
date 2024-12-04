def test_create_user(client):
    data = {"email": "fife@bobosunne.com", "password":"supersecret"}
    response = client.post("/user/", json=data)
    assert response.status_code==201
    assert response.json()["email"]=="fife@bobosunne.com"
