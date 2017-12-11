from bs4 import BeautifulSoup
import mechanize
import time

br = mechanize.Browser()
"""
br.open("http://registration.baa.org/2017/cf/Public/iframe_ResultsSearch.cfm?mode=entry")
br.select_form(name="PublicSearch")
br.form["BibNumber"] = "11"
data = br.submit().read()
soup = BeautifulSoup(data, "html5lib")
"""

"""
6: BIB NAME AGE M/F CITY ST CTRY CTZ
9: 5k 10k 15k 20k Half 25k 30k 35k 40k
11: Pace, Proj. Time, Offl. Time, Overall, Gender, Division
"""

"""
trs = soup.find_all("tr")
trs = (trs[6], trs[9], trs[11])
# basic info first:
basic = [td.text.strip() for td in trs[0].find_all("td")]
times = [td.text.strip() for td in trs[1].find_all("td")]
overall = [td.text.strip() for td in trs[2].find_all("td")]
"""

with open("member.csv", "a") as f:
    f.write("bib,name,age,m/f,city,state,country,citizen,5K,10K,15K,20K,Half,25K,30K,35K,40K,Pace,Proj. Time,Offl. Time,Overall,Gender,Division\n")
    for bib in range(32531, 50000):
        br.open("http://registration.baa.org/2016/cf/Public/iframe_ResultsSearch.cfm?mode=entry")
        br.select_form(name="PublicSearch")

        br.form["BibNumber"] = str(bib)
        data = br.submit().read()
        soup = BeautifulSoup(data, "html5lib")

        trs = soup.find_all("tr")
        if len(trs) < 12:
            time.sleep(0.5)
            br.open("http://registration.baa.org/2016/cf/Public/iframe_ResultsSearch.cfm?mode=entry")
            br.select_form(name="PublicSearch")
            br.form["BibNumber"] = 'F' + str(bib)
            data = br.submit().read()
            soup = BeautifulSoup(data, "html5lib")
            
            trs = soup.find_all("tr")
            if len(trs) < 12:
                continue
            
        trs = (trs[5], trs[8], trs[10])
        # basic info first:
        basic = [td.text.strip() for td in trs[0].find_all("td")]
        basic[1] = "\"" + basic[1] + "\""
        times = [td.text.strip() for td in trs[1].find_all("td")]
        overall = [td.text.strip() for td in trs[2].find_all("td")]

        s = ",".join(basic + times + overall) + "\n"
        f.write(s.encode('utf-8'))
    time.sleep(0.5)

