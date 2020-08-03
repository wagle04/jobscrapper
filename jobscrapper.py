import bs4 as bs
from urllib.request import Request, urlopen
import os
import smtplib


file_name = "sentlinks.txt"

sender_email = "sender gmail address"
rec_email = "reciever gmail address"
sender_password = "sender gmail password"


def mainprocess(url):

    print("*******************************************************")
    print("website url: "+url)
    header = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url, headers=header)
    page = urlopen(req)
    page_soup = bs.BeautifulSoup(page, "html.parser")

    jobs = page_soup.findAll(
        'div', {"class": "single-post d-flex row no-gutters job_list"})

    for job in jobs:
        job_title = str(job.a.text).lower()
        job_footer = job.findAll('div', {"class": "job-listing-footer"})
        job_footer_lis = job.findAll('li')
        job_link = job.a['href']

        job_address = str(job_footer_lis[0].text).lower()
        job_level = str(job_footer_lis[1].text).lower()
        job_posted_time = str(job_footer_lis[2].text).lower()

        # if job was added a month ago, the program stops
        if("month" in job_posted_time):
            return

        # specify language and frameworks
        if("python" in job_title or "django" in job_title):

            # specify required job level
            if("begineer" in job_level):

                # specify the required address
                if("kathmandu" in job_address or "lalitpur" in job_address):

                    # specify the time when the job vacancy was posted. vacany posted a month before may have been filled or so
                    if ("minute" in job_posted_time or "hour" in job_posted_time or "day" in job_posted_time or "week" in job_posted_time):
                        print(job_link)
                        print(job_title)
                        print(job_address)
                        print(job_level)
                        print(job_posted_time)

                        # to check if the link is already mailed or not

                        if not (os.path.exists(file_name)):
                            f = open(file_name, "w")
                            f.close()

                        with open(file_name) as f:
                            lines = f.read().splitlines()

                        if not (job_link in lines):

                            message = "Subject: New Job Vacancy  \n \n"+"\n \n"+job_link

                            server = smtplib.SMTP('smtp.gmail.com', 587)
                            server.starttls()
                            server.login(sender_email, sender_password)
                            print("login success")
                            server.sendmail(
                                sender_email, rec_email, message)
                            print("email has been sent")

                            with open(file_name, "a") as g:
                                g.write(job_link+"\n")

    # for checking the older pages for job vacancy; loop through mainprocess function until month appers on job vacany posted date
    last_slash_position = url.rfind("/")
    index = int(url[last_slash_position+1:])

    # kathmandujob.com posts 14 job vacany per page
    index = index+14
    new_incomplete_url = url[:last_slash_position+1]
    new_complete_url = new_incomplete_url+str(index)
    print("*******************************************************")

    mainprocess(new_complete_url)


if __name__ == "__main__":
    website = "https://kathmandujobs.com/jobs/0"
    print("main function running............")
    print("*******************************************************")
    mainprocess(website)
