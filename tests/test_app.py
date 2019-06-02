import os
import random

import pytest
import pytz

from app import app, db
from config import TestConfig, test_base_dir
from app.service.user_actions import UserActions
from app.service.file_actions import FileActions
from app.service.admin_actions import AdminActions
from app.models import User, File


@pytest.fixture(scope="session", autouse=True)
def another_resource_setup_with_autouse(request):
    app.config.from_object(TestConfig)
    db.create_all()
    print('\nDB INITIALIZED')

    def resource_teardown():
        os.remove(f'{test_base_dir}/test_app.db')
        print('\nDB DELETED')
    request.addfinalizer(resource_teardown)


def test_change_password():
    user = User(username='TestChangePassword')
    user.set_password('test')
    db.session.add(user)
    db.session.commit()
    user = User.query.filter_by(username='TestChangePassword').first()
    old_password_hash = user.password_hash
    try:
        UserActions().change_password(user_id=user.id, old_password='test', new_password='TestChangePassword')
    except Exception:
        pass
    user = User.query.filter_by(username='TestChangePassword').first()
    assert(old_password_hash != user.password_hash)


def test_set_timezone():
    user = User(username='TestSetTimezone')
    db.session.add(user)
    db.session.commit()
    user = User.query.filter_by(username='TestSetTimezone').first()
    timezone = random.choice(pytz.common_timezones)
    try:
        UserActions().set_timezone(user_id=user.id, timezone=timezone)
    except Exception:
        pass
    user = User.query.filter_by(username='TestSetTimezone').first()
    assert(user.timezone == timezone.replace('-', '/'))


@pytest.mark.parametrize('status', [True, False])
def test_sharing(status):
    user = User(username=f'TestSharing{str(status)}')
    db.session.add(user)
    db.session.commit()
    user = User.query.filter_by(username=f'TestSharing{str(status)}').first()
    file = File(filename=f'TestSharing{str(status)}', user_id=user.id)
    db.session.add(file)
    db.session.commit()
    file = File.query.filter_by(filename=f'TestSharing{str(status)}').first()
    try:
        FileActions().sharing(user_id=user.id, file_id=file.id, share=status)
    except Exception:
        pass
    file = File.query.filter_by(filename=f'TestSharing{str(status)}').first()
    assert(file.is_shared == status)


def test__generate_sharelink():
    sharelink = AdminActions()._generate_sharelink()
    assert isinstance(sharelink, str)
    assert(len(sharelink) > 10)


def test_delete_user():
    user = User(username='TestDeleteUser')
    db.session.add(user)
    db.session.commit()
    user = User.query.filter_by(username='TestDeleteUser').first()
    try:
        AdminActions().delete_user(user.id)
    except Exception:
        pass
    deleted_user = User.query.filter_by(username='TestDeleteUser').first()
    assert not deleted_user
