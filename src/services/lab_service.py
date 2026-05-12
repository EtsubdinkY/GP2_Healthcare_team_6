from src.config.database import get_connection


class LabService:
    def get_labs_by_patient(self, patient_id):
        query = """
            SELECT
                lo.order_id,
                lo.order_date,
                lo.priority,
                lo.status,
                lt.test_name,
                lt.test_code,
                lr.value,
                lr.unit,
                lr.abnormal_flag,
                lr.result_date
            FROM lab_order lo
            JOIN appointment a ON lo.appt_id = a.appt_id
            JOIN lab_order_item loi ON lo.order_id = loi.order_id
            JOIN lab_test lt ON loi.test_id = lt.test_id
            LEFT JOIN lab_result lr ON loi.order_item_id = lr.order_item_id
            WHERE a.patient_id = %s
            ORDER BY lo.order_date DESC
            LIMIT 10;
        """

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (patient_id,))
                rows = cur.fetchall()

        labs = []
        for row in rows:
            labs.append({
                "order_id": row["order_id"],
                "order_date": row["order_date"],
                "priority": row["priority"],
                "status": row["status"],
                "test_name": row["test_name"],
                "test_code": row["test_code"],
                "value": row["value"],
                "unit": row["unit"],
                "abnormal_flag": row["abnormal_flag"],
                "result_date": row["result_date"],
            })

        return labs