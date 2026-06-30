import csv
import io

from flask import jsonify, Response
from fpdf import FPDF


def success_response(data=None, message="success", status_code=200):
    payload = {"message": message}
    if data is not None:
        payload["data"] = data
    return jsonify(payload), status_code


def error_response(message="error", status_code=400):
    return jsonify({"error": message}), status_code


def rows_to_csv_response(rows, fieldnames, filename):
    """Build a Flask Response containing a CSV file download."""
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow({key: row.get(key, "") for key in fieldnames})

    response = Response(buffer.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response


def rows_to_pdf_response(title, rows, fieldnames, filename):
    """Build a Flask Response containing a simple tabular PDF download."""
    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, title, ln=True)
    pdf.set_font("Helvetica", "B", 9)

    page_width = pdf.w - 2 * pdf.l_margin
    col_width = page_width / max(len(fieldnames), 1)
    row_height = 7

    for field in fieldnames:
        pdf.cell(col_width, row_height, field.replace("_", " ").title(), border=1)
    pdf.ln(row_height)

    pdf.set_font("Helvetica", "", 9)
    for row in rows:
        for field in fieldnames:
            value = row.get(field, "")
            pdf.cell(col_width, row_height, str(value) if value is not None else "", border=1)
        pdf.ln(row_height)

    pdf_bytes = bytes(pdf.output(dest="S"))
    response = Response(pdf_bytes, mimetype="application/pdf")
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response


def parse_csv_upload(file_storage):
    """Parse an uploaded CSV file into a list of dict rows."""
    content = file_storage.read().decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(content))
    return [
        {(k.strip() if k else k): (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
        for row in reader
    ]