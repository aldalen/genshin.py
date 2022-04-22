import genshin


async def test_record_cards(client: genshin.Client, hoyolab_uid: int):
    data = await client.get_record_cards(hoyolab_uid)

    assert data

    assert data[0].level >= 40


async def test_honkai_user(client: genshin.Client, honkai_uid: int):
    data = await client.get_honkai_user(honkai_uid)

    assert data


async def test_honkai_abyss(client: genshin.Client, honkai_uid: int):
    data = await client.get_honkai_abyss(honkai_uid)

    assert data is not None


async def test_elysian_realm(client: genshin.Client, honkai_uid: int):
    data = await client.get_elysian_realm(honkai_uid)

    assert data is not None


async def test_memorial_arena(client: genshin.Client, honkai_uid: int):
    data = await client.get_memorial_arena(honkai_uid)

    assert data is not None


async def test_full_honkai_user(client: genshin.Client, honkai_uid: int):
    data = await client.get_full_honkai_user(honkai_uid)

    assert data
