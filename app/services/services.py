from datetime import datetime

from sqlalchemy import select, not_
from sqlalchemy.ext.asyncio import AsyncSession


async def add_donate_to_project(
        upgrade_model,
        new,
        session: AsyncSession,
):
    """Функция распределения донатов по проектам"""
    all_upgrade = await session.execute(
        select(upgrade_model).where(
            not_(
                upgrade_model.fully_invested)
        )
    )
    all_upgrade = all_upgrade.scalars().all()
    update_data = new.dict()
    if all_upgrade is not None:
        full_new = update_data['full_amount']
        invest_new = 0
        for upgrade in all_upgrade:
            full_upgrade = upgrade.full_amount
            invested_upgrade = upgrade.invested_amount
            if invest_new < full_new:
                balance_upgrade = full_upgrade - invested_upgrade
                balance_new = full_new - invest_new
                if balance_upgrade <= balance_new:
                    invest_new += balance_upgrade
                    upgrade.fully_invested = True
                    upgrade.invested_amount = full_upgrade
                    upgrade.close_date = datetime.now()
                else:
                    upgrade.invested_amount += balance_new
                    invest_new = full_new
            session.add(upgrade)
            if full_new == invest_new:
                update_data['fully_invested'] = True
                update_data['close_date'] = datetime.now()
                update_data['invested_amount'] = invest_new
                break
    return update_data
