from Models.models import Admin
from Connections.connections import session,EMAIL,EMAIL_PASSWORD
import secrets
import requests
import smtplib
from hashing import Harsher
from jose import jwt
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


SECRET_KEY = "437125588a32a48932c07911f45df783d34379f0b866440da76960384c688ec97d5b4b6b07153d0a5f4276bb336134adf126613d5151627d09710c799ee98530"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def create_admin():
    db = session
    admin_username = await create_user_name()
    password = await create_password()
    hashed_password = Harsher.get_hash_password(password)
    admin = Admin(username=admin_username, password=hashed_password)
    try:
        db.add(admin)
        db.commit()
        db.refresh(admin)
        send_welcome_email(admin,password)
    except Exception as e:
        print(f"Error occurred: {e}")
        db.rollback()
    return {"username": admin_username, "password": password}


async def create_user_name():
    counter = 1
    letter_counter = 65  
    while True:
        admin_username = f"{chr(letter_counter)}{counter:03}@Animex.ug"
        counter += 1
        if counter > 999999:  
            counter = 1
            letter_counter += 1
            if letter_counter > 90: 
                letter_counter = 65

        return admin_username
    

async def create_password(length=8):
    password = secrets.token_hex(length)

    return password

def send_welcome_email(user_details,password):
    sender_email = EMAIL
    sender_password = EMAIL_PASSWORD

    reset_token = secrets.token_urlsafe(20)

    # Create the email
    msg = MIMEMultipart('related')
    msg['From'] = sender_email
    msg['To'] = user_details.email if hasattr(user_details, 'email') else user_details.Email
    msg['Subject'] = "Welcome to Animax UG"

    # Make name flexible for DoctorName and name
    # name = user_details.name if hasattr(user_details, 'name') else user_details.DoctorName

    # Make access number flexible for accessnumber, access_no, Accessnumber, AccessNumber
    access_no = user_details["username"]

    html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <center><img src="cid:company_logo" alt="Company Logo" style="width: 100px; height: auto; margin-bottom: 20px;"></center>
            <!-- <p>Dear ,<br><br> -->
            Welcome to Animax!<br><br>
            We are thrilled to have you join us in our mission to care for roaming dogs.<br> At Animax, we are dedicated to providing the best support and solutions for the welfare of these animals.<br>
            Please log in to your account using these credentials:<br>
            Username: <strong>{access_no}</strong><br>
            Password: <strong>{password}</strong><br><br>
            We encourage you to change your password after logging in for security reasons.<br>
            If you have any questions or need assistance, our dedicated support team is here to assist you.<br><br>
            Thank you for joining us in making a difference in the lives of roaming dogs. Your participation and support are invaluable to our cause.<br><br>
            Warm regards,<br>
            The Animax Team<br><br>
            Note: This is an automated message. Please do not reply to this email.</p>
        </body>
    </html>
    """

    msg.attach(MIMEText(html_body, 'html'))

    # firebase_url = 'https://firebasestorage.googleapis.com/v0/b/bfamproject-80d95.appspot.com/o/prod%2Fproducts%2F1705940735027_gen_visual.jpeg?alt=media&token=de7a990b-2238-455f-a6d2-1f0ba71f55d2'

    # response = requests.get(firebase_url)
    # if response.status_code == 200:
    #     img_data = response.content
    #     img = MIMEImage(img_data)
    #     img.add_header('Content-ID', '<company_logo>')
    #     msg.attach(img)
    # else:
    #     print("Failed to retrieve image from Firebase")

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    try:
        server.login(sender_email, sender_password)
    except smtplib.SMTPAuthenticationError:
        print("SMTP Authentication Error: The username or password you entered is not correct.")
        return

    server.send_message(msg)
    server.quit()

async def login(credentials):
    db = session
    username = credentials["username"]
    input_password = credentials["password"]
    admin = db.query(Admin).filter(Admin.username == username).first()

    if admin and Harsher.verify_password(input_password, admin.password):
        token_data = {"sub": username}
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        admin_data = Admin.get_admin(db)
        access_token = create_access_token(
            data=token_data, 
            expires_delta=access_token_expires
        )
        return {"data": admin_data,"access_token": access_token, "token_type": "bearer"}
    else:
        raise Exception("Invalid Username or Password")
