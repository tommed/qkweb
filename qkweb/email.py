import os

sendmail_path = "/usr/sbin/sendmail"

def send(eto, efrom, subject, body):
	""" send an email using sendmail """
	p = os.popen("%s -t" % sendmail_path, "w")
	p.write("From: %s\n"  % efrom)
	p.write("To: %s\n" % eto)
	p.write("Subject: %s\n\n" % subject)
	p.write(body)
	return p.close()
