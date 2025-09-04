from decimal import Decimal
from operator import or_
from sqlalchemy import func
from conf.db_session import create_session
from models.aditivo_nutritivo import AditivoNutritivo
from models.sabor import Sabor
from models.picole import Picole
from models.revendedor import Revendedor
from sqlalchemy import select, func
import asyncio


async def select_todos_aditivos_nutritivos() -> None:

    aditivos_nutritivos: list[AditivoNutritivo] | None = None

    async with create_session() as session:
        # Forma síncrona
        # aditivos_nutritivos = session.query(AditivoNutritivo).all()

        # Forma assíncrona
        query = select(AditivoNutritivo)
        result = await session.execute(query)
        aditivos_nutritivos = result.scalars().all()

    # return aditivos_nutritivos
    for aditivo in aditivos_nutritivos:
        print(aditivo.id)
        print(aditivo.nome)
        print(aditivo.formula_quimica + '\n')


async def select_sabor_by_id(id: int) -> None:
    sabor: Sabor | None = None

    async with create_session() as session:
        # sabor = session.query(Sabor).filter_by(id=id).one_or_none()
        result = await session.execute(select(Sabor).where(Sabor.id == id))
        sabor = result.scalar()

    print(sabor.nome)


async def select_picole_by_id(id: int) -> None:
    picole: Picole | None = None

    async with create_session() as session:
        # picole = session.query(Picole).filter_by(id=id).one_or_none()
        query = select(Picole).where(Picole.id == id)
        picole = (await session.execute(query)).scalar()

    if picole:
        print(f'ID: {picole.id}')
        print(f'Data_Criação: {picole.data_criacao}')
        print(f'Preço: {picole.preco}')
        print(f'Sabor: {picole.sabor.nome}')
        print(f'Embalagem: {picole.tipo_embalagem.nome}')
        print(f'Tipo: {picole.tipo_picole.nome}')
        print(f'Conservantes: {picole.conservantes}')
        print(f'Aditivos nutritivos: {picole.aditivos_nutritivos}')
        print(f'Ingredientes: {picole.ingredientes}')
    else:
        print(f'Picolé de ID = {id} não existe!')


async def select_group_by_picole() -> None:
    picoles: list[Picole] | None = None
    async with create_session() as session:
        # picoles: list[Picole] = session.query(Picole).group_by(
        #     Picole.id, Picole.id_tipo_picole).all()

        # query = select(Picole).join(Picole.sabor).group_by(
        #     Picole.id, Picole.id_tipo_picole)
        # result = await session.execute(query)
        # picoles = result.scalars().unique().all()

        query = select(Picole).group_by(
            Picole.id, Picole.id_tipo_picole)
        result = await session.execute(query)
        picoles = result.scalars().unique().all()

    if picoles:
        for picole in picoles:
            print(f'ID: {picole.id}')
            print(f'ID do tipo: {picole.id_tipo_picole}')
            print(f'Tipo Picolé: {picole.tipo_picole.nome}')
            print(f'Sabor: {picole.sabor.nome}\n')


async def select_sabores_limit() -> None:
    sabores: list[Sabor] | None = None
    async with create_session() as session:
        # sabores: list[Sabor] = session.query(
        #     Sabor).order_by(Sabor.id).limit(4).all()

        query = select(Sabor).order_by(Sabor.id).limit(4)
        result = await session.execute(query)
        sabores = result.scalars().unique().all()

        if sabores:
            for sabor in sabores:
                print(f'ID: {sabor.id}')
                print(f'Sabor: {sabor.nome}')
                print(f'Picolés: {sabor.picoles}\n')


async def select_revendedor_by_id(id_revendedor: int) -> None:
    async with create_session() as session:
        # revendedor: Revendedor | None = session.query(Revendedor).filter(
        #     Revendedor.id == id_revendedor).one_or_none()

        query = select(Revendedor).filter(Revendedor.id == id_revendedor)
        result = await session.execute(query)
        revendedor: Revendedor = result.scalar()

        if revendedor:
            print(f'ID revendedor: {revendedor.id}')
            print(f'Razão social: {revendedor.razao_social}')
            print(f'Contato: {revendedor.contato}')
            print(f'CNPJ: {revendedor.cnpj}\n')
        else:
            print(f'Não existe revendedor com ID = {id_revendedor}')


async def select_count_revendedor() -> None:
    quant_revendedores: int = 0

    async with create_session() as session:
        # revendedores = session.query(
        #     Revendedor).count()

        query = select(func.count(Revendedor.id))  # .select_from(Revendedor)
        result = await session.execute(query)
        quant_revendedores = result.scalar()
    print(f'Quantidade de revendedores: {quant_revendedores}')


async def select_agregacao() -> None:
    async with create_session() as session:
        # resultado: list[tuple[Decimal]] = session.query(
        #     func.sum(Picole.preco).label('soma'),
        #     func.avg(Picole.preco).label('media'),
        #     func.min(Picole.preco).label('mais_barato'),
        #     func.max(Picole.preco).label('mais_caro')
        # ).all()
        query = select(
            func.sum(Picole.preco).label('soma'),
            func.avg(Picole.preco).label('media'),
            func.min(Picole.preco).label('mais_barato'),
            func.max(Picole.preco).label('mais_caro')
        )

        resultado = await session.execute(query)
        agreg: list[tuple[Decimal]] = resultado.all()

        print(f'A soma: {agreg}')

        # print(f'A soma de todos os picolés é: {resultado[0][0]}')

        # for row in range(0, len(valores)):
        #     for valor in valores[row]:
        #         print(valor)

        # for valores in resultado:
        #     for valor in valores:
        #         print(valor)

        for row in agreg:
            for alias in row._mapping.keys():
                print(f'{alias}: {row._mapping[alias]}')


async def select_order_by_sabor() -> None:
    async with create_session() as session:
        query = select(Sabor).order_by(Sabor.data_criacao.desc())
        result = await session.execute(query)
        sabores: list[Sabor] = result.scalars().unique().all()

        if sabores:
            for sabor in sabores:
                print(f'ID sabor: {sabor.id}')
                print(f'Sabor: {sabor.nome}')
                print(f'Data criação: {sabor.data_criacao}\n')

if __name__ == '__main__':
    # asyncio.run(select_todos_aditivos_nutritivos())
    # asyncio.run(select_sabor_by_id(2))
    # asyncio.run(select_picole_by_id(id=13))
    # picole: Picole = select_picole_by_id(id=2)
    # asyncio.run(select_group_by_picole())
    # asyncio.run(select_sabores_limit())
    # asyncio.run(select_count_revendedor())
    asyncio.run(select_agregacao())
    # asyncio.run(select_revendedor_by_id(id_revendedor=4))
    # asyncio.run(select_order_by_sabor())

    # if picole:
    #     print(f'ID: {picole.id}')
    #     print(f'Data_Criação: {picole.data_criacao}')
    #     print(f'Preço: {picole.preco}')
    #     print(f'Sabor: {picole.sabor.nome}')
    #     print(f'Embalagem: {picole.tipo_embalagem.nome}')
    #     print(f'Tipo: {picole.tipo_picole.nome}')
    #     print(f'Conservantes: {picole.conservantes}')
    #     print(f'Aditivos nutritivos: {picole.aditivos_nutritivos}')
    #     print(
    #         f'Aditivos nutritivos: {[aditivo.nome for aditivo in picole.aditivos_nutritivos]}')
    #     print(f'Ingredientes: {picole.ingredientes}')
