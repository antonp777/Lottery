from fastapi import APIRouter

from BOT.util.generateDataReport import generate_data_for_report
from app.Models.ModelsEnum import TransExpenseStatus, LotteryStatus
from app.Schemas.STransExpence import STransactionExpenseAdd
from app.dao.TransactionExpenceDAO import TransactionExpenceDAO

router = APIRouter(
    prefix="/transExpence",
    tags=["Транзакции Расхода"]
)


# Добавление транзакции
@router.post("")
async def add_trans_expence(trans_data: STransactionExpenseAdd):
    await TransactionExpenceDAO.add_model(sum=trans_data.sum,
                                          count_tickets=trans_data.count_tickets,
                                          status=trans_data.status,
                                          id_user=trans_data.id_user,
                                          id_card=trans_data.id_card)


# Добавление транзакции с ответом id
@router.post("/add")
async def add_trans_expence_with_id(data: STransactionExpenseAdd):
    return await TransactionExpenceDAO.add_trans_expence(sum=data.sum,
                                                         count_tickets=data.count_tickets,
                                                         status=data.status,
                                                         id_user=data.id_user,
                                                         id_lottery=data.id_lottery)

@router.post("/updateStatus")
async def update_status_trans_expence(id_trans: int, status: TransExpenseStatus):
    await TransactionExpenceDAO.update_model(model_id=id_trans, status=status)

@router.post("/updateStatusSumCountTicket")
async def update_status_sum_count_tickets_trans_expence(id_trans: int, status: TransExpenseStatus, sum: int, count_tickets: int):
    await TransactionExpenceDAO.update_model(model_id=id_trans, status=status, sum=sum, count_tickets=count_tickets)

@router.delete("")
async def delete_trans_expence(id_trans: int):
    await TransactionExpenceDAO.delete_model(model_id=id_trans)

@router.get("/report")
async def get_report_trans_expense(id_user: int):
    list_result = await TransactionExpenceDAO.get_all_trans_expenses_join_lottery(id_user)

    list_trans_expense = []
    for i in list_result:
        list_trans_expense.append(
            {'date': i[0].date.strftime('%d.%m.%Y %H:%M'), 'lottery': i[1], 'count_tickets': i[0].count_tickets,
             'sum': i[0].sum})

    return generate_data_for_report(list_trans_expense, 2)


# Выгрузка данных из БД для отчёта по активным или завершённым лотереями
@router.get("/report")
async def get_report_lottery_for_user(id_user: int, status: LotteryStatus):
    list_lotterys = await TransactionExpenceDAO.get_lottery_with_count_ticket_by_user(id_user)
    list_lottery = []
    for i in list_lotterys:
        if i['status'] == status:
            list_lottery.append({'name': i['name'], 'count_tickets': i['count_tickets']})

    return generate_data_for_report(list_lottery, 2)