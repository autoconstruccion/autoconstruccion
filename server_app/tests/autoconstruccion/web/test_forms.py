import pytest


############################################################
# ----- Test ProjectForm -----
############################################################


# creates a fixture that returns a valid form
@pytest.fixture()
def project_form(request_ctx):
    """
    Returns a Project Form with valid data populated.
    """
    from autoconstruccion.web.forms import ProjectForm
    values = {'name': "Proyecto de testing",
              'description': "Este es un proyecto de prueba para test",
              'start_date': "24-01-2015",
              'end_date': "24-02-2015",
              'location': "Prueba a ver si lo encuentras",
              'contact_phone': "987654321",
              'image': None
              }
    return ProjectForm(data=values)


def test_get_valid_project_form(project_form):
    validity = project_form.validate()
    assert validity


def test_should_throw_exception_when_is_empty(project_form):
    from autoconstruccion.web.forms import ProjectForm
    fixture = {}
    project = ProjectForm(data=fixture)
    assert not project.validate()


# ------ Test name field
def test_should_fail_if_name_is_empty_none(project_form):
    project_form.name.data = None
    assert not project_form.validate()


def test_should_fail_if_name_is_empty_string(project_form):
    project_form.name.data = ''
    assert not project_form.validate()
    # test if error message appears
    assert 'name' in project_form.errors


def test_should_be_ok_when_name_has_5_chars(project_form):
    project_form.name.data = 'Peter'
    assert project_form.name.validate(project_form)


def test_should_fail_if_name_has_less_than_3_chars(project_form):
    project_form.name.data = 'Dr'
    assert not project_form.validate()
    assert 'name' in project_form.errors


def test_should_fail_if_name_has_more_than_255_chars(project_form):
    project_form.name.data = 'D'*256
    assert not project_form.validate()
    assert 'name' in project_form.errors


# ------ Test description field
def test_should_fail_if_description_is_empty_none(project_form):
    project_form.description.data = None
    assert not project_form.validate()


def test_should_fail_if_description_is_empty_string(project_form):
    project_form.description.data = ''
    assert not project_form.validate()
    assert 'description' in project_form.errors


def test_should_accept_description_greater_than_5(project_form):
    project_form.description.data = 'description'
    assert project_form.validate()


def test_should_fail_if_description_has_less_than_5_characters(project_form):
    project_form.description.data = 'desc'
    assert not project_form.validate()


def test_should_have_a_start_date_field(project_form):
    assert project_form.start_date


def test_should_have_a_end_date_field(project_form):
    assert project_form.end_date


def test_should_have_a_location_field(project_form):
    assert project_form.location


def test_should_have_an_image_field(project_form):
    assert project_form.image


def test_should_accept_jpg_images(project_form):
    project_form.image.data = '/folder/image.jpg'
    assert project_form.validate()



############################################################
# ----- Test UserForm -----
############################################################

# creates a fixture that returns a valid form
@pytest.fixture()
def user_form(request_ctx):
    """
    Returns a Project Form with valid data populated.
    """
    from autoconstruccion.web.forms import UserForm
    values = {'full_name': "Pepe Pérez Mengano",
              'email': "pepe.perez@fulano.es",
              'password': "123456",
              'phone_number': "654321987",
              'abilities': "Hago de todo..",
              'availability': "24/7",
              'tools': "",
              'materials': "",
              'is_admin': False,
              }
    return UserForm(data=values)


def test_get_valid_user_form(user_form):
    validity = user_form.validate()
    assert validity


def test_should_fail_if_full_name_is_empty_none(user_form):
    user_form.full_name.data = None
    assert not user_form.validate()


def test_should_fail_if_full_name_is_empty_string(user_form):
    user_form.full_name.data = ''
    assert not user_form.validate()


def test_should_fail_if_full_name_is_less_than_3_chars(user_form):
    user_form.full_name.data = 'ab'
    assert not user_form.validate()


def test_should_fail_if_full_name_is_greater_than_255_chars(user_form):
    user_form.full_name.data = 'a'*256
    assert not user_form.validate()


def test_should_fail_if_email_is_empty_none(user_form):
    user_form.email.data = None
    assert not user_form.validate()


def test_should_fail_if_email_is_empty_string(user_form):
    user_form.email.data = ''
    assert not user_form.validate()


def test_should_fail_with_a_not_valid_email(user_form):
    user_form.email.data = "fulanazo"
    assert not user_form.validate()
    user_form.email.data = "fulanazo@yo"
    assert not user_form.validate()


def test_should_have_a_abilities_field(user_form):
    assert user_form.abilities


def test_should_have_a_availability_field(user_form):
    assert user_form.availability


def test_should_have_a_tools_field(user_form):
    assert user_form.tools


def test_should_have_a_materials_field(user_form):
    assert user_form.materials


if __name__ == '__main__':
    pytest.main()

############################################################
# ----- Test SkillForm -----
############################################################


# creates a fixture that returns a valid form
@pytest.fixture()
def skill_form(client):
    """
    Returns a Project Form with valid data populated.
    """
    from autoconstruccion.web.forms import SkillForm
    values = {'name': "Cocinar",
              'description': "Saber cocinar",
              'image': None,
              }
    return SkillForm(data=values)


def test_get_valid_skill_form(skill_form):
    validity = skill_form.validate()
    assert validity


def test_skill_should_fail_if_full_name_is_empty_none(skill_form):
    skill_form.name.data = None
    assert not skill_form.validate()


def test_skill_should_fail_if_full_name_is_empty_string(skill_form):
    skill_form.name.data = ''
    assert not skill_form.validate()


def test_skill_should_fail_if_full_name_is_less_than_3_chars(skill_form):
    skill_form.name.data = 'ab'
    assert not skill_form.validate()


def test_skill_should_fail_if_full_name_is_greater_than_255_chars(skill_form):
    skill_form.name.data = 'a'*256
    assert not skill_form.validate()


def test_skill_should_fail_if_description_is_empty_none(skill_form):
    skill_form.description.data = None
    assert not skill_form.validate()


def test_skill_should_accept_description_greater_than_5(skill_form):
    skill_form.description.data = 'description'
    assert skill_form.validate()


def test_skill_should_fail_if_description_has_less_than_5_characters(skill_form):
    skill_form.description.data = 'desc'
    assert not skill_form.validate()

if __name__ == '__main__':
    pytest.main()
