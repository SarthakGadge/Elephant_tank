import random
import datetime
from django.core.mail import send_mail
from django.utils import timezone
from django.db import connection
from django.conf import settings
import os


import base64

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        # Read the image and encode it to Base64
        encoded_image = base64.b64encode(img_file.read()).decode('utf-8')
    
    return encoded_image

#############################################################################################################################################################################################################################
#UserAuth

def generate_and_send_otp(user):
    otp = str(random.randint(1000, 9999))

    # Save OTP in the user model or OTP table
    user.otp = otp
    user.otp_expiry = timezone.now() + timezone.timedelta(minutes=10)
    user.max_otp_try -= 1
    if user.max_otp_try <= 0:
        user.otp_max_out = timezone.now() + timezone.timedelta(hours=1)
    else:
        user.max_otp_try -= 1
    user.save()

    subject = 'Verify Your Email'
    message = f'''
<html>
<body>
    <h2 style="color: #FF0000;">Verify Your Email</h2>
    <p>Dear {user.full_name},</p>
    
    <p>Welcome to Elephant Tank, Please <span style="color: #FF0000">verify OTP </span> for <span style="color: #FF0000">confirmation of registration </span></p>
    
    <p style="font-weight: bold; font-size: 18px;">OTP: <span style="color: #FF0000;">{otp}</span></p>

    <p style="color: #777;">Note: Do not share this OTP with anyone. If you did not register this account, please ignore this email.</p>
    
    <p>Thank you,<br/>
    The Elephant Tank Team.</p>
</body>
</html>
'''

    from_email = settings.EMAIL_HOST_USER
    to_email = [user.email]

    try:
        send_mail(subject, '', from_email, to_email,
                  fail_silently=False, html_message=message)
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

    return True

def mail_after_verifiation(stud_email):
    img_base64  = image_to_base64("userauth/static/images/Image.png")
    subject = 'Email Verified Successfully!'
    message = f'''
    <html>
    <body>
        <h2 style="color: #4A90E2;">Email Verification Successful!</h2>
        <p>Congratulations! Your email has been successfully verified. We will let you know when you access to login.</p>
        <p>Just a quick reminder: the event is scheduled for **31st January and 1st February 2024**. Please scan the QR code provided to access more details about the event.</p>
        
        <img src="data:image/png;base64,{img_base64}" alt="QR Code" style="width:200px;height:200px;" />
        
        <p>Warm regards,<br/>        
        <p>Warm regards,<br/>
        <strong>The Elephant Tank Team</strong></p>
    </body>
    </html>

    '''

    from_email = settings.EMAIL_HOST_USER
    to_email = [stud_email]

    try:
        send_mail(subject, '', from_email, to_email,
                  fail_silently=False, html_message=message)
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

    return True

def forgot_pass_mail(mail, otp):
    img_base64  = image_to_base64("userauth/static/images/Image.png")
    subject = 'Forgot Password'
    message = f'''
<html>
<body>
    <h2 style="color: #4A90E2;">Forgot Password OTP</h2>
    <p>You have requested to reset your password. Please use the OTP below to proceed with resetting your password:</p>
    <h3 style="color: #E94E77;">Your OTP: <strong>{otp}</strong></h3>
    <p>If you did not request this, please ignore this email or contact support immediately.</p>
    
    <p>Warm regards,<br/>
    <strong>The Elephant Tank Team</strong></p>
</body>
</html>
'''

    from_email = settings.EMAIL_HOST_USER
    to_email = [mail]

    try:
        send_mail(subject, '', from_email, to_email,
                  fail_silently=False, html_message=message)
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

    return True

def resend_otp(email, otp):
    subject = 'Forgot Password'
    message = f'''
<html>
<body>
    <h2 style="color: #4A90E2;">OTP</h2>
    <p>You have requested a new otp. Please use the OTP below to proceed with verification of your email:</p>
    <h3 style="color: #E94E77;">Your OTP: <strong>{otp}</strong></h3>
    <p>If you did not request this, please ignore this email or contact support immediately.</p>
    
    <p>Warm regards,<br/>
    <strong>The Elephant Tank Team</strong></p>
</body>
</html>
'''

    from_email = settings.EMAIL_HOST_USER
    to_email = [email]

    try:
        send_mail(subject, '', from_email, to_email,
                  fail_silently=False, html_message=message)
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

    return True

