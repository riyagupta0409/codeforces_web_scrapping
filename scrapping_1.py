import requests
from bs4 import BeautifulSoup as bs
import os
import csv

months = ['jan' , 'feb' , 'mar' , 'apr' , 'may' , 'jun' , 'jul' ,'aug' , 'sep' , 'oct' , 'nov' , 'dec']
 

def main_window():
	while True :
		s = input('Enter username of the user :- ')
		if user_exist(s):
			print("CURRENT USER ---" , s)
			print("1. All Submissions")
			print("2. Check for a particular verdict")
			print("3. Check for a particular year")
			print("4. Check for a particular month")
			print("5. To change user")
			changed = 0 
			while True:
				if not changed:
					choice = input("Enter your choice :-")
				else :
					choice = input("Enter valid choice :-")
				if choice == '1':
					all_submissions(s)
				if choice == '2':
					particular_verdict(s)
				if choice == '3':
					particular_year(s)
				if choice == '4':
					particular_month(s)
				if choice == '5':
					break	
				if choice == 'X' or choice == 'x' or choice == 'E' or choice == 'e':
					return
				else :
					changed =1 
					continue
		else:
			print("Invalid username !! Can't fetch data")
			continue

def user_exist(s):
	response = requests.get('https://codeforces.com/submissions/{}'.format(s))
	soup = bs(response.text , "html.parser")
	try :
		all_content = soup.find("table" , {"class":"status-frame-datatable"})
		if all_content == None :
			return 0 
		rows = all_content.findAll("tr")
		row = rows[1]
		td = row.findAll("td")
		who = td[2].a.text
		if who!=s:
			return 0
		else:
			return 1
	except:
		return 0

def all_submissions(s):

	with open('submissions.csv','w',newline='') as file :
		writer = csv.writer(file)
		writer.writerow(['#','when','who','problem','lang','verdict','time','memory'])
	f=1
	page = 0
	save = []
	total = 0
	accepted = 0
	wrong = 0
	tle = 0 
	while True:
		page+=1
		with open('submissions.csv','a+',newline='',encoding="utf-8") as file :
			writer = csv.writer(file)
			response = requests.get('https://codeforces.com/submissions/{}/page/{}'.format(s,page))
			soup = bs(response.text , "html.parser")
			all_content = soup.find("table" , {"class":"status-frame-datatable"})
			rows = all_content.findAll("tr")

			# hash to check the submission id of first submission and compare with last page
			hash_ = rows[1]["data-submission-id"]
			if hash_ == save :
				print("Total submissions :- {}".format(total))
				print("Accepted submissions :- {}".format(accepted))
				print("Wrong submissions  :- {}".format(wrong))
				print("Time Limit Exceeded :- {}".format(tle))

				os.startfile(r'C:\Users\DELL\Desktop\python_tut\web_scrapping\app\submissions.csv')
				return 

			# fetching each row data n writing in csv
			for row in range(1,len(rows)):
				total+=1
				td = rows[row].findAll("td")
				hash_ = rows[row]["data-submission-id"]
				if row == 1:
					save = hash_
				when = td[1].span.text
				who = td[2].a.text
				problem = str(td[3].a.text).strip()
				lang = td[4].text.strip()
				verdict = td[5].span.text.strip()
				time = td[6].text.strip()
				memory = td[7].text.strip()
				if verdict == "Accepted":
					accepted+=1
				elif verdict[:4] == 'Time':
					tle+=1
				elif verdict[:5] == 'Wrong':
					wrong+=1
				writer.writerow([hash_,when,who,problem,lang,verdict,time,memory])

def particular_verdict(s):
	user_verdict = input('Enter verdict :- ')

	with open('submissions.csv','w',newline='',encoding="utf-8") as file :
		writer = csv.writer(file)
		writer.writerow(['#','when','who','problem','lang','verdict','time','memory'])
	f=1
	page = 0
	save = []
	count = 0
	while True:
		page+=1
		with open('submissions.csv','a+',newline='',encoding="utf-8") as file :
			writer = csv.writer(file)
			response = requests.get('https://codeforces.com/submissions/{}/page/{}'.format(s,page))
			soup = bs(response.text , "html.parser")
			all_content = soup.find("table" , {"class":"status-frame-datatable"})
			rows = all_content.findAll("tr")
			hash_ = rows[1]["data-submission-id"]
			if hash_ == save :
				print("Total {} solutions are {}".format(user_verdict ,count))
				os.startfile(r'C:\Users\DELL\Desktop\python_tut\web_scrapping\app\submissions.csv')
				return 
			for row in range(1,len(rows)):
				td = rows[row].findAll("td")
				hash_ = rows[1]["data-submission-id"]
				if row == 1:
					save = hash_
				when = td[1].span.text
				who = td[2].a.text
				problem = str(td[3].a.text).strip()
				lang = td[4].text.strip()
				verdict = td[5].span.text.strip()	
				time = td[6].text.strip()
				memory = td[7].text.strip()
				if verdict[0].lower() == (user_verdict[0]).lower():
					count+=1
					writer.writerow([hash_,when,who,problem,lang,verdict,time,memory])


