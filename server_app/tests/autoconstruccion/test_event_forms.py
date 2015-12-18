import pytest


@pytest.fixture
def event_form(client):
    from autoconstruccion.web.forms import EventForm
    event = {
        'name': 'Pintar',
        'description': 'Hay que pintar las paredes de un 6 piso',
        'start_date': '24/12/2015'
    }
    return EventForm(data=event)


def test_event_valid_must_be_valid(event_form):
    assert event_form.validate()


def test_should_ok_when_name_has_3_letters(event_form):
    event_form.name.data = 'alv'
    assert event_form.name.validate(event_form)


def test_should_not_accept_when_there_no_name(event_form):
    event_form.name.data = ''
    assert not event_form.name.validate(event_form)


def test_should_ok_when_description_has_3_letters(event_form):
    event_form.description.data = 'des'
    assert event_form.description.validate(event_form)


def test_should_not_accept_when_there_no_description(event_form):
    event_form.description.data = ''
    assert not event_form.description.validate(event_form)
