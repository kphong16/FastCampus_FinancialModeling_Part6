from connector import Connector

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