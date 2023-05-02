import re

def userid(string):
    pattern = r"^[A-Z]\d{9}$"

    alphaTable = {'A': 1, 'B': 10, 'C': 19, 'D': 28, 'E': 37, 'F': 46,
            'G': 55, 'H': 64, 'I': 39, 'J': 73, 'K': 82, 'L': 2, 'M': 11,
            'N': 20, 'O': 48, 'P': 29, 'Q': 38, 'R': 47, 'S': 56, 'T': 65,
            'U': 74, 'V': 83, 'W': 21, 'X': 3, 'Y': 12, 'Z': 30}

    # 計算總和值
    if re.search(pattern,string):
        abc = alphaTable[string[0]] + int(string[1]) * 8 + int(string[2]) * 7 + int(string[3]) * 6 + int(string[4]) * 5 + int(string[5]) * 4 + int(string[6]) * 3 + int(string[7]) * 2 + int(string[8]) * 1 + int(string[9])
        # 驗證餘數
        if abc % 10 == 0:
            return True
    else:
        return False

def username(string):
    pattern = r"[\W]" #特殊字元
    
    if re.search(pattern,string):
        print("帳號有特殊字")
        return False#有 
    else:   
        print("帳號正常")
        return True#沒有

def password(string):
    pattern = r"[\W]"
    if re.search(pattern,string):#有特殊字元
        
        pattern = r"[^\w!@$%^?~]"
        if re.search(pattern,string):#有非法字元，不可註冊

            return False

        else:#無非法字元，可以註冊
            return True
    else:#無特殊字元，可以註冊 
        return True

