

# pytest
# pip install pytest

def test_should_check_authentication_error_for_post_api_if_client_not_authorized(client):
    response = client.get("/api/v1/user-posts")
    assert response.status_code == 403
    data = response.json
    assert data == {"error": "Not authorized"}


def test_should_check_post_api(client, user_headers):
    response = client.get(
        "/api/v1/user-posts",
        headers=user_headers
    )
    assert response.status_code == 200
    data = response.json
    assert data == {"post": []}