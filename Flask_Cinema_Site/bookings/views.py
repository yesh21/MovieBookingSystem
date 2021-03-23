from flask import render_template, redirect, Blueprint, flash, request
from flask_login import current_user

from Flask_Cinema_Site.bookings.forms import PaymentForm
from Flask_Cinema_Site.helper_functions import get_redirect_url, send_email
from Flask_Cinema_Site.models import Movie, Viewing, User, Transaction, Seat
from Flask_Cinema_Site import db

import json
from datetime import datetime

from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

import os

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


bookings_blueprint = Blueprint(
    'bookings', __name__,
    template_folder='templates',
    static_folder='static'
)

# Global Variables to keep track of current booking
# Probably a better way to do this
seats = None
m = None
v = None


# Will show movie, brief details and row of times for each day
# Once selected will redirect to seats
@bookings_blueprint.route('/slot', methods=['GET'])
def view_specific():
    movie_id = request.args.get('movie', None)
    viewing_id = request.args.get('viewing', None)

    global m, v

    m = Movie.query.get(movie_id)
    v = Viewing.query.get(viewing_id)
    if not m:
        flash(f'Movie with id [{movie_id}] not found', 'danger')
        return redirect(get_redirect_url())

    if not v:
        flash(f'Viewing with id [{viewing_id}] not found', 'danger')
        return redirect(get_redirect_url())

    # viewings = Viewing.query.filter_by(movie_id=m.id).all()
    return render_template('select_time.html', title=m.name, movie=m, times=v)


# Stores currently selected seats.
@bookings_blueprint.route("/slot/seats", methods=['POST'])
def seat_book():
    global seats
    seats = json.loads(request.data)

    # Add seats to the database

    return json.dumps({'status': 'OK'})


@bookings_blueprint.route("/pay", methods=['GET', 'POST'])
def payment():
    payment_form = PaymentForm()
    if payment_form.validate_on_submit():
        for seat in seats:
            double_booking = User.query.join(Transaction)\
                .filter(User.id == Transaction.user_id).join(Seat)\
                .filter(Transaction.id == Seat.transaction_id)\
                .filter(Seat.seat_number == seat).join(Viewing)\
                .filter(Seat.viewing_id == Viewing.id).first()
    # .filter(Viewing.time == v.time).first() PROBLEM WHEN ADDING TIME COMPARISON

            if double_booking:
                flash("Double booking detected!")
                return redirect(get_redirect_url())
        movie = Movie.query.filter(Movie.name == m.name).first()
        viewing = Viewing.query.filter(Viewing.movie_id == movie.id).first()
        current_date = datetime.now()

        transaction = Transaction(user_id=current_user.id, datetime=current_date)
        transaction.viewings.append(viewing)
        for seat in seats:
            seating = Seat.query.filter(seat == Seat.seat_number).first()
            transaction.seats.append(seating)
        db.session.add(transaction)
        db.session.commit()

        create_pdf(transaction.id, current_user.id, movie)
        flash("Thank you for booking with us, confirmation email will arrive soon!")
        return redirect(get_redirect_url())

    return render_template('payment.html', seats=seats, title=m.name, times=v, form=payment_form)


def create_pdf(trans_id, user_id, movie):
    transaction = Transaction.query.filter(Transaction.id == trans_id).first()
    user = User.query.filter(User.id == user_id).first()
    viewing = Viewing.query.filter(Viewing.movie_id == movie.id).first()
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
    send_pdf(path, user.email)


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
