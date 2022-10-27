from datetime import datetime

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from app.models import CharityProject, Donation


async def add_free_donate(
        project_in: CharityProject,
        session: AsyncSession,
):
    all_donate = await session.execute(
        select(Donation).where(
            Donation.fully_invested == 0
        )
    )
    all_donate = all_donate.scalars().all()
    update_data = project_in.dict()
    if all_donate is not None:
        full_amount = update_data['full_amount']
        invested_amount = 0
        for donat in all_donate:
            full_donat = donat.full_amount
            invest_donat = donat.invested_amount
            if invested_amount < full_amount:
                if (full_donat - invest_donat) <= (full_amount - invested_amount):
                    invested_amount += (full_donat - invest_donat)
                    donat.fully_invested = True
                    donat.invested_amount = full_donat
                    donat.close_date = datetime.now()
                else:
                    donat.invested_amount = (full_amount - invested_amount)
                    invested_amount = full_amount
                    update_data['fully_invested'] = True
                    update_data['close_date'] = datetime.now()
                    break
            session.add(donat)
        update_data['invested_amount'] = invested_amount
    return update_data


async def add_donate_to_project(
        donat_in: Donation,
        session: AsyncSession,
):
    all_project = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested == 0
        )
    )
    all_project = all_project.scalars().all()
    update_data = donat_in.dict()
    if all_project is not None:
        full_amount = update_data['full_amount']
        invested_amount = 0
        for project in all_project:
            full_project = project.full_amount
            invest_project = project.invested_amount
            if invested_amount < full_amount:
                if (full_project - invest_project) <= (full_amount - invested_amount):
                    invested_amount += (full_project - invest_project)
                    project.fully_invested = True
                    project.invested_amount = full_project
                    project.close_date = datetime.now()
                else:
                    project.invested_amount += (full_amount - invested_amount)
                    invested_amount = full_amount
                    update_data['fully_invested'] = True
                    update_data['close_date'] = datetime.now()
                    break
            session.add(project)
        update_data['invested_amount'] = invested_amount
    return update_data
