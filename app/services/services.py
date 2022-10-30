from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def add_donate_to_project(
        upgrade_model,
        new,
        # donat_in: Donation,
        session: AsyncSession,
):
    """Функция распределения донатов по проектам"""
    all_upgrade = await session.execute(
        select(upgrade_model).where(
            upgrade_model.fully_invested == 0
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
                    if balance_upgrade == balance_new:
                        update_data['fully_invested'] = True
                        update_data['close_date'] = datetime.now()
                        session.add(upgrade)
                        break
                else:
                    upgrade.invested_amount += balance_new
                    invest_new = full_new
                    update_data['fully_invested'] = True
                    update_data['close_date'] = datetime.now()
                    break
            session.add(upgrade)
        update_data['invested_amount'] = invest_new
    return update_data
