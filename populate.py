from typing import List
from faker import Faker
from sqlalchemy import select

from conf.db_session import create_session
from models.aditivo_nutritivo import AditivoNutritivo
from models.conservante import Conservante
from models.ingrediente import Ingrediente
from models.picole import Picole
from models.revendedor import Revendedor
from models.sabor import Sabor
from models.tipo_embalagem import TipoEmbalagem
from models.tipo_picole import TipoPicole
from models.lote import Lote
from models.nota_fiscal import NotaFiscal

# Configuração do Faker
fake = Faker('pt_BR')


async def populate_aditivos_nutritivos(session):
    aditivos = [
        "Vitamina C", "Vitamina D", "Vitamina B12",
        "Ferro", "Cálcio", "Proteína", "Fibras"
    ]

    for nome in aditivos:
        aditivo = AditivoNutritivo(
            nome=nome,
            formula_quimica=fake.lexify(text="???-???-???")
        )
        session.add(aditivo)

    await session.commit()


async def populate_conservantes(session):
    conservantes = [
        "Sorbato de Potássio", "Benzoato de Sódio",
        "Ácido Cítrico", "Metabissulfito de Sódio", "Nitrito de Sódio"
    ]

    for nome in conservantes:
        conservante = Conservante(
            nome=nome,
            descricao=fake.text(max_nb_chars=45)
        )
        session.add(conservante)

    await session.commit()


async def populate_sabores(session):
    sabores = [
        "Morango", "Chocolate", "Baunilha", "Creme",
        "Napolitano", "Flocos", "Pistache"
    ]

    for nome in sabores:
        sabor = Sabor(nome=nome)
        session.add(sabor)

    await session.commit()


async def populate_ingredientes(session):
    ingredientes = [
        "Leite", "Açúcar", "Cacau", "Morango",
        "Água", "Creme de Leite", "Leite Condensado"
    ]

    for nome in ingredientes:
        ingrediente = Ingrediente(nome=nome)
        session.add(ingrediente)

    await session.commit()


async def populate_tipos_embalagem(session):
    tipos = [
        "Papel", "Plástico", "Papelão", "Plástico Reciclável"
    ]

    for nome in tipos:
        tipo = TipoEmbalagem(nome=nome)
        session.add(tipo)

    await session.commit()


async def populate_tipos_picole(session):
    tipos = [
        "Água", "Cremoso", "Frutas", "Premium"
    ]

    for nome in tipos:
        tipo = TipoPicole(nome=nome)
        session.add(tipo)

    await session.commit()


async def populate_revendedores(session):
    for _ in range(5):
        revendedor = Revendedor(
            cnpj=fake.cnpj(),
            razao_social=fake.company(),
            contato=fake.name()
        )
        session.add(revendedor)

    await session.commit()


async def populate_picoles(session):
    # Recuperar dados necessários
    stmt_sabores = select(Sabor)
    sabores = (await session.scalars(stmt_sabores)).unique().all()

    stmt_tipos = select(TipoPicole)
    tipos = (await session.scalars(stmt_tipos)).unique().all()

    stmt_embalagens = select(TipoEmbalagem)
    embalagens = (await session.scalars(stmt_embalagens)).unique().all()

    stmt_ingredientes = select(Ingrediente)
    ingredientes = (await session.scalars(stmt_ingredientes)).unique().all()

    stmt_conservantes = select(Conservante)
    conservantes = (await session.scalars(stmt_conservantes)).unique().all()

    stmt_aditivos = select(AditivoNutritivo)
    aditivos = (await session.scalars(stmt_aditivos)).unique().all()

    # Criar picolés
    for _ in range(10):
        picole = Picole(
            preco=fake.pyfloat(min_value=2, max_value=10, right_digits=2),
            id_sabor=fake.random_element(elements=sabores).id,
            id_tipo_picole=fake.random_element(elements=tipos).id,
            id_tipo_embalagem=fake.random_element(elements=embalagens).id,
        )

        # Adicionar ingredientes aleatórios
        for _ in range(fake.random_int(min=2, max=4)):
            picole.ingredientes.append(
                fake.random_element(elements=ingredientes))

        # Adicionar conservantes aleatórios
        for _ in range(fake.random_int(min=1, max=2)):
            picole.conservantes.append(
                fake.random_element(elements=conservantes))

        # Adicionar aditivos nutricionais aleatórios
        for _ in range(fake.random_int(min=1, max=3)):
            picole.aditivos_nutritivos.append(
                fake.random_element(elements=aditivos))

        session.add(picole)

    await session.commit()


async def populate_notas_fiscais_e_lotes(session):
    # Recuperar revendedores e tipos de picolés
    stmt_revendedores = select(Revendedor)
    revendedores = (await session.scalars(stmt_revendedores)).unique().all()

    stmt_tipos_picole = select(TipoPicole)
    tipos_picole = (await session.scalars(stmt_tipos_picole)).unique().all()

    # Criar notas fiscais e lotes
    for _ in range(5):
        revendedor = fake.random_element(elements=revendedores)
        nota = NotaFiscal(
            valor=fake.pyfloat(min_value=100, max_value=1000, right_digits=2),
            numero_serie=str(fake.unique.random_number(digits=8)),
            descricao=fake.text(max_nb_chars=100),
            id_revendedor=revendedor.id,
            data=fake.date_time_between(start_date='-2y', end_date='now')
        )
        session.add(nota)
        await session.flush()  # Para obter o ID da nota fiscal

        # Criar lotes para esta nota fiscal
        for _ in range(fake.random_int(min=1, max=3)):
            tipo_picole = fake.random_element(elements=tipos_picole)
            lote = Lote(
                id_tipo_picole=tipo_picole.id,
                quantidade=fake.random_int(min=100, max=500)
            )
            session.add(lote)
            await session.flush()  # Para obter o ID do lote

            # Relacionar lote com nota fiscal
            nota.lotes.append(lote)

    await session.commit()


async def main():
    async with create_session() as session:
        print("Populando banco de dados...")

        # Populando as tabelas em ordem
        await populate_aditivos_nutritivos(session)
        await populate_conservantes(session)
        await populate_sabores(session)
        await populate_ingredientes(session)
        await populate_tipos_embalagem(session)
        await populate_tipos_picole(session)
        await populate_revendedores(session)
        await populate_picoles(session)
        await populate_notas_fiscais_e_lotes(session)

        print("Banco de dados populado com sucesso!")

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
