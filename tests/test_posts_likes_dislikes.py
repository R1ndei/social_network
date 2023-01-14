import pytest
import json


@pytest.mark.asyncio()
async def test_create_post(login_user, async_client):
    headers = {'Authorization': login_user}
    payload: dict = {"head": "test_pytest", "main_text": "test_pytest"}
    response = await async_client.post("/api/v1/post", headers=headers, data=payload)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json['status'] == 200


@pytest.mark.asyncio()
async def test_create_second_post(login_user_without_posts, async_client):
    headers = {'Authorization': login_user_without_posts}
    payload: dict = {"head": "test_pytest2", "main_text": "test_pytest2"}
    response = await async_client.post("/api/v1/post", headers=headers, data=payload)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json['status'] == 200


@pytest.mark.asyncio()
async def test_get_all_posts(login_user, async_client):
    headers = {'Authorization': login_user}
    params = {"with_user_posts": True}
    response = await async_client.get("/api/v1/post", headers=headers, params=params)
    response_json = response.json()
    assert response.status_code == 200


@pytest.mark.asyncio()
async def test_update_post(login_user, async_client):
    headers = {'Authorization': login_user}
    payload: dict = {"head": "test_update", "main_text": "test_update"}
    response = await async_client.put("/api/v1/post/1", headers=headers, json=payload)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json['detail'] == "Updated successfully"


@pytest.mark.asyncio()
async def test_like_own_post(login_user, async_client):
    headers = {'Authorization': login_user}
    response = await async_client.post("/api/v1/like/1", headers=headers)
    response_json = response.json()
    assert response.status_code == 400
    assert response_json['detail'] == "You can't like own posts"


@pytest.mark.asyncio()
async def test_like_post(login_user_without_posts, async_client):
    headers = {'Authorization': login_user_without_posts}
    response = await async_client.post("/api/v1/like/1", headers=headers)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json['detail'] == "Liked successfully"


@pytest.mark.asyncio()
async def test_like_not_exist_post(login_user_without_posts, async_client):
    headers = {'Authorization': login_user_without_posts}
    response = await async_client.post("/api/v1/like/12", headers=headers)
    response_json = response.json()
    assert response.status_code == 400
    assert response_json['detail'] == "Post with current id doesn't exist"


@pytest.mark.asyncio()
async def test_get_own_likes(login_user_without_posts, async_client):
    headers = {'Authorization': login_user_without_posts}
    response = await async_client.get("/api/v1/like", headers=headers)
    response_json = response.json()
    assert response.status_code == 200
    assert len(response_json) == 1


@pytest.mark.asyncio()
async def test_delete_own_like(login_user_without_posts, async_client):
    headers = {'Authorization': login_user_without_posts}
    response = await async_client.delete("/api/v1/like/1", headers=headers)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json['detail'] == "Like removed successfully"


@pytest.mark.asyncio()
async def test_get_own_likes_after_delete(login_user_without_posts, async_client):
    headers = {'Authorization': login_user_without_posts}
    response = await async_client.get("/api/v1/like", headers=headers)
    response_json = response.json()
    assert response.status_code == 200
    assert len(response_json) == 0


@pytest.mark.asyncio()
async def test_dislike_post(login_user, async_client):
    headers = {'Authorization': login_user}
    response = await async_client.post("/api/v1/dislike/2", headers=headers)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json['detail'] == "Dislike created successfully"


@pytest.mark.asyncio()
async def test_like_disliked_post(login_user, async_client):
    headers = {'Authorization': login_user}
    response = await async_client.post("/api/v1/like/2", headers=headers)
    count_dislikes = await async_client.get("/api/v1/dislike", headers=headers)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json['detail'] == "Liked successfully"
    assert len(count_dislikes.json()) == 0


@pytest.mark.asyncio()
async def test_delete_post(login_user, async_client):
    headers = {'Authorization': login_user}
    payload: dict = {"head": "test_update", "main_text": "test_update"}
    response_delete = await async_client.delete("/api/v1/post/1", headers=headers)
    params = {"with_user_posts": True}
    response_get = await async_client.get("/api/v1/post", headers=headers, params=params)
    response_json = response_get.json()
    assert response_delete.status_code == 200
    assert response_get.status_code == 200


@pytest.mark.asyncio()
async def test_create_post_without_login(login_user, async_client):
    payload: dict = {"head": "test_pytest", "main_text": "test_pytest"}
    response = await async_client.post("/api/v1/post", data=payload)
    response_json = response.json()
    assert response.status_code == 401