def particular_year(s):
	year = int(input('Enter the year :- '))
	with open('submissions.csv','w',newline='',encoding="utf-8") as file :
		writer = csv.writer(file)
		writer.writerow(['#','when','who','problem','lang','verdict','time','memory'])
	f=1
	page = 0
	save = []
	count = 0
	flag = 1
	while True:
		page+=1
		with open('submissions.csv','a+',newline='',encoding="utf-8") as file :
			writer = csv.writer(file)
			response = requests.get('https://codeforces.com/submissions/{}/page/{}'.format(s,page))
			soup = bs(response.text , "html.parser")
			all_content = soup.find("table" , {"class":"status-frame-datatable"})
			rows = all_content.findAll("tr")
			hash_ = rows[1]["data-submission-id"]

			if hash_ == save :
				print("Total submissions are {}".format(count))
				os.startfile(r'C:\Users\DELL\Desktop\python_tut\web_scrapping\app\submissions.csv')
				return 
			for row in range(1,len(rows)):
				td = rows[row].findAll("td")
				hash_ = rows[1]["data-submission-id"]
				if row == 1:
					save = hash_
				when = td[1].span.text
				if int(when[7:11] )< int(year) :
					flag = 0 
					break

				who = td[2].a.text
				problem = str(td[3].a.text).strip()
				lang = td[4].text.strip()
				verdict = td[5].span.text.strip()	
				time = td[6].text.strip()
				memory = td[7].text.strip()
				if when[7:11] == str(year):
					count+=1
					writer.writerow([hash_,when,who,problem,lang,verdict,time,memory])
			if flag == 0:
				print("Total submissions are {}".format(count))
				os.startfile(r'C:\Users\DELL\Desktop\python_tut\web_scrapping\app\submissions.csv')
				return 

def particular_month(s):
	year = int(input('Enter the year :- '))
	month = input('Enter the month :- ')
	with open('submissions.csv','w',newline='',encoding="utf-8") as file :
		writer = csv.writer(file)
		writer.writerow(['#','when','who','problem','lang','verdict','time','memory'])
	f=1
	page = 0
	save = []
	count = 0
	flag = 1
	while True:
		page+=1
		with open('submissions.csv','a+',newline='',encoding="utf-8") as file :
			writer = csv.writer(file)
			response = requests.get('https://codeforces.com/submissions/{}/page/{}'.format(s,page))
			soup = bs(response.text , "html.parser")
			all_content = soup.find("table" , {"class":"status-frame-datatable"})
			rows = all_content.findAll("tr")
			hash_ = rows[1]["data-submission-id"]
			if hash_ == save :
				print("Total submissions are {}".format(count))
				os.startfile(r'C:\Users\DELL\Desktop\python_tut\web_scrapping\app\submissions.csv')
				return 
			for row in range(1,len(rows)):
				td = rows[row].findAll("td")
				hash_ = rows[1]["data-submission-id"]
				if row == 1:
					save = hash_
				when = td[1].span.text
				who = td[2].a.text
				problem = str(td[3].a.text).strip()
				lang = td[4].text.strip()
				verdict = td[5].span.text.strip()	
				time = td[6].text.strip()
				memory = td[7].text.strip()
				if when[7:11] == str(year) and when[:3].lower()==month[:3].lower():
									count+=1
									writer.writerow([hash_,when,who,problem,lang,verdict,time,memory])


				# break condition for checking month and year 
				if int(when[7:11] ) < int(year) :
					flag = 0 
					break

				elif int(when[7:11] ) == int(year):
					if months.index(when[:3].lower()) < months.index(month[:3].lower()) :
						flag = 0 
						break

			if flag == 0:
				print("Total submissions are {}".format(count))
				os.startfile(r'C:\Users\DELL\Desktop\python_tut\web_scrapping\app\submissions.csv')
				return 				
				
main_window()



