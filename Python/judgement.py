import os
import pandas as pd
import subprocess

from subprocess import TimeoutExpired


def get_py_file(path):
    '''
    :param path:->str :unzipped upload folder path("X:/TA/kadai4/")
    :return:->list :py file list
    '''
    res = []
    lst = os.listdir(path)
    for f in lst:
        fname = os.listdir(path + f)
        for file in fname:
            if '2013' in file:
                res.append(path + f + '/' + file)
                print(file, ' loaded')
    return res


# get lists of input and output file path
def load_test(path, problem):
    '''
    :param path: ->str: year directory('X:/TA/2016/')
    :param problem: -> str: problem number(A,B,C....)
    :return:->list: list of input case and test case
    '''
    inputFile = []
    testFile = []
    for i in range(1, 5):
        inputFile.append(path + problem + str(i))
        testFile.append(path + problem + str(i) + '.ans')
    return inputFile, testFile


# get standard answer from file
def get_ans(file):
    '''
    :param file: -> str: file from inputFile
    :return: -> list: result list
    '''
    with open(file) as f:
        std_ans = f.read().strip().splitlines()
    f.close()
    # print("{} test point loaded ".format(len(std_ans)))
    return std_ans


# judge one py file (個別採点にも使える)
def judge_one(file, std_in, std_out, std_ans):
    """
    :param file: -> str: test target py file
    :param std_in: -> str: inputFile path
    :param std_out: -> str: outputFile path
    :param std_ans: ->list: test case result list
    :return: count: -> int: passed point
            point: -> int: total point
            res: -> int: score
    """
    point = len(std_ans)
    # check if upload file is format correct
    if os.path.isfile(file) and file.endswith('2013.py'):
        try:
            subprocess.call("python " + file, stdin=open(std_in, 'r'),
                            stdout=open(std_out, 'w'), timeout=5)
        except TimeoutExpired:
            print('Time out')
            pass
        stu_ans = []
        try:
            with open(std_out, 'r') as f:
                stu_ans = f.read().strip().splitlines()
            f.close()
        except:
            pass
        count = 0
        point = len(std_ans)
        for i, j in zip(std_ans, stu_ans):
            if i == j:
                count += 1
        print('{} of {} point passed'.format(count, point))
    else:
        print('wrong file')
        print(os.path.isfile(file))
        count = -1
    if count == point:
        res = 2
    elif count > point * 0.8:
        res = 1
    else:
        res = 0
    return count, point, res


# main function
def judgement_death(kadai, path, year, problem):
    """
    :param kadai:->str kadai(kadai4,kadai5...)
    :param path:->str work space('X:/TA')
    :param year:->int year(2015...)
    :param problem:->str (A,B,C...)
    :return: None
    """
    stu_path = path + 'stu_list.xlsx'
    result_path = path + 'result/' + year + '{}.xls'.format(kadai)
    output_path = path + 'result/' + year + '/'
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    upload_path = path + kadai + '/'
    frame = pd.read_excel(stu_path)
    stu_list = list(frame.iloc[:, 0])
    lst = os.listdir(upload_path)
    upload_list = []
    for i in range(len(lst)):
        f = lst[i].split('_')[0]
        f = f[0].upper() + f[1:]
        upload_list.append(f)
    py_list = get_py_file(upload_path)
    dic = {}
    input_files, answers = load_test(path + str(year) + '/', problem)
    for stu, py in zip(upload_list, py_list):
        score = 0
        print()
        print('-----------------------------------------------------')
        print("student {}:".format(stu))
        if not os.path.exists(output_path + stu + '/'):
            os.mkdir(output_path + stu + '/')
        for case, iF, ans in zip(range(len(input_files)), input_files, answers):
            print('case {}: '.format(case))
            std_out = output_path + stu + '/' + str(case) + '.txt'
            ans = get_ans(ans)
            count, point, res = judge_one(py, iF, std_out, ans)
            if res == 2:
                print('pass'.format(case))
            elif res == 1:
                print('error'.format(case))
            else:
                print('failed'.format(case))
            # print("{} passed {} of {} in case {} score ={}".format(stu,count,point,case, res))
            score += res
        dic[stu] = score
        print("{} score ={}".format(stu, score))
    print(dic)
    score = []
    for idx in stu_list:
        score.append(dic[idx] if idx in dic else 'not uploaded')
    df = pd.DataFrame({'ID': stu_list, 'result score': score})
    df.to_excel(result_path)


judgement_death('kadai6', 'G:/TA/', '2013', 'A')
