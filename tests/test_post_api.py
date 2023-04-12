def test_should_check_authentication_error_for_post_api_if_client_not_authorized(client):
    response = client.get("/api/v1/user-posts")
    assert response.status_code == 403
    data = response.json
    assert data == {"error": "Not authorized"}

def test_should_check_user_post_api(client, user_headers):
    response = client.get(
        "/api/v1/user-posts",
        headers=user_headers
    )
    assert response.status_code == 200
    data = response.json
    assert data == {"post": []}

def test_should_check_create_post_api(
        client,
        user_headers,
        send_data_for_post_api):
    
    response = client.post(
        "/api/v1/create-post",
        headers=user_headers,
        json = send_data_for_post_api
    )
    assert response.status_code == 200

def test_should_check_error_title_or_body_for_create_post(
        client,
        user_headers):
    
    responce = client.post(
        "/api/v1/create-post",
        headers = user_headers,
        json = None
    )
    assert responce.status_code == 400

def test_should_check_update_post(
        client,
        user_headers,
        send_data_for_post_api,
        create_post):
    
    _post = create_post
    responce = client.put(
        f"/api/v1/update-post/update/{_post.id}",
        headers = user_headers,
        json = send_data_for_post_api
    )
    assert responce.status_code == 200

def test_should_check_wrong_post_id(
        client,
        user_headers):

    responce = client.get(
        "/api/v1/post-comments/post/0",
        headers = user_headers
    )
    assert responce.status_code == 404

def test_should_check_ppost_comment(
        client,
        user_headers,
        create_post):
    
    _post = create_post
    responce = client.get(
        f"/api/v1/post-comments/post/{_post.id}",
        headers = user_headers
    )
    assert responce.status_code == 200

def test_should_check_delete_post(
        client,
        user_headers,
        create_post):

    _post = create_post
    responce = client.delete(
        f"/api/v1/delete-post/delete/{_post.id}",
        headers = user_headers
    )
    assert responce.status_code == 200