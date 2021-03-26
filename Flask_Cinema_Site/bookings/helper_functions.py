from Flask_Cinema_Site.models import Transaction, User, Viewing

from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

import os
from datetime import datetime

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def create_pdf(transaction, email_address):
    user = transaction.user
    viewing = transaction.viewings[0]
    movie = viewing.movie

    count = 0
    data_array = []

    data_array.append(["Email address", "Date", "Movie", "Seats"])

    for seat in transaction.seats:
        if count == 0:
            data_array.append([str(user.email), str(transaction.datetime), str(movie.name),
                              str(seat.seat_number)])
        else:
            data_array.append(["", "", "", str(seat.seat_number)])
        count = count + 1

    vat = viewing.price * 0.2

    data_array.append(["Sub total", "", "", str(viewing.price)])
    data_array.append(["VAT", "", "", str(vat)])
    data_array.append(["Total", "", "", str(viewing.price + vat)])

    dir = os.getcwd()
    path = os.path.join(dir, "Flask_Cinema_Site", "bookings", "receipts", "receipt.pdf")

    pdf = SimpleDocTemplate(path, pagesize=A4)
    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    title_style.alignment = 1
    title = Paragraph("MovieBox receipt", title_style)

    style = TableStyle(
        [
            ("BOX", (0, 0), (-1, -1), 1, colors.black),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BACKGROUND", (0, 0), (-1, -1), colors.gray),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ]
    )

    table = Table(data_array, style=style)
    pdf.build([title, table])
    send_pdf(path, email_address)


def send_pdf(path, email):
    from_addr = "alan.ashford.786123@gmail.com"
    toaddr = str(email)
    today_date = datetime.now()

    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = toaddr
    msg['Subject'] = "MovieBox receipt"

    body = "Please see your MovieBox receipt attached for the "\
        + "transaction which occured on: " + str(today_date)\
        + "."
    msg.attach(MIMEText(body, 'plain'))

    filename = "receipt.pdf"
    attachment = open(path, "rb")

    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(from_addr, "Laughing522")
    text = msg.as_string()
    s.sendmail(from_addr, toaddr, text)
    s.quit()

    attachment.close()
    os.remove(path)
