import random
import datetime
from django.core.mail import send_mail
from django.utils import timezone
from django.db import connection
from django.conf import settings
from django.core.mail import EmailMessage
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
        
        <p>Thank you,<br/>
    The Elephant Tank Team.</p>
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
    
    <p>Thank you,<br/>
    The Elephant Tank Team.</p>
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
    
    <p>Thank you,<br/>
    The Elephant Tank Team.</p>
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
#Interested Email

def email_of_interest_student(investor_name, investor_email, stud_name, student_email, description=None, linkedin_url=None):
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

        <p>Thank you,<br/>
    The Elephant Tank Team.</p>
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


def email_interst_investor(investor_name, investor_email, stud_name, student_email):
    subject = 'Interest Intimation'
    message = f'''
    <html>
    <body>
        <h2 style="color: #4A90E2;">Confirmation of Interest Notification</h2>
        <p>Dear {investor_name},</p>
        
        <p>We are pleased to inform you that the student, <strong>{stud_name}</strong>, has been successfully notified about your interest in their idea.</p>
        
        {f'<p>You can also connect with them directly on this email {student_email}'}
        
        <p>If you have any further queries or require assistance, feel free to reach out to us at any time.</p>

        <p>Thank you for your support in fostering innovation and empowering bright minds.<br/>
        
        <p>Thank you,<br/>
    The Elephant Tank Team.</p>
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

#################################################################################################################################################################################
#Funding Mails

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

        <p>Thank you,<br/>
    The Elephant Tank Team.</p>
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

        <p>Thank you,<br/>
    The Elephant Tank Team.</p>
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
    subject = 'Welcome Investor'
    img_base64  = image_to_base64("userauth/static/images/Image.png")

    message = f'''
    <html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f9f9f9;">
<div style="max-width: 600px; margin: 20px auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); padding: 20px;">
<h2 style="color: #4A90E2; text-align: center;">🎉 Congratulations! 🎉</h2>
<p>Dear <b>{investor_name}</b>,</p>
<p>We’re delighted to inform you that your <b>Investor Account</b> has been approved! Welcome aboard as we embark on an exciting journey together. 🌟</p>
<h3 style="color: #4A90E2;">Event Details:</h3>
<p>📅 Mark your calendar! The event is scheduled for <b>January 31st and February 1st, 2024</b>.</p>
<p>🔗 <b>Login & Explore:</b> Use the link below to access your account and learn more about the event:</p>
<p style="text-align: center;">
<a href="https://elephant-tank.com/Login@elephanttank/" 
               style="color: #ffffff; background-color: #4A90E2; text-decoration: none; padding: 10px 20px; border-radius: 5px;">Login Now</a>
</p>
<p style="text-align: center;">or scan the QR code below:</p>
<p style="text-align: center;">
<img src="data:image/png;base64,{img_base64}" alt="QR Code" style="width: 200px; height: 200px; border: 1px solid #ddd; border-radius: 10px;" />
</p>
<p>We’re thrilled to have you as a part of our community and can’t wait for you to explore the opportunities ahead. 🚀</p>
<p style="margin-top: 30px; text-align: center; font-size: 0.9em; color: #888;">
            Thank you,<br/>
<b>The Elephant Tank Team</b>
</p>
</div>
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
    subject = 'Submit Your Idea'
    message = f'''
    <html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f9f9f9;">
    <div style="max-width: 600px; margin: 20px auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); padding: 20px;">
        <h2 style="color: #4A90E2; text-align: center;">🎉 Welcome Back to the Elephant Tank! 🎉</h2>
        <p>Dear <b>{stud_name}</b>,</p>
        <p>We’re thrilled to inform you that your registration has been <b>approved!</b> You’re now one step closer to embarking on your entrepreneurial journey with us. 🚀</p>
        
        <h3 style="color: #4A90E2;">What’s Next?</h3>
        <p>It’s time to bring your ideas to life! Here’s how you can proceed:</p>
        <ul style="background-color: #f1f1f1; padding: 15px; border-radius: 5px;">
            <li><b>Participation:</b> You can participate <i>individually</i> or as a group (maximum group size: 4).</li>
            <li><b>Idea Submission:</b> Share your innovative idea, including:</li> 
            <ul style="margin-left: 20px;">
                <li><b>Project Type</b></li>
                <li><b>Project Title</b></li>
                <li><b>Project Description</b></li>
                <li><b>Supporting Documents:</b> PDF , PPT, if video.</li>
            </ul>
        </ul>
        <p><b>Important:</b> Ensure your submission follows the format mentioned. Submit your ideas within <b>2-3 days</b> to stay on track!</p>
        
        <h3 style="color: #4A90E2;">Event Details:</h3>
        <p>📅 Mark your calendar! The event is scheduled for <b>January 31st and February 1st, 2024</b>.</p>
        <p>🔗 <b>Login & Explore:</b> Use the link below to access your account and submit your ideas:</p>
        <p style="text-align: center;">
            <a href="https://elephant-tank.com/Login@elephanttank/" 
               style="color: #ffffff; background-color: #4A90E2; text-decoration: none; padding: 10px 20px; border-radius: 5px;">Login Now</a>
        </p>
        <p style="text-align: center;">or scan the QR code below:</p>
        <p style="text-align: center;">
            <img src="data:image/png;base64,{img_base64}" alt="QR Code" style="width: 200px; height: 200px; border: 1px solid #ddd; border-radius: 10px;" />
        </p>
        
        <p>We can’t wait to see your innovative ideas! Let’s make this event a milestone in your journey to becoming an entrepreneur. 🌟</p>
        
        <p style="margin-top: 30px; text-align: center; font-size: 0.9em; color: #888;">
            Thank you,<br/>
            <b>The Elephant Tank Team</b>
        </p>
    </div>
</body>
</html>
    '''
    from_email = settings.EMAIL_HOST_USER
    to_email = [student_email]

    # Create email object
    email = EmailMessage(subject, message, from_email, to_email)
    email.content_subtype = 'html'

    # Attach files
    file_paths = [
        "userauth/static/images/Elephant Tank & InnovateX - Idea Submit.pdf",
        "userauth/static/images/Elephant Tank & InnovateX - project.pptx",
    ]
    
    for file_path in file_paths:
        if os.path.exists(file_path):  # Check if the file exists
            try:
                email.attach_file(file_path)
            except Exception as e:
                print(f"Error attaching file {file_path}: {e}")
        else:
            print(f"File not found: {file_path}")

    # Send email
    try:
        email.send(fail_silently=False)
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
        
        <p>Thank you,<br/>
    The Elephant Tank Team.</p>
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
