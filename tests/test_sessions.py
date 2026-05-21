def test_create_session(client, auth_headers):
    response = client.post("/api/v1/sessions", json={"user_id": "user_1", "title": "First chat"}, headers=auth_headers)

    assert response.status_code == 201
    body = response.json()
    assert body["user_id"] == "user_1"
    assert body["title"] == "First chat"
    assert body["is_favorite"] is False
    assert "id" in body


def test_add_and_list_messages(client, auth_headers):
    session = client.post("/api/v1/sessions", json={"user_id": "user_1", "title": "RAG chat"}, headers=auth_headers).json()

    add_response = client.post(
        f"/api/v1/sessions/{session['id']}/messages",
        json={"sender": "USER", "content": "Explain my balance", "retrieved_context": {"source": "kb-1"}},
        headers=auth_headers,
    )

    assert add_response.status_code == 201

    list_response = client.get(f"/api/v1/sessions/{session['id']}/messages?limit=10&offset=0", headers=auth_headers)
    assert list_response.status_code == 200
    body = list_response.json()
    assert body["total"] == 1
    assert body["items"][0]["content"] == "Explain my balance"


def test_requires_api_key(client):
    response = client.post("/api/v1/sessions", json={"user_id": "user_1", "title": "No auth"})
    assert response.status_code == 401
