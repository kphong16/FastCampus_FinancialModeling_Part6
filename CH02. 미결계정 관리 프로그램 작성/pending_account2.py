from connector import Connector
import pandas as pd

class TransactionManager:
    def create(
            self, account_name, client_name, transaction_date, 
            amount_receivable, amount_payable, settlement_status, 
            notes
        ):
        with Connector() as db:
            query = """
                INSERT INTO transaction_records 
                    (account_name, client_name, transaction_date, 
                    amount_receivable, amount_payable, 
                    settlement_status, notes) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            db.cursor.execute(
                query, 
                (account_name, client_name, transaction_date, 
                    amount_receivable, amount_payable, 
                    settlement_status, notes
                )
            )
            db.connection.commit()
            return db.cursor.lastrowid

    def read_all(self):
        with Connector() as db:
            query = "SELECT * FROM transaction_records"
            db.cursor.execute(query)
            return db.cursor.fetchall()

    def read(self, transaction_id):
        with Connector() as db:
            query = "SELECT * FROM transaction_records WHERE id = %s"
            db.cursor.execute(query, (transaction_id,))
            return db.cursor.fetchone()

    def update(
            self, transaction_id, account_name, client_name, 
            transaction_date, amount_receivable, 
            amount_payable, settlement_status, notes
        ):
        with Connector() as db:
            query = """
                UPDATE transaction_records 
                SET account_name = %s, client_name = %s, 
                    transaction_date = %s, amount_receivable = %s,
                    amount_payable = %s, settlement_status = %s,
                    notes = %s 
                WHERE id = %s
            """
            db.cursor.execute(
                query, 
                (account_name, client_name, transaction_date, 
                    amount_receivable, amount_payable, 
                    settlement_status, notes, transaction_id
                )
            )
            db.connection.commit()

    def delete(self, transaction_id):
        with Connector() as db:
            query = "DELETE FROM transaction_records WHERE id = %s"
            db.cursor.execute(query, (transaction_id,))
            db.connection.commit()


class CashflowManager:
    def create(
            self, transaction_id, dw_date, deposit_amount, 
            withdrawal_amount, notes
        ):
        with Connector() as db:
            query = """
                INSERT INTO cashflow_records 
                    (transaction_id, dw_date, deposit_amount, 
                    withdrawal_amount, notes) 
                VALUES (%s, %s, %s, %s, %s)
            """
            db.cursor.execute(
                query, 
                (transaction_id, dw_date, deposit_amount, 
                withdrawal_amount, notes)
            )
            db.connection.commit()
            return db.cursor.lastrowid

    def read_all(self):
        with Connector() as db:
            query = "SELECT * FROM cashflow_records"
            db.cursor.execute(query)
            return db.cursor.fetchall()

    def read(self, cashflow_id):
        with Connector() as db:
            query = "SELECT * FROM cashflow_records WHERE id = %s"
            db.cursor.execute(query, (cashflow_id,))
            return db.cursor.fetchone()

    def update(
            self, cashflow_id, transaction_id, dw_date, 
            deposit_amount, withdrawal_amount, notes
        ):
        with Connector() as db:
            query = """
                UPDATE cashflow_records 
                SET transaction_id = %s, dw_date = %s, 
                    deposit_amount = %s, withdrawal_amount = %s, 
                    notes = %s 
                WHERE id = %s
            """
            db.cursor.execute(
                query, 
                (transaction_id, dw_date, deposit_amount, 
                withdrawal_amount, notes, cashflow_id)
            )
            db.connection.commit()

    def delete(self, cashflow_id):
        with Connector() as db:
            query = "DELETE FROM cashflow_records WHERE id = %s"
            db.cursor.execute(query, (cashflow_id,))
            db.connection.commit()


class ReportingManager:
    def pending_report(self):
        with Connector() as db:
            query = "SELECT * FROM transaction_records"
            db.cursor.execute(query)
            tmdf = pd.DataFrame(db.cursor.fetchall())

            query = "SELECT * FROM cashflow_records"
            db.cursor.execute(query)
            cmdf = pd.DataFrame(db.cursor.fetchall())

        # 받은 금액을 계산
        amount_received = cmdf.groupby('transaction_id')[
                'deposit_amount'
            ].sum().reset_index()
        amount_received.columns = ['id', 'amount_received']

        # 거래 DataFrame에 받은 금액을 병합
        result_df = tmdf.merge(amount_received, on='id', how='left')

        # 지급된 금액을 계산
        amount_paid = cmdf.groupby('transaction_id')[
                'withdrawal_amount'
            ].sum().reset_index()
        amount_paid.columns = ['id', 'amount_paid']

        # 거래 DataFrame에 지급된 금액을 병합
        result_df = result_df.merge(amount_paid, on='id', how='left')

        # 결산된 금액 계산
        result_df['amount_received'] = result_df[
                'amount_received'
            ].fillna(0).astype(int)
        result_df['amount_paid'] = result_df[
                'amount_paid'
            ].fillna(0).astype(int)

        # 미수/미지급 잔액 계산
        result_df['receivable_remained'] = (
                result_df['amount_receivable'] - result_df['amount_received']
            )
        result_df['payable_remained'] = (
                result_df['amount_payable'] - result_df['amount_paid']
            )

        # 원하는 컬럼 순서로 재배열
        result_df = result_df[[
                'id', 'account_name', 'client_name', 'transaction_date', 
                'amount_receivable', 'amount_received', 'receivable_remained', 
                'amount_payable', 'amount_paid', 'payable_remained', 
                'settlement_status', 'notes'
            ]]

        # settlement_status 설정
        for idx in result_df.index:
            if result_df.loc[idx, 'receivable_remained'] > 0:
                result_df.loc[idx, 'settlement_status'] = '미수'
            elif result_df.loc[idx, 'payable_remained'] > 0:
                result_df.loc[idx, 'settlement_status'] = '미지급'
            else:
                result_df.loc[idx, 'settlement_status'] = '완료'

        return result_df