#!/usr/bin/python

'''
Author: Kevin Baker (kbaker@tcd.ie)
Usage: ./diff_mailchimp_exports.py << old list >> << new list >>

You can use this script to diff two Mailchimp csv exports
where the format is <email>, <first name>, <last name>, ...

It produces a list of <email>, <first name>, <last name>
for people who are on the old csv mailing list and are not
on the new csv mailing list

The use case this was created for was during Fresher's week
it is helpful to create a list of email for a reminder email 
to last year's members who haven't signed up again this year. 

Issues:
If people sign up with a different email address they will end up 
in the new list. Some checking of names might be useful to reduce
false positives
'''

import csv
import logging
import sys
from sets import Set

logger = logging.getLogger('diff_lists')

def diff_lists(old_list, new_list):
  new_list_file = open(new_list, 'r')

  new_emails = Set()
  with open(new_list, 'r') as new_list_csv:
    csvreader = csv.reader(new_list_csv)
    for row in csvreader:
      new_emails.add(row[0]) # first item in row is email address

  logger.info("There are %d email addresses in the new list" % len(new_emails))

  missing_emails = Set()
  with open(old_list, 'r') as old_list_csv:
    csvreader = csv.reader(old_list_csv)
    count = 0
    for row in csvreader:
      email = row[0]
      count = count + 1
      if email not in new_emails:
        missing_emails.add(email)
        print ','.join([email, row[1], row[2]])
    logger.info("There are %d email addresses in the old list" % count)

  logger.info("There are %d email addresses in the old list that are not in the new list", len(missing_emails))

if __name__ == "__main__":
  if len(sys.argv) is not 3:
    raise Exception("Usage: ./diff_mailchimp_exports.py << old list >> << new list >>")
  old_list = sys.argv[1]
  new_list = sys.argv[2]

  diff_lists(old_list, new_list)