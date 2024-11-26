from main import client
from fastapi import status
from src.tailors.schemas import TailorItem, TailorListItem


def test_get_tailors(access_token_user, access_token_tailor):
    res_u = client.get("/tailors", headers=access_token_user.get('header'))
    assert res_u.status_code == status.HTTP_200_OK
    assert isinstance(res_u.json(), list)
    TailorListItem.model_validate(res_u.json()[0])


def test_get_tailor(access_token_user, access_token_tailor):
    res_u = client.get(f"/tailors/{access_token_tailor.get('id')}",
                       headers=access_token_user.get('header'))
    assert res_u.status_code == status.HTTP_200_OK
    TailorItem.model_validate(res_u.json())


def test_update_tailor(access_token_tailor):
    res = client.put(f"/tailors/{access_token_tailor.get('id')}",
                     headers=access_token_tailor.get('header'),
                     json={'brand_name': 'Yomi casual'})
    assert res.status_code == status.HTTP_200_OK
    res = client.get(f"/tailors/{access_token_tailor.get('id')}",
                     headers=access_token_tailor.get('header'))

    assert res.json()['brand_name'] == 'Yomi casual'


def test_tailor_is_active(access_token_tailor, access_token_admin, update_data_t):
    res = client.get(f"/tailors/{access_token_tailor.get('id')}",
                     headers=access_token_tailor.get('header'))
    assert res.status_code == status.HTTP_200_OK
    assert res.json()['is_enabled'] == False

    res = client.put(f"/tailors/{access_token_tailor.get('id')}",
                     json=update_data_t,
                     headers=access_token_tailor.get('header'))
    assert res.status_code == status.HTTP_200_OK

    res = client.patch(f'/admin/tailors/{access_token_tailor.get("id")}/verify',
                       headers=access_token_admin.get('header'))
    assert res.status_code == status.HTTP_200_OK

    res = client.get(f"/tailors/{access_token_tailor.get('id')}",
                     headers=access_token_tailor.get('header'))
    assert res.status_code == status.HTTP_200_OK
    assert res.json()['is_enabled'] == True
