import os
import pandas as pd


# load all py file
def get_py_file(path):
    '''
    :param path: unzipped upload folder path("X:/TA/kadai4/")
    :return: py file list
    '''
    res = []
    lst = os.listdir(path)
    for f in lst:
        fname = os.listdir(path + f)
        file = fname[0]
        res.append(path + f + '/' + file)
    return res


# get lists of input and output file path
def load_test(path, problem):
    '''
    :param path: year directory('X:/TA/2016/')
    :param problem: problem number(A,B,C....)
    :return:list of input case and test case
    '''
    inputFile = []
    testFile = []
    for i in range(1, 5):
        inputFile.append(path+problem+str(i))
        testFile.append(path+problem+str(i)+'.ans')
    return inputFile, testFile


# get standard answer
def get_ans(file):
    '''
    :param file:file from inputFile
    :return: result list
    '''
    with open(file) as f:
        std_ans = f.read().strip().splitlines()
    f.close()
    # print("{} test point loaded ".format(len(std_ans)))
    return std_ans


# judge one py file
def judge_one(file, std_in, std_out, std_ans):
    """
    :param file: test target py file
    :param std_in: inputFile path
    :param std_out: outputFile path
    :param std_ans: test case result list
    :return: count:passed point
            point: total point
            res: score
    """
    point = len(std_ans)
    # check if upload file is format correct
    if os.path.isfile(file) and file.endswith('.py'):
        os.system("{} < {} > {}".format(file, std_in, std_out))
        with open(std_out, 'r') as f:
            stu_ans = f.read().strip().splitlines()
        f.close()
        count = 0
        point = len(std_ans)
        for i, j in zip(std_ans, stu_ans):
            if i == j:
                count += 1
        # print('{} of {} point passed'.format(count, point))
    else:
        print(os.path.isfile(file))
        count = -1
    if count==point:
        res = 2
    elif count>point * 0.8:
        res = 1
    else:
        res = 0
    return count, point, res


def judgement_death(kadai, path, year, problem):
    """
    :param kadai: kadai(kadai4,kadai5...)
    :param path: work space('X:/TA')
    :param year: year(2015...)
    :param problem: (A,B,C...)
    :return: None
    """
    stu_path = path + 'stu_list.xlsx'
    result_path = path + 'result/{}.xls'.format(kadai)
    output_path = path + 'result/'
    upload_path = path + kadai+'/'
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
    input_files, answers = load_test(path+str(year)+'/', problem)
    for stu, py in zip(upload_list, py_list):
        score = 0
        print('-----------------------------------------------------')
        print("student {}:".format(stu))
        if not os.path.exists(output_path + stu + '/'):
            os.mkdir(output_path + stu + '/')
        for case, iF, ans in zip(range(len(input_files)), input_files, answers):
            std_out = output_path + stu + '/' + str(case) + '.txt'
            ans = get_ans(ans)
            count, point, res = judge_one(py, iF, std_out, ans)
            if res == 2:
                print('case {}: pass'.format(case))
            elif res == 1:
                print('case {}: error'.format(case))
            else:
                print('case {}: failed'.format(case))
            # print("{} passed {} of {} in case {} score ={}".format(stu,count,point,case, res))
            score += res
        dic[stu] = score
        print("{} score ={}".format(stu, score))
    print(dic)
    score = []
    for idx in stu_list:
        score.append(dic[idx] if idx in dic else 'not uploaded')
    df = pd.DataFrame({'ID':stu_list, 'result score':score})
    df.to_excel(result_path)


judgement_death('kadai4', 'X:/TA/', '2016', 'A')
