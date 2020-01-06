with open("fileList_real.txt","r") as f:
    with open ("final_list.txt","w") as g:
        for line in f:
            print(line[23:],file=g,end="")
