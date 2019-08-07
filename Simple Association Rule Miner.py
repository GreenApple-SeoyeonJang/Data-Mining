import sys
f = open(sys.argv[1], 'r')
minsup = float(sys.argv[2])
minconf = float(sys.argv[3])

valarr = [] # 트랜잭션 ID값을 제외한 전체 리스트
count = [0] # 전체 리스트 valarr에서 각 트랜잭션 시작 위치 저장
transaction = 0  # 트랜잭션 개수
c1 = []
c2 = []
c2_c = [[0]*100 for i in range(100)] #frequent 2-itemset을 구하기 위한 c2 카운트 리스트
f1 = []

for c in range(0, 100): #c1리스트 초기화
    c1.append(0)

line = f.readline()
c = 0
while line != '':     # 텍스트 파일 읽어서 c1리스트 만들기
    transaction = transaction + 1
    linearr = line.split(',')
    count.append(count[c] + len(linearr)-1)
    c = c + 1
    for i in range(1, len(linearr)): #각 아이템 개수 카운트
        c1[int(linearr[i])] = c1[int(linearr[i])] + 1
        valarr.append((int(linearr[i])))
    line = f.readline()
f.close()

#Step 1: Find frequent 1-itemsets / minsup을 넘긴 c1의 아이템셋
for i in range(0, 100):
    if (float(c1[i]) / transaction) >= minsup:
        f1.append(i)

# Step 2: Generate candidate 2-itemsets / frequent 1-itemset의 조합인 c2
for j in range(0, len(f1)-1):
    for k in range(j + 1, len(f1)):
        c2.append([f1[j], f1[k]])

# 각 Candidate 2-itemset이 transaction마다 몇 번 나왔는지 카운트 c2_c[][]
for p in range(0, len(c2)):
    for q in range(0, transaction):
        if (valarr[count[q]:count[q + 1]].count(c2[p][0]) > 0) and (valarr[count[q]:count[q + 1]].count(c2[p][1]) > 0):
            c2_c[c2[p][0]][c2[p][1]] = c2_c[c2[p][0]][c2[p][1]] + 1

print('Association rules found:')
for m in range(0, 100):
    for n in range(0, 100):
        if (float(c2_c[m][n]) / transaction) >= minsup: #Step 3: Find frequent 2-itemsets / c2_c에서 카운트가 minsup 이상인 경우
            if (float(c2_c[m][n]) / c1[m]) > minconf: #Step 4: Generate association rules / confidence > minconf
                print(m, '->', n, '(support =', (float(c2_c[m][n])/transaction), ', confidence =', c2_c[m][n]/c1[m])
            if (float(c2_c[m][n]) / c1[n]) > minconf:
                print(n, '->', m, '(support =', (float(c2_c[m][n])/transaction), ', confidence =', c2_c[m][n]/c1[n])