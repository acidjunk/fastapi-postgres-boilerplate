from http import HTTPStatus


def test_users_get_multi_admin(test_client, superuser_token_headers):
    response = test_client.get("/api/users", headers=superuser_token_headers)
    assert HTTPStatus.OK == response.status_code
    users = response.json()

    assert 1 == len(users)


def test_users_get_multi_non_admin(test_client, user_token_headers):
    response = test_client.get("/api/users", headers=user_token_headers)
    assert HTTPStatus.FORBIDDEN == response.status_code
