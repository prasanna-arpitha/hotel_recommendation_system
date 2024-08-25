import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
sender_email = 'nikhitharelangi22@gmail.com'  # Replace with your email address
sender_password = 'ovvc zaki yrcb iuip'  # Replace with your email password
smtp_server = 'smtp.gmail.com'
smtp_port = 587

def send_email_for_login(receiver_email):
    # Create message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'Hotel Recommendation'

    body = f'Hello,\n\nYou have successfully registered into this!!!!.\n\nBest regards'
    message.attach(MIMEText(body, 'plain'))
    
def send_email_for_updates(receiver_email):
    # Create message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'No more confusion'

    body = f'Hello,\n\nStuck up in choosing hotels.\nHere is the solution follow our updates for best experiences!!!\n\nBest regards'
    message.attach(MIMEText(body, 'plain'))

    # Send email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print(f'Email notification sent to {receiver_email} successfully!')
    except Exception as e:
        print(f'Error sending email: {e}')

def schedule_follow_up_notification(receiver_email, follow_up_time):
    time.sleep(follow_up_time)  # Wait for specified time
    send_email_for_updates(receiver_email)

if __name__ == '__main__':
    receiver_email = 'relangidhanalakshmi15@gmail.com'  # Enter the recipient's email address
    follow_up_time = 30  # Follow-up time in seconds (e.g., 1 hour = 3600 seconds)

    send_email_for_login(receiver_email)
    schedule_follow_up_notification(receiver_email, follow_up_time)
    send_email_for_updates(receiver_email)

def send_email_for_updates(receiver_email):
    # Create message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'No more confusion'

    body = f'Hello,\n\nStuck up in choosing hotels.\nHere is the solution follow our updates for best experiences!!!\n\nBest regards'
    message.attach(MIMEText(body, 'plain'))

    # Send email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print(f'Email notification sent to {receiver_email} successfully!')
    except Exception as e:
        print(f'Error sending email: {e}')


def schedule_follow_up_notification(receiver_email, follow_up_time):
    time.sleep(follow_up_time)  # Wait for specified time
    send_email_for_updates(receiver_email)


@app.route('/email', methods=['POST'])
def send_email():
    # Create message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = 'arpithalucky579@gmail.com'
    message['Subject'] = "We're Here to Help You Plan Your Perfect Stay!"
    receiver_email = 'arpithalucky579gmail.com'

    body = f"We hope this email finds you well!\nWe noticed that you recently used our hotel recommendation system to explore accommodation options. While you may not have booked a stay yet, we wanted to reach out and offer our assistance in planning your upcoming trip.\nOur team is here to help you find the perfect hotel that suits your preferences and needs. Whether you're looking for a cozy boutique hotel, a luxurious resort, or a budget-friendly option, we have a wide range of recommendations tailored to your requirements.\nIf you have any questions or need further assistance, please don't hesitate to reach out to us. We're committed to ensuring that your stay is nothing short of exceptional, and we're eager to help you every step of the way.\nThank you for considering us for your travel plans. We look forward to assisting you in creating a memorable experience.\nBest regards\nHotel Recommendation team"
    
    message.attach(MIMEText(body, 'plain'))

    # Send email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print(f'Email notification sent to {receiver_email} successfully!')
    except Exception as e:
        print(f'Error sending email: {e}')
@app.route('/verify_email', methods=['POST'])
def verify_email():
    data = request.json  # Get JSON data from the request
    email = data['email']
    verification_code = generate_verification_code()

    # Call your verification function here
    verification_code_sent = send_email_for_verification(email, verification_code)

    if verification_code_sent:
        response = jsonify({'success': True, 'message': 'Verification code sent successfully'})
        response.status_code = 200
    else:
        response = jsonify({'success': False, 'message': 'Failed to send verification code'})
        response.status_code = 500
    
    return response