import pytest

from functional.testdata.parameters.film_params import FILM_BASE_PARAMS, \
    NONEXISTENT_FILM_ID, FILM_PARAMS


class TestFilmNotFoundWithoutData:

    @pytest.mark.parametrize(
        "query_parameters", [*FILM_PARAMS])
    @pytest.mark.asyncio
    async def test_films(self, make_get_request, query_parameters: dict):
        response = await make_get_request('/film')
        assert response.status == 404

    @pytest.mark.asyncio
    async def test_film_id(self, make_get_request):
        response = await make_get_request(
            f'/film/{NONEXISTENT_FILM_ID}')
        assert response.status == 404

    @pytest.mark.parametrize(
        "query_parameters", [*FILM_BASE_PARAMS])
    @pytest.mark.asyncio
    async def test_film_similar(self, make_get_request,
                                query_parameters: dict):
        response = await make_get_request(
            f'/film/{NONEXISTENT_FILM_ID}/similar')
        assert response.status == 404
