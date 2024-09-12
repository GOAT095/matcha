import pytest
from app import app  # Import your Flask app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
#normal post test
def test_add_user_success(client):
    response = client.post('/add_user', json={
        "gender": "Male",
        "sexual_preferences": "Heterosexual",
        "biography": "Software engineer who loves hiking",
        "interests": ["hiking", "photography", "coding"],
        "profile_picture": "profile_pic.jpg",
        "pictures": ["pic1.jpg", "pic2.jpg", "pic3.jpg"]
    })
    assert response.status_code == 201
    assert response.get_json() == {"message": "User added successfully!"}
#test with a lot of pics
def test_add_user_too_many_pictures(client):
    response = client.post('/add_user', json={
        "gender": "Female",
        "sexual_preferences": "Bisexual",
        "biography": "Loves travel and adventure",
        "interests": ["travel", "photography"],
        "profile_picture": "profile_pic.jpg",
        "pictures": ["pic1.jpg", "pic2.jpg", "pic3.jpg", "pic4.jpg", "pic5.jpg", "pic6.jpg"]
    })
    assert response.status_code == 400
    assert response.get_json() == {"error": "You can upload up to 5 pictures"}
