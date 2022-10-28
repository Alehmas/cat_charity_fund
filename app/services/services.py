from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def add_free_donate(
        project_in: CharityProject,
        session: AsyncSession,
):
    """Функция распределения свободных донатов при
    создании проекта"""
    all_donate = await session.execute(
        select(Donation).where(
            Donation.fully_invested == 0
        )
    )
    all_donate = all_donate.scalars().all()
    update_data = project_in.dict()
    if all_donate is not None:
        full_project = update_data['full_amount']
        invested_project = 0
        for donat in all_donate:
            full_donat = donat.full_amount
            invest_donat = donat.invested_amount
            if invested_project < full_project:
                balance_project = full_project - invested_project
                balance_donat = full_donat - invest_donat
                if balance_donat <= balance_project:
                    invested_project += balance_donat
                    donat.fully_invested = True
                    donat.invested_amount = full_donat
                    donat.close_date = datetime.now()
                    session.add(donat)
                    if balance_donat == balance_project:
                        update_data['fully_invested'] = True
                        update_data['close_date'] = datetime.now()
                        session.add(donat)
                        break
                else:
                    donat.invested_amount += balance_project
                    invested_project = full_project
                    update_data['fully_invested'] = True
                    update_data['close_date'] = datetime.now()
                    break
            session.add(donat)
        update_data['invested_amount'] = invested_project
    return update_data


async def add_donate_to_project(
        donat_in: Donation,
        session: AsyncSession,
):
    """Функция распределения нового доната по незакрытым проектам"""
    all_project = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested == 0
        )
    )
    all_project = all_project.scalars().all()
    update_data = donat_in.dict()
    if all_project is not None:
        full_donat = update_data['full_amount']
        invest_donat = 0
        for project in all_project:
            full_project = project.full_amount
            invested_project = project.invested_amount
            if invest_donat < full_donat:
                balance_project = full_project - invested_project
                balance_donat = full_donat - invest_donat
                if balance_project <= balance_donat:
                    invest_donat += balance_project
                    project.fully_invested = True
                    project.invested_amount = full_project
                    project.close_date = datetime.now()
                    if balance_project == balance_donat:
                        update_data['fully_invested'] = True
                        update_data['close_date'] = datetime.now()
                        session.add(project)
                        break
                else:
                    project.invested_amount += balance_donat
                    invest_donat = full_donat
                    update_data['fully_invested'] = True
                    update_data['close_date'] = datetime.now()
                    break
            session.add(project)
        update_data['invested_amount'] = invest_donat
    return update_data
