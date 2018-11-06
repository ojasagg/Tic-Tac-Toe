import time
import random
node_val_computed=0
def decision(t):
	t=t.split(',')
#	print ",".join(t)
	for i in range(9):
		t[i]=int(t[i])
	arr=[t[:3],t[3:6],t[6:]]
	if arr[0][0]==0 and arr[1][1]==0 and arr[2][2]==0:
		return 1
	if arr[0][2]==0 and arr[1][1]==0 and arr[2][0]==0:
		return 1
	if arr[0][0]==0 and arr[1][0]==0 and arr[2][0]==0:
		return 1
	if arr[0][1]==0 and arr[1][1]==0 and arr[2][1]==0:
		return 1
	if arr[0][2]==0 and arr[1][2]==0 and arr[2][2]==0:
		return 1
	if (arr[0][0]==0 and arr[0][1]==0 and arr[0][2]==0):
		return 1
	if (arr[1][0]==0 and arr[1][1]==0 and arr[1][2]==0):
		return 1
	if (arr[2][0]==0 and arr[2][1]==0 and arr[2][2]==0):
		return 1
	if arr[0][0]+arr[1][1]+arr[2][2]==3:
		return -1
	if arr[0][2]+arr[1][1]+arr[2][0]==3:
		return -1
	if (arr[0][0]==1 and arr[0][1]==1 and arr[0][2]==1):
		return -1
	if (arr[1][0]==1 and arr[1][1]==1 and arr[1][2]==1):
		return -1
	if (arr[2][0]==1 and arr[2][1]==1 and arr[2][2]==1):
		return -1
	if arr[0][0]+arr[1][0]+arr[2][0]==3:
		return -1
	if arr[0][1]+arr[1][1]+arr[2][1]==3:
		return -1
	if arr[0][2]+arr[1][2]+arr[2][2]==3:
		return -1	
	if t.count(-1)>0:
		return 2#unfilled condition
	return 0#draw condition

def compute_alpha_beta(tree,key,turn,alpha,beta):
	global node_val_computed
	node_val_computed+=1
	d=decision(key)
	if d!=2:
		value[key]=d
		return d
	if turn==1:
		chldrn=[]
		val=-250
		for i in tree[key][0]:
			x=compute_alpha_beta(tree,i,1-turn,alpha,beta)
			val=max(val,x)
			alpha=max(val,x)
			chldrn.append(x)
			if x==1 and alpha>=beta:
				break
		value[key]=max(chldrn)
		return max(chldrn)
	else:
		val=250
		chldrn=[]
		for i in tree[key][0]:
			x=compute_alpha_beta(tree,i,1-turn,alpha,beta)
			chldrn.append(x)
			val=min(val,x)
			beta=min(val,x)
			if x==-1 and alpha>=beta:
				break
		value[key]=min(chldrn)
		return min(chldrn)

def print_move(s):
	print '\n\n'
	row=[0,0,0]
	arr=[]
	for i in range(3):
		arr.append(row[:])
	k=0
	for i in range(3):
		line='\t\t\t'
		for j in range(3):
			if s[k]=="-1":
				line+=''
				line+='\t'
			elif s[k]=="0":
				line+='O'
				line+='\t'
			else:
				line+='X'
				line+='\t'
			if j<2:
				line+='|'
			line+='\t'
			k+=1
		print line
		if i<2:
			print "\t\t\t----------------------------------"
	print '\n\n'

#Start of the code
start_time=time.time()
s="-1,-1,-1,-1,-1,-1,-1,-1,-1"
value={}
tree={}
tree[s]=[[],[]]#children, parent
tmp_tree=[s]
c=0
print"Generating initial tree...."
while len(tmp_tree)>0:
	node=tmp_tree.pop(0)
	node_list=node.split(',')
	for k in range(9):
		node_list[k]=int(node_list[k])
	zero_count=node_list.count(0)
	one_count=node_list.count(1)
	if zero_count+one_count==9:
		continue
	turn=0
	if zero_count==one_count:
		turn=0
	else:
		turn=1
	for i in range(9):
		if node_list[i]==-1:
			temp_list=[0]*9
			node_list[i]=turn
			for k in range(9):
				temp_list[k]=str(node_list[k])
			new_node=",".join(temp_list)
			if tree.has_key(new_node):
				tree[new_node][1].append(node)				
			else:
				value[new_node]=-1
				tree[new_node]=[[],[node]]
				tmp_tree.append(new_node)
			tree[node][0].append(new_node)
			node_list[i]=-1
	c+=1
count=0
countw=0
countl=0
countd=0
countnon=0
for i in tree:
	count+=1
	if decision(i)==1:
		countw+=1
	if decision(i)==-1:
		countl+=1
	elif decision(i)==0:
		countd+=1
	elif decision(i)==2:
		countnon+=1

#print count
s="-1,-1,-1,-1,-1,-1,-1,-1,-1"
print"Computing minimax node values...."
compute_alpha_beta(tree,s,1,250,-250)
#Tree with value stored upto now
print "Time taken via alpha-beta pruning is "+str(time.time()-start_time)+"sec"
print "Value of "+str(node_val_computed)+"computed"

#Play game

print "\n\n\t\t You play with O "
print "\t\t Bot plays with X "
s="-1,-1,-1,-1,-1,-1,-1,-1,-1"
while True:
	u_inp=input('\n\n\t\t\033[1;36mMake your move, enter first choice(1-9)------\033[1;m')
	to_move=s.split(",")
	to_move[u_inp-1]="0"
	s=",".join(to_move)
	if decision(s)!=2:
		print_move(s.split(","))
		break
	print_move(s.split(","))
	print '\n\n\t\t\033[1;36mComputer move done\033[1;m'
	states=[]
	state_val=[]
	for i in tree[s][0]:
		states.append(i)
		state_val.append(value[i])
	flag=min(state_val)
	max_val_entry=[]
	for i in range(len(state_val)):
		if state_val[i]==flag:
			max_val_entry.append(i)
	l=len(max_val_entry)
	move=random.randint(0,l-1)
	game_move=states[max_val_entry[move]]
	s=game_move[:]
	print_move(s.split(","))
	if decision(s)!=2:
		break
if decision(s)==1:
	print '\t\t\033[1;32mYOU WON\033[1;m'
elif decision(s)==-1:
	print '\t\t\033[1;31mYOU LOSE\033[1;m'
else:
	print '\t\t\033[1;36mGAME DRAW\033[1;m'
print "\n\n"
