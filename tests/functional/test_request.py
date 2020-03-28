def test_connection(test_client):
    response = test_client.get('/api/')
    assert response.status_code == 200
    assert b'{"message":"API is online!"}' in response.data
