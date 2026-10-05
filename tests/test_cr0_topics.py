"""CR-0 · Tēma "Parki un skvēri" un tēmu saraksts.

Sagaidāmās vērtības ņemtas no tracker/CR-0.md pieņemšanas kritērijiem
un docs/openapi.yaml (GET /topics), nevis no koda.
"""

EXPECTED_TOPICS = [
    {"code": "ROADS", "name": "Ceļi un ielas"},
    {"code": "WASTE", "name": "Atkritumi"},
    {"code": "PLANNING", "name": "Teritorijas plānošana"},
    {"code": "PARKS", "name": "Parki un skvēri"},
    {"code": "OTHER", "name": "Cits"},
]

EXISTING_TOPICS = {
    "ROADS": "Ceļi un ielas",
    "WASTE": "Atkritumi",
    "PLANNING": "Teritorijas plānošana",
    "OTHER": "Cits",
}


def test_cr0_ac1_topics_list(client):
    response = client.get("/topics")

    assert response.status_code == 200
    # Precīzs saturs un secība; OTHER vienmēr beigās (precizējums 2026-10-01)
    assert response.json() == EXPECTED_TOPICS


def test_cr0_ac2_parks_submission_created(client, valid_payload):
    payload = {**valid_payload, "topic": "PARKS"}

    response = client.post("/submissions", json=payload)

    assert response.status_code == 201


def test_cr0_ac3_unknown_topic_rejected(client, valid_payload):
    payload = {**valid_payload, "topic": "ZOO"}

    response = client.post("/submissions", json=payload)

    assert response.status_code == 400
    error = response.json()["error"]
    assert error["code"] == "VALIDATION_ERROR"
    assert any(d["field"] == "topic" for d in error["details"])


def test_cr0_ac4_existing_topics_unchanged(client, valid_payload):
    response = client.get("/topics")
    assert response.status_code == 200
    by_code = {item["code"]: item["name"] for item in response.json()}

    for code, name in EXISTING_TOPICS.items():
        assert by_code.get(code) == name, f"Tēma {code} mainīta vai trūkst"
        created = client.post("/submissions", json={**valid_payload, "topic": code})
        assert created.status_code == 201, f"Tēma {code} vairs netiek pieņemta"
