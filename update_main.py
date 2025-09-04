from decimal import Decimal

from sqlalchemy import select
from models.sabor import Sabor
from models.picole import Picole

from conf.db_session import create_session
from select_main import select_sabor_by_id, select_picole_by_id
import asyncio


async def update_sabor_by_id(sabor_id: int, nome_sabor: str) -> None:
    async with create_session() as session:
        query = select(Sabor).filter(Sabor.id == sabor_id)
        sabor: Sabor | None = (await session.execute(query)).unique().scalar_one_or_none()

        if sabor:
            sabor.nome = nome_sabor
            await session.commit()
            await session.refresh(sabor)
        else:
            print(f'Não existe sabor com ID = {sabor_id}')


async def update_picole_by_id(picole_id: int, preco: Decimal, id_sabor: int = None) -> None:
    async with create_session() as session:
        query = select(Picole).filter(Picole.id == picole_id)
        result = await session.execute(query)
        picole: Picole = result.unique().scalar_one_or_none()

        if picole:
            picole.preco = preco
            if id_sabor:
                picole.id_sabor = id_sabor

            await session.commit()
        else:
            print(f'Não existe picolé com ID = {picole_id}')


async def update_sabor():
    print('Antes da atualização')
    await select_sabor_by_id(id=8)
    print('Após atualização')
    await update_sabor_by_id(sabor_id=8, nome_sabor='Jabuticaba')
    await select_sabor_by_id(id=8)


async def update_picole():
    print('Antes da atualização')
    await select_picole_by_id(id=10)
    print('Após atualização')
    await update_picole_by_id(picole_id=10, preco=10.50, id_sabor=7)
    await select_picole_by_id(id=10)


if __name__ == '__main__':
    # print('Antes da atualização')
    # asyncio.run(select_sabor_by_id(id=8))
    # print('Após atualização')
    # asyncio.run(update_sabor_by_id(sabor_id=8, nome_sabor='Jabuticaba'))
    # asyncio.run(select_sabor_by_id(id=8))

    # asyncio.run(update_sabor())
    asyncio.run(update_picole())

    # print('Antes da atualização')
    # select_picole_by_id(id=10)
    # print('Após atualização')
    # update_picole_by_id(picole_id=10, preco=10.50, id_sabor=7)
    # select_picole_by_id(id=10)
