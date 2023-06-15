import os
from email.message import EmailMessage
import ssl
import smtplib
import pandas as pd
import mimetypes

def read_emails_from_csv_of_type(filename, email_types=None):
    df = pd.read_csv(filename)

    # If email_types is provided, filter the dataframe for rows where type is in the list of email_types
    if email_types is not None:
        df = df[df['type'].isin(email_types)]

    return df['mails'].tolist()

def send_mail(email_subject, filenames_to_attach, email_types=None, attach_pdf=True):
    email_sender = 'dpavez@crystal-lagoons.com'
    email_password = 'vcxpacpxsbyxajmy'
    filename = 'mails.csv'

    # Read the email addresses from the CSV file
    emails = read_emails_from_csv_of_type(filename, email_types)

    subject = email_subject

    # Initialize the body as an empty string
    body = ''
    
    # Initialize a flag to indicate whether a DWG has been attached
    dwg_attached = False

    for i, filename_to_attach in enumerate(filenames_to_attach, start=1):
        # Get the email body from the text file
        txt_filename = os.path.join('TEXs', filename_to_attach, filename_to_attach + '.txt')
        with open(txt_filename, 'r') as f:
            # Add a title before each part
            body += f'Part {i}:\n' + f.read() + '\n\n'

    em = EmailMessage()

    em['From'] = email_sender
    em['To'] = email_sender  # Send to your own email
    em['Cc'] = ', '.join(emails)  # CC all emails
    em['Subject'] = subject
    em.set_content(body)

    for filename_to_attach in filenames_to_attach:
        if attach_pdf:
            # Construct the paths to the files to attach
            pdf_filename = os.path.join('TEXs', filename_to_attach, filename_to_attach + '.pdf')
            mime_type_pdf, _ = mimetypes.guess_type(pdf_filename)
            mime_type_pdf, mime_subtype_pdf = mime_type_pdf.split('/')
            with open(pdf_filename, 'rb') as f:
                em.add_attachment(f.read(),
                                maintype=mime_type_pdf,
                                subtype=mime_subtype_pdf,
                                filename=os.path.basename(pdf_filename))

        # Attach the DWG file if it exists and no DWG has been attached yet
        if not dwg_attached:
            dwg_filename = os.path.join('dwg', filename_to_attach + '.dwg')
            if os.path.exists(dwg_filename):
                mime_type_dwg = 'application'
                mime_subtype_dwg = 'octet-stream'  # generic byte stream type
                with open(dwg_filename, 'rb') as f:
                    em.add_attachment(f.read(),
                                    maintype=mime_type_dwg,
                                    subtype=mime_subtype_dwg,
                                    filename=os.path.basename(dwg_filename))
                dwg_attached = True  # Update the flag to indicate that a DWG has been attached

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(em)
