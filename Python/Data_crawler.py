from urllib.request import urlopen
from urllib import request
import os


def get_page(year, problem):
    folder = 'C:/Users/Hu Hang/Desktop/online/TA/' + str(year) + '/'
    if not os.path.exists(folder):
        os.makedirs(folder)
    base_url = "https://icpc.iisf.or.jp/past-icpc/domestic{}/judgedata/{}/".format(year, problem)
    for i in range(1, 5):
        for j in ['', '.ans']:
            title = str(problem) + str(i) + str(j)
            print(title)
            req = request.Request(base_url + title)
            html = urlopen(req)
            content = html.read().decode('utf-8')

            file = os.path.join(folder, title)
            with open(file, 'w') as f:
                f.write(content)
            f.close()
            print(title, 'finished')


get_page(2016, 'A')

