import pytest
import httpx


BASE_URL = "http://localhost:8085"


def test_post_get_put():
    phone1 = "+7 (800) 123-45-67"
    phone2 = "+7 939 111 11 11"
    addr1 = "г. Москва, ул. Космонавтов, 15"
    addr2 = "г. Белгород, пр-кт Б. Хмельницкого, 153"

    # Удалить существующие записи

    # POST (успешно)
    r = httpx.post(f"{BASE_URL}/address", json={"phone": phone1, "address": addr1})
    assert r.status_code == 201

    # POST (уже существует)
    r = httpx.post(f"{BASE_URL}/address", json={"phone": phone1, "address": addr1})
    assert r.status_code == 400

    # GET (успешно)
    r = httpx.get(f"{BASE_URL}/address", params={"phone": phone1})
    assert r.status_code == 200
    assert r.json()["address"] == addr1

    # GET (неверные данные)
    r = httpx.get(f"{BASE_URL}/address", params={"phone": "12321"})
    assert r.status_code == 422

    # GET (не существует)
    r = httpx.get(f"{BASE_URL}/address", params={"phone": phone2})
    assert r.status_code == 404

    # PUT (успешно)
    r = httpx.put(f"{BASE_URL}/address", json={"phone": phone1, "address": addr2})
    assert r.status_code == 200

    # PUT (не существует)
    r = httpx.put(f"{BASE_URL}/address", json={"phone": phone2, "address": addr2})
    assert r.status_code == 404

    # PUT (не изменено)
    r = httpx.put(f"{BASE_URL}/address", json={"phone": phone1, "address": addr2})
    assert r.status_code == 400

    # GET (успешно)
    r = httpx.get(f"{BASE_URL}/address", params={"phone": phone1})
    assert r.status_code == 200
    assert r.json()["address"] == addr2

    # DELETE (не существует)
    r = httpx.delete(f"{BASE_URL}/address", params={"phone": phone2})
    assert r.status_code == 404

    # DELETE (успешно)
    r = httpx.delete(f"{BASE_URL}/address", params={"phone": phone1})
    assert r.status_code == 200

    httpx.delete(f"{BASE_URL}/address", params={"phone": phone2})
