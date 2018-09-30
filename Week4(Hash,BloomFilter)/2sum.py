class TwoSum():
    def __init__(self, file_name):
        self.MIN = -10000
        self.MAX = 10000

        self.data_set = set()
        self.data_list = []

        file = open(file_name)
        lines = file.readlines()

        for x in lines:
            self.data_set.add(int(x.strip("\n")))

        self.data_list = sorted(self.data_set)

    def sum_checker(self):
        left = 0
        right = len(self.data_list) - 1
        counter = [False] * (self.MAX - self.MIN + 1)

        while right > left:
            Sum = self.data_list[left] + self.data_list[right]

            if Sum > self.MAX:
                right -= 1
            elif Sum < self.MIN:
                left += 1
            else:
                counter[Sum - self.MIN] = True
                current_left = left
                current_right = right

                while(current_left < right):
                    #Sweep left from current index to right
                    current_left += 1
                    Sum = self.data_list[current_left] + self.data_list[right]
                    if Sum > self.MAX:
                        break
                    elif Sum < self.MIN:
                        break
                    else:
                        if self.data_list[current_left] != self.data_list[right]:
                            counter[Sum - self.MIN] = True

                while(current_right > left):
                    #Sweep right from current index to left
                    current_right -= 1
                    Sum = self.data_list[left] + self.data_list[current_right]
                    if Sum > self.MAX:
                        break
                    elif Sum < self.MIN:
                        break
                    else:
                        if self.data_list[left] != self.data_list[current_right]:
                            counter[Sum - self.MIN] = True

                right -= 1
                left += 1
        
        num = 0
        for i in counter:
            if i:
                num+=1

        return num


            
if __name__ == "__main__":
    twosum = TwoSum('2sum.txt')
    counter = twosum.sum_checker()
    print(counter)