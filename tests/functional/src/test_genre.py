import pytest

nonexistent_genre_id = '135c3882-129a-472d-8f3a-bf84014b6537'


class TestGenreNotFoundWithoutData:

    @pytest.mark.asyncio
    async def test_genre_id(self, make_get_request):
        response = await make_get_request(f'/genre/{nonexistent_genre_id}')
        assert response.status == 404

    @pytest.mark.asyncio
    async def test_genre(self, make_get_request):
        response = await make_get_request(f'/genre/')
        assert response.status == 404
