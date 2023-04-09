def test_should_check_create_comment_api(
        client,
        user_headers,
        create_post,
        send_data_for_create_comment_api):
    
    post_id = create_post
    response = client.post(
        f"/api/v1/create-comment/post/{post_id}",
        headers = user_headers,
        json = send_data_for_create_comment_api
    )
    assert response.status_code == 200
def test_should_check_wrong_post_id(
        client,
        user_headers,
        create_post,
        send_data_for_create_comment_api):
    
    post_id = create_post
    response = client.post(
        f"/api/v1/create-comment/post/0",
        headers = user_headers,
        json = send_data_for_create_comment_api
    )
    assert response.status_code == 404
def test_should_check_authentication_error_for_comment_api_if_client_not_authorized(
        client,
        user_headers,
        create_post,
        send_data_for_create_comment_api):
    
    post_id = create_post
    response = client.post(
        f"/api/v1/create-comment/post/0",
        json = send_data_for_create_comment_api
    )
    assert response.status_code == 403