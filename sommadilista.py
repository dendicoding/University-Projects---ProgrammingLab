
def sum_list(my_list):
    somma = 0
    if len(my_list) == 0:
        return None
    for i in my_list:
        somma = somma + i
    return somma


def main():
    my_list = [1, 2, 3]
    print('Somma: {}'.format(sum_list(my_list)))

if __name__ == "__main__":
    main()
    
    
    
    