########################################################################################################################################################################################################################################################################################
#Mail about Funding and interested

def send_funding_email_to_student(investor_name, investor_email, stud_name, student_email, description=None, linkedin_url=None):
    subject = 'Interesed Investor'
    message = f'''
    <html>
    <body>
        <h2 style="color: #4A90E2;">Exciting News About Your Idea Submission!</h2>
        <p>Dear {stud_name},</p>
        
        <p>We are thrilled to inform you that your idea has captured the interest of an investor, <strong>{investor_name}</strong>. You can connect with them directly via email at <a href="mailto:{investor_email}">{investor_email}</a>.</p>
        
        {f'<p>Additionally, you can reach out to them on LinkedIn: <a href="{linkedin_url}" target="_blank">{linkedin_url}</a>.</p>' if linkedin_url else ''}

        {f'<p>Here’s a message from the investor:<br/><em>{description}</em></p>' if description else '<p>Details about the investment will be shared with you soon.</p>'}

        <p>We are proud of your achievement and wish you the very best as you take this exciting step forward. Keep innovating and inspiring!</p>

        <p>Warm regards,<br/>
        <strong>The Elephant Tank Team</strong></p>
    </body>
    </html>
    '''

    from_email = settings.EMAIL_HOST_USER
    to_email = [student_email]

    try:
        send_mail(subject, '', from_email, to_email,
                  fail_silently=False, html_message=message)
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

    return True


def send_funding_confirmation_to_investor(investor_name, investor_email, stud_name, student_email):
    subject = 'Verify Your Email'
    message = f'''
    <html>
    <body>
        <h2 style="color: #4A90E2;">Confirmation of Interest Notification</h2>
        <p>Dear {investor_name},</p>
        
        <p>We are pleased to inform you that the student, <strong>{stud_name}</strong>, has been successfully notified about your interest in their idea.</p>
        
        {f'<p>You can also connect with them directly on this email {student_email}'}
        
        <p>If you have any further queries or require assistance, feel free to reach out to us at any time.</p>

        <p>Thank you for your support in fostering innovation and empowering bright minds.<br/>
        <strong>The Elephant Tank Team</strong></p>
    </body>
    </html>
    '''

    from_email = settings.EMAIL_HOST_USER
    to_email = [investor_email]

    try:
        send_mail(subject, '', from_email, to_email,
                  fail_silently=False, html_message=message)
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

    return True

def send_funding_success_email_to_student(investor_name, investor_email, stud_name, student_email, description=None, linkedin_url=None):
    subject = 'Investor Funding Confirmation'
    message = f'''
    <html>
    <body>
        <h2 style="color: #4A90E2;">Great News! Your Idea Has Been Funded!</h2>
        <p>Dear {stud_name},</p>
        
        <p>We are excited to share that your idea has been officially funded by <strong>{investor_name}</strong>. You can reach out to them directly via email at <a href="mailto:{investor_email}">{investor_email}</a>.</p>
        
        {f'<p>Additionally, you can connect with them on LinkedIn: <a href="{linkedin_url}" target="_blank">{linkedin_url}</a>.</p>' if linkedin_url else ''}

        {f'<p>The investor has shared the following message with you:<br/><em>{description}</em></p>' if description else '<p>Details about the funding will be shared with you shortly.</p>'}

        <p>Congratulations on this incredible achievement! We hope this investment helps you bring your idea to life. Keep striving and innovating!</p>

        <p>Warm regards,<br/>
        <strong>The Elephant Tank Team</strong></p>
    </body>
    </html>
    '''

    from_email = settings.EMAIL_HOST_USER
    to_email = [student_email]

    try:
        send_mail(subject, '', from_email, to_email,
                  fail_silently=False, html_message=message)
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

    return True


