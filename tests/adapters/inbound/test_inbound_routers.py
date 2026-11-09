"""Tests d'intégration de la couche entrante : DTO -> mappers -> réponse."""


def _create_festival(client):
    response = client.post(
        "/festivals",
        json={
            "name": "Hellforge Open Air",
            "location": "Clisson",
            "start_date": "2027-06-18T10:00:00",
            "end_date": "2027-06-20T23:00:00",
        },
    )
    assert response.status_code == 201
    return response.json()


def _create_artist(client):
    response = client.post(
        "/artists",
        json={
            "name": "Iron Vow",
            "genre": "Heavy metal",
            "required_equipment": ["large_rigging"],
        },
    )
    assert response.status_code == 201
    return response.json()


def _create_stage(client, festival_id):
    response = client.post(
        "/stages",
        json={
            "festival_id": festival_id,
            "name": "Mainstage",
            "capacity": 50000,
            "available_equipment": ["large_rigging", "special_lighting"],
        },
    )
    assert response.status_code == 201
    return response.json()


def test_inbound_flow_maps_dtos_and_orm_rows(client):
    festival = _create_festival(client)
    artist = _create_artist(client)
    stage = _create_stage(client, festival["id"])

    assert festival["status"] == "preparation"
    assert festival["start_date"].startswith("2027-06-18T10:00:00")
    assert artist["required_equipment"] == ["large_rigging"]
    assert stage["available_equipment"] == ["large_rigging", "special_lighting"]

    concert_response = client.post(
        "/concerts",
        json={
            "festival_id": festival["id"],
            "artist_id": artist["id"],
            "stage_id": stage["id"],
            "start_time": "2027-06-18T18:00:00",
            "end_time": "2027-06-18T19:30:00",
        },
    )
    assert concert_response.status_code == 201
    concert = concert_response.json()
    assert concert["status"] == "scheduled"
    assert concert["start_time"].startswith("2027-06-18T18:00:00")

    listed = client.get("/concerts", params={"festival_id": festival["id"]})
    assert listed.status_code == 200
    assert [item["id"] for item in listed.json()] == [concert["id"]]

    rescheduled = client.patch(
        f"/concerts/{concert['id']}/reschedule",
        json={
            "stage_id": stage["id"],
            "start_time": "2027-06-18T20:00:00",
            "end_time": "2027-06-18T21:00:00",
        },
    )
    assert rescheduled.status_code == 200
    assert rescheduled.json()["start_time"].startswith("2027-06-18T20:00:00")

    incident_response = client.post(
        "/incidents",
        json={
            "concert_id": concert["id"],
            "description": "Micro défectueux",
        },
    )
    assert incident_response.status_code == 201
    incident = incident_response.json()
    assert incident["resolved"] is False
    assert incident["occurred_at"] is not None

    incidents = client.get("/incidents", params={"concert_id": concert["id"]})
    assert incidents.status_code == 200
    assert [item["id"] for item in incidents.json()] == [incident["id"]]


def test_invalid_festival_range_is_mapped_to_400(client):
    response = client.post(
        "/festivals",
        json={
            "name": "Invalid Festival",
            "location": "Clisson",
            "start_date": "2027-06-20T10:00:00",
            "end_date": "2027-06-19T10:00:00",
        },
    )

    assert response.status_code == 400
    assert response.json()["type"] == "BAD_REQUEST"


def test_invalid_reschedule_range_is_mapped_to_400(client):
    festival = _create_festival(client)
    artist = _create_artist(client)
    stage = _create_stage(client, festival["id"])
    concert = client.post(
        "/concerts",
        json={
            "festival_id": festival["id"],
            "artist_id": artist["id"],
            "stage_id": stage["id"],
            "start_time": "2027-06-18T18:00:00",
            "end_time": "2027-06-18T19:30:00",
        },
    ).json()

    response = client.patch(
        f"/concerts/{concert['id']}/reschedule",
        json={
            "stage_id": stage["id"],
            "start_time": "2027-06-18T21:00:00",
            "end_time": "2027-06-18T20:00:00",
        },
    )

    assert response.status_code == 400
    assert response.json()["type"] == "BAD_REQUEST"


def test_unknown_concert_returns_404(client):
    assert client.get("/concerts/999").status_code == 404


def test_reschedule_unknown_concert_returns_404(client):
    response = client.patch(
        "/concerts/999/reschedule",
        json={
            "stage_id": 1,
            "start_time": "2027-06-18T20:00:00",
            "end_time": "2027-06-18T21:00:00",
        },
    )

    assert response.status_code == 404


def test_cancel_unknown_concert_returns_404(client):
    assert client.post("/concerts/999/cancel").status_code == 404
