

def test_register(test_client):
    response = test_client.post('/auth/register', json={
        'email': 'dead@pool.com',
        'password': 'chimichangas4life',
    })
    assert response.status_code == 201, (
        'User registration should return status code 201.'
    )
    data = response.json()
    keys = sorted(['id', 'email', 'is_active', 'is_superuser', 'is_verified'])
    assert sorted(list(data.keys())) == keys, (
        f'When registering a user, the response must contain keys `{keys}`.'
    )
    data.pop('id')
    assert data == {
        'email': 'dead@pool.com',
        'is_active': True,
        'is_superuser': False,
        'is_verified': False,
    }, 'When registering a user, the API response body is different than expected.'


def test_register_invalid_pass(user_client):
    response = user_client.post('/auth/register', json={
        'email': 'dead@pool.com',
        'password': '$',
    })
    assert response.status_code == 400, (
        'Incorrect user registration should return status code 400.'
    )
    data = response.json()
    assert list(data.keys()) == ['detail'], (
        'If the user registers incorrectly, the `detail` key should be in the response.'
    )
    assert data == {
        'detail': {
            'code': 'REGISTER_INVALID_PASSWORD',
            'reason': 'Password should be at least 3 characters',
        },
    }, 'When the user registers incorrectly, the body of the API response is different than expected.'
