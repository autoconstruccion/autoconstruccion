

def test_home_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200


def test_projects_page_loads(client):
    response = client.get('/projects')
    assert response.status_code == 200


def test_users_page_loads(client):
    response = client.get('/users')
    assert response.status_code in [302, 200, 403]

