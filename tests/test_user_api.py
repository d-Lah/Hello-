def test_should_check_registrate_user(
        client,
        send_data_for_user_api,):
    
    responce = client.post(
        "/api/v1/register-user",
        json = send_data_for_user_api)

    assert responce.status_code == 200

def test_should_check_error_required_fields_in_registrate_user(client):
    
    responce = client.post(
        "/api/v1/register-user")
    assert responce.status_code == 400

def test_should_check_error_exists_phone_number_in_user_api(
        client,
        send_data_with_exists_phone_number_for_use_api):

    responce = client.post(
    "/api/v1/register-user",
    json = send_data_with_exists_phone_number_for_use_api)

    assert responce.status_code == 400
def test_should_check_login_user(
        client,
        new_user,):
    
    data = {"phone_number": new_user.phone_number,
            "password": "password"}
    responce = client.post(
        "/api/v1/login",
        json = data)

    assert responce.status_code == 200
    

def test_should_check_authentication_error_for_user_api_if_client_not_authorized(
        client):
    
    response = client.get("/api/v1/user-info")
    assert response.status_code == 403
    data = response.json
    assert data == {"error": "Not authorized"}

def test_should_check_user_info(client, user_headers):
    responce = client.get(
        "/api/v1/user-info",
        headers = user_headers
    )
    assert responce.status_code == 200

def test_should_check_edit_user_info(
        client,
        user_headers,
        send_data_for_user_api):
    
    responce = client.put(
        "/api/v1/user-info/edit",
        headers = user_headers,
        json = send_data_for_user_api
    )
    assert responce.status_code == 200

def test_should_check_change_password(
        client,
        user_headers,
        send_data_for_change_password):
    
        responce = client.put(
        "/api/v1/user-info/change-password",
        headers = user_headers,
        json = send_data_for_change_password)

        assert responce.status_code == 200
def test_should_chech_error_old_password_in_change_password(
        client,
        user_headers,
        send_data_with_wrong_old_password_for_change_password):
     
        responce = client.put(
        "/api/v1/user-info/change-password",
        headers = user_headers,
        json = send_data_with_wrong_old_password_for_change_password)

        assert responce.status_code == 400