def send_funding_confirmation_to_investor_about_funding(investor_name, investor_email, stud_name, student_email):
    subject = 'Funding Confirmation Successful'
    message = f'''
    <html>
    <body>
        <h2 style="color: #4A90E2;">Thank You for Your Investment!</h2>
        <p>Dear {investor_name},</p>
        
        <p>We are pleased to confirm that your funding for the student, <strong>{stud_name}</strong>, has been successfully communicated to them.</p>
        
        <p>You can connect with the student directly via their email: <a href="mailto:{student_email}">{student_email}</a>.</p>
        
        <p>If you have any additional requirements or inquiries, feel free to contact us anytime.</p>

        <p>Thank you for supporting and empowering innovation. Your investment truly makes a difference!</p>

        <p>Warm regards,<br/>
        <strong>The Elephant Tank Team</strong></p>
    </body>
    </html>
    '''

    from_email = settings.EMAIL_HOST_USER
    to_email = [investor_email]

    try:
        send_mail(subject, '', from_email, to_email,
                  fail_silently=False, html_message=message)
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

    return True

###########################################################################################################################################################################################################################################
# All admin approvals

def investor_mail_for_approval(investor_mail, investor_name):
    subject = 'Investor account approved'
    img_base64  = image_to_base64("userauth/static/images/Image.png")

    message = f'''
    <html>
    <body>
        <h2 style="color: #4A90E2;">Congratulations! Your Account has been approved by the admin</h2>
        <p>Dear {investor_name},</p>
        <p>We are glad to inform you that your Investor account have been approved and we will be delighted to have you for the event,<p>
        <p>just a reminder that the event is scheduled at 31 Jan and 1 Feb of 2024, Please scan the QR code to know more</p>
        
        <img src="data:image/png;base64,{img_base64}" alt="QR Code" style="width:200px;height:200px;" />
        
        <p>Warm regards,<br/>
        <strong>The Elephant Tank Team</strong></p>
    </body>
    </html>
    '''


    from_email = settings.EMAIL_HOST_USER
    to_email = [investor_mail]

    try:
        send_mail(subject, '', from_email, to_email,
                  fail_silently=False, html_message=message)
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

    return True

def approval_mail(stud_name, student_email):
    img_base64  = image_to_base64("userauth/static/images/Image.png")
    subject = 'Approval of Registration'
    message = f'''
    <html>
    <body>
        <h2 style="color: #4A90E2;">Your Registration has been approved!</h2>
        <p>Dear {stud_name},</p>
        <p>We are glad to inform you that your registration have been approved for the mail "{student_email}" and we will be delighted to have you for the event,<p>
        <p>just a reminder that the event is scheduled at 31 Jan and 1 Feb of 2024, Please scan the QR code to know more</p>
        <p>You can login to the website using this url : https://elephant-tank.com/Login1234567890/ or scan the QR code below.</p>
        
        <img src="data:image/png;base64,{img_base64}" alt="QR Code" style="width:200px;height:200px;" />
        
        <p>Warm regards,<br/>
        <strong>The Elephant Tank Team</strong></p>
    </body>
    </html>
    '''

    from_email = settings.EMAIL_HOST_USER
    to_email = [student_email]

    try:
        send_mail(subject, '', from_email, to_email,
                  fail_silently=False, html_message=message)
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

    return True


##

def project_approved(email, name):
    subject = 'Project approved'
    img_base64  = image_to_base64("userauth/static/images/Image.png")

    message = f'''
    <html>
    <body>
        <h2 style="color: #4A90E2;">Congratulations! Your Project has been approved by the admin</h2>
        <p>Dear {name},</p>
        <p>We are glad to inform you that your project have been approved and we will be delighted to have you for the event,<p>
        <p>just a reminder that the event is scheduled at 31 Jan and 1 Feb of 2024, Please scan the QR code to know more</p>
        
        <img src="data:image/png;base64,{img_base64}" alt="QR Code" style="width:200px;height:200px;" />
        
        <p>Warm regards,<br/>
        <strong>The Elephant Tank Team</strong></p>
    </body>
    </html>
    '''


    from_email = settings.EMAIL_HOST_USER
    to_email = [email]

    try:
        send_mail(subject, '', from_email, to_email,
                  fail_silently=False, html_message=message)
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

    return True
