def test_should_check_create_comment_api(
        client,
        user_headers,
        create_post,
        send_data_for_comment_api):
    
    _post = create_post
    response = client.post(
        f"/api/v1/create-comment/post/{_post.id}",
        headers = user_headers,
        json = send_data_for_comment_api
    )
    assert response.status_code == 200

def test_should_check_wrong_post_id(
        client,
        user_headers,
        create_post,
        send_data_for_comment_api):
    
    response = client.post(
        f"/api/v1/create-comment/post/0",
        headers = user_headers,
        json = send_data_for_comment_api
    )
    assert response.status_code == 404

def test_should_check_authentication_error_for_comment_api_if_client_not_authorized(
        client,
        user_headers,
        create_post,
        send_data_for_comment_api):
    
    _post = create_post
    response = client.post(
        f"/api/v1/create-comment/post/{_post.id}",
        json = send_data_for_comment_api
    )
    assert response.status_code == 403

def test_should_check_update_comment(
        client,
        user_headers,
        create_comment,
        send_data_for_comment_api):
    
    _comment = create_comment
    responce =client.put(
        f"/api/v1/update-comment/update/{_comment.id}",
        headers = user_headers,
        json = send_data_for_comment_api
    )
    assert responce.status_code == 200
    
def test_should_check_error_text_for_create_comment_and_update_comment(
        client,
        user_headers,
        create_post):

    _post = create_post
    responce = client.post(
        f"/api/v1/create-comment/post/{_post.id}",
        headers = user_headers
    )
    assert responce.status_code == 400

def test_should_check_wrong_comment_id(
        client,
        user_headers,
        send_data_for_comment_api):
    
    responce = client.put(
        "/api/v1/update-comment/update/0",
        headers = user_headers,
        json = send_data_for_comment_api
    )
    assert responce.status_code == 404

def test_should_check_delete_comment(
        client,
        user_headers,
        create_comment):
    
    _comment = create_comment
    responce = client.delete(
        f"/api/v1/delete-comment/delete/{_comment.id}",
        headers = user_headers
    )
    assert responce.status_code == 200