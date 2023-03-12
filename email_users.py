import csv
import smtplib
from fileinput import filename


filename = 'csvs/match_check_in.csv'
# filename = 'csvs/test.csv'

file = open(filename, 'r', encoding="utf8")
datareader = csv.reader(file)
reader = list(datareader)

# Iterate through each row in the CSV file
for row in reader:
    email = row[0]

    # Connect to the SMTP server and send the email
    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()
    server.login("amina@inpairs.io", "@X372j0f58z")

    subject = "Checking in!"
    body = f"Salam!\n\nWe hope things are going well with your match! We would love to hear your feedback on the whole process, so please respond to this email to let us know if you would be available for a quick ~10 minute chat about your experience. We look forward to hearing from you soon!\n\n JAK!\n The inpairs Team"
    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail("amina@inpairs.io", email, msg)

    # Close the SMTP server connection
    server.quit()
