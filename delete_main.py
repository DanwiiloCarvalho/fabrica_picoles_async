from sqlalchemy import Result, select
from models.picole import Picole
from models.revendedor import Revendedor
from conf.db_session import create_session
from select_main import select_picole_by_id, select_revendedor_by_id
import asyncio


async def delete_picole_by_id(id_picole: int) -> None:

    async with create_session() as session:
        query = select(Picole).filter(Picole.id == id_picole)
        result: Result = await session.execute(query)
        picole: Picole | None = result.unique().scalar_one_or_none()

        if picole:
            await session.delete(picole)
            await session.commit()
        else:
            print(f'Picolé de ID = {id_picole} não existe')


async def delete_revendedor_by_id(id_revendedor: int):
    async with create_session() as session:
        query = select(Revendedor).filter(Revendedor.id == id_revendedor)
        result: Result = await session.execute(query)
        revendedor: Revendedor | None = result.unique().scalar_one_or_none()

        if revendedor:
            await session.delete(revendedor)
            await session.commit()
        else:
            print(f'Não existe revendedor com ID = {id_revendedor}')


async def main_delete_picole():
    print('Antes da deleção')
    await select_picole_by_id(13)
    await delete_picole_by_id(13)

    print('Após a deleção')
    await select_picole_by_id(13)


async def main_delete_revendedor():
    print('Antes da deleção')
    await select_revendedor_by_id(id_revendedor=1)
    await delete_revendedor_by_id(id_revendedor=1)

    print('Após a deleção')
    await select_revendedor_by_id(id_revendedor=1)

if __name__ == '__main__':
    # asyncio.run(main_delete_picole())
    asyncio.run(main_delete_revendedor())
