class Quine_Mc:

    # initializer
    # Minterm 리스트와 Don't care 리스트를 받는다.
    # 단 Don't care가 없는 경우(입력 받지 않은 경우) default 값으로 ['']을 받는다.
    # 각 리스트는 bit를 String 타입으로 저장 ex) min1 = ['1101', '1100', '1110', '1111', '1010', '0011', '0111', '0110']
    def __init__(self, m_list, d_list=['']):
        self.m_list = m_list
        self.d_list = d_list

    def __info__(self):
        print('M  :', self.m_list)
        print('D  :', self.d_list)
        print('PI :', Quine_Mc.dic_to_list(Quine_Mc.pi(self)))
        print('EPI:', Quine_Mc.epi(self))

    # staticmethod 항목

    # list 형태를 dic 형태로 바꿔준다.
    # example) min1 = ['1101' ...]
    #          -> {'1101' : 13 ...}
    @staticmethod
    def list_to_dic(list_data):
        result = {}
        for n in list_data:
            result.update({n: Quine_Mc.bin_to_dec(n)})
        return result

    # string 타입의 2진수를 10진수로 변환하여 return
    @staticmethod
    def bin_to_dec(str_data):
        result = 0
        for m in range(len(str_data)):
            result += pow(2, len(str_data) - 1 - m) * int(str_data[m])
        return result

    # dic 형태를 list 형태로 바꿔준다. 예시는 list_to_dic 참조
    @staticmethod
    def dic_to_list(dic_data):
        result = []
        for key in dic_data:
            result.append(key)
        return result

    # 두 개의 최소항의 결합 , 만일 두 항이 한 자리만 차이난다면, 그 자리를 -로 대체한 후 그 값을 return 한다.
    @staticmethod
    def combine(num1, num2):
        l = len(num2)
        cnt = 0
        result = ''
        for i in range(l):  # 최소항의 길이만큼 반복
            if num2[i] == num1[i]:  # 최소항의 각 자리가 같다면 return 될 변수에 그 자리값을 추가
                result += num2[i]
            else:  # 각 자리가 다르다면 cnt 변수에 1을 추가하고 return 될 변수에 '-' 추가
                cnt += 1
                result += '-'

        if cnt == 1:  # 각 자리가 다른 횟수가 1번이었다면, 즉 두 항이 한자리만 차이나는 경우에는 return
            return result
        else:  # 그 외의 경우에는 None 값 return
            return None

    # Prime Implicant를 구하는 pi와 Essentail Prime Implicatn를 구하는 epi는 위의 static method를 활용.

    def pi(self):
        # f_list 에 minterm 리스트와 don't care 리스트를 합쳐준다. 단, don't care 리스트가 비었을 경우에는 minterm리스트만.
        f_list = self.m_list.copy()
        if self.d_list != ['']:
            f_list.extend(self.d_list)
        # f_dic 에 f_list 를 변환하여 저장.
        f_dic = Quine_Mc.list_to_dic(f_list)
        while True:
            l = len(f_list)
            # del_list 두 항이 결합되면 결합되는 항은 지워저야 한다. 다만 바로 지우면 반복문의 index 오류가 발생하므로 반복이 끝난 후 지우기 위해 지울 항은 따로 보관한다.
            # extend_list 또한 del_list와 마찬가지로 추가 될 경우 index error 발생 가능하므로 추후 추가하기 위해 따로 저장.
            del_list = []
            extend_list = []
            for i in range(l - 1):  # 중복되는 항의 결합을 배제하기 위한 반복 조건
                for j in range(i, l):
                    combine_result = Quine_Mc.combine(f_list[i], f_list[j])
                    if combine_result is not None:  # 두 항이 한 자리만 차이나는 경우
                        f_list[i] not in del_list and del_list.append(f_list[i])
                        f_list[j] not in del_list and del_list.append(f_list[j])  # 각 항을 del_list에 추가
                        combine_result not in extend_list and extend_list.append(
                            combine_result)  # 결합된 값이 extend_list에 없을 경우 추가, 중복 될 경우가 있기 때문.
                        val = str(f_dic[f_list[i]]) + " " + str(
                            f_dic[f_list[j]])  # dict 형에서 value로 들어갈 것, 항의 숫자를 합쳐준다. ex) 1101 과 1100이 합쳐지면 '13 12'
                        f_dic.update({combine_result: val})  # dict은 집합이므로 중복된 값을 자동 제거하고 업데이트하므로 바로 추가해준다.

            if not del_list:  # 무한 반복문의 종료 조건, del_list가 없다는 뜻은 더 이상 결합할 수 있는 항이 없다는 뜻이므로 종료
                break
            for d in del_list:  # 결합 된 항을 제거하여 후보항만 남긴다.
                f_list.remove(d)
                del f_dic[d]

            f_list.extend(extend_list)  # 결합 되어 새로 나온 항을 추가.

        return f_dic

    def epi(self):  # 기본적으로 pi에서 구한 dic 형태의 후보항 dict 사용
        pi_dic = Quine_Mc.pi(self)
        mt_dic = {}
        result = []
        # don't care는 EPI에서 고려하지 않는다. 따라서 minterm의 항만 10진수로 변환하여 따로 저장.
        for i in self.m_list:
            mt_dic.update({str(Quine_Mc.bin_to_dec(i)): 0})

        # pi에서 구한 후보항들의 dict에는 value에 번호가 적혀있다.
        # value내 번호가 minterm의 번호와 일치할 시 그 번호에 1 증가.
        for key in pi_dic:
            for n in pi_dic[key].split():
                try:
                    mt_dic[n] += 1
                except KeyError:  # don't care의 번호는 mt_dic에 없으므로 key error 발생, 에러처리해준다.
                    pass

        for key in pi_dic:
            for n in pi_dic[key].split():
                try:
                    if mt_dic[n] == 1:  # 1인경우는 그 번호를 가진 항이 EPI라는 것이므로 그 항을 return될 변수에 추가해준다.
                        key not in result and result.append(key)
                except KeyError:
                    pass
        return result


# 테스트 케이스

min1 = ['1101', '1100', '1110', '1111', '1010', '0011', '0111', '0110']

min2 = ['0000', '0100', '1000', '0101', '1100', '0111', '1011', '1111']

min3 = ['0001', '0011', '0100', '0110', '1011', '0000', '1000', '1010', '1100', '1101']

min4 = ['0000', '0010', '0101', '0110', '0111', '1000', '1001', '1101']
dc4 = ['0001', '1100', '1111']

qm1 = Quine_Mc(min1)
qm2 = Quine_Mc(min2)
qm3 = Quine_Mc(min3)
qm4 = Quine_Mc(min4, dc4)

qm1.__info__()
print()
qm2.__info__()
print()
qm3.__info__()
print()
qm4.__info__()
