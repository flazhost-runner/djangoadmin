import pytest
from core.helpers import paginate, ci_like, remove_empty_fields, add_or_update_query_param


def test_remove_empty_fields():
    result = remove_empty_fields({'a': 1, 'b': '', 'c': None, 'd': 'value'})
    assert result == {'a': 1, 'd': 'value'}


def test_add_or_update_query_param():
    url = '/admin/v1/access/user/?q_page=1&q_name=test'
    result = add_or_update_query_param(url, 'q_page', 2)
    assert 'q_page=2' in result
    assert 'q_name=test' in result


@pytest.mark.django_db
def test_paginate():
    from apps.access.models import User
    qs = User.objects.all()
    result = paginate(qs, {'q_page': 1, 'q_page_size': 10})
    assert 'datas' in result
    assert 'paginate_data' in result
    assert result['paginate_data']['current_page'] == 1
