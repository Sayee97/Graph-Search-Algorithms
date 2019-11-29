import collections
import heapq
import math
import time
import re
import time
import time
#import queue
start_time = time.time()
class NodeUCS:
	x=0
	y=0
	p=0
	cost=0
	def __init__(self,cost=0,x=None,y=None,p=None):
		self.cost=cost
		self.x=x
		self.y=y
		self.p=p
	def __lt__(self, other):
		return self.cost<other.cost
	def __eq__(self,other):
		if not isinstance(other,NodeUCS):
			return NotImplemented
		return self.x==other.x and self.y==other.y
	def __hash__(self):
		return hash((self.x,self.y))

class asearchNode:
	x=0
	y=0
	p=0
	cost=0
	heur=0
	def __init__(self,cost=0,heur=0,x=None,y=None,p=None):
		self.cost=cost
		self.heur=heur
		self.x=x
		self.y=y
		self.p=p
	def __lt__(self, other):
		return self.heur<other.heur
	def __hash__(self):
		return hash((self.x,self.y))
	def __eq__(self,other):
		if not isinstance(other,asearchNode):
			return NotImplemented
		return self.x==other.x and self.y==other.y
    
class Node:
	x=0
	y=0
	p=0
	def __init__(self, x=None, y=None, parent=None):
		self.x=x
		self.y=y
		self.p=parent
	def __eq__(self,other):
		if not isinstance(other,Node):
			return NotImplemented
		return self.x==other.x and self.y==other.y
	def __hash__(self):
		return hash((self.x,self.y))

file1 = open("input.txt","r+")
algoUsed1=file1.readline().strip()
terrainDomain=file1.readline().strip().split()
terrainDomain = [int(i) for i in terrainDomain]
W=terrainDomain[0]
H=terrainDomain[1]
landingSite=file1.readline().strip().split()
landingSite=[int(i) for i in landingSite]
lsColumn=landingSite[0]
lsRow=landingSite[1]
threshold= int(file1.readline().strip())
noOfTargets=int(file1.readline().strip())
targetCoordinates=[]
for i in range(noOfTargets):
	p=file1.readline().split()
	p=[int(j) for j in p]
	targetCoordinates.append(p)
terrain=[]
for i in range(H):
	q=file1.readline().strip().split()
	q=[int(o) for o in q]
	terrain.append(q)


def isValid(x,y,i,j):

	if(x>=0 and x<=W-1) and (y>=0 and y<=H-1):
		if abs(terrain[y][x]-terrain[j][i])<=threshold:
			return True
		else:
			return False
	else:
		return False

def heuristic(x,y,n,o):
	h=max(abs(y-o),abs(x-n))
	return h

def BFS(n,o):
	de=[]
	openUCSComp={}
	closedUCS={}
	curr=Node()
	possiblititiesR=[-1,0,0,1,1,-1,1,-1]
	possibilitiesC=[0,-1,1,0,-1,1,+1,-1]
	src=Node(lsColumn,lsRow,None)
	de.append(src)
	openUCSComp[src]=1
	#o=set()


	visited=set()
	while de:
		if not de:
			return None
		curr=de.pop(0)
		i=curr.x
		j=curr.y
		currS=str(curr.x)+" "+str(curr.y)
		if i==n and j==o:
			return curr

		for k in range(8):
			x=i+possibilitiesC[k]
			y=j+possiblititiesR[k]
			if isValid(x,y,i,j):
				agla=Node(x,y,curr)
				if(not agla in closedUCS) and (not agla in openUCSComp):
					de.append(agla)
					openUCSComp[agla]=1
		closedUCS[curr]=1
		#visited.add(currS)
	return None



def pathWeWant(n,ans):
	while(n!=None):
		ans.append([n.x,n.y])
		n=n.p

	return ans


def A(n,o):
	openUCS=[]
	closedUCS={}
	openUCSComp={}
	possiblititiesR=[-1,0,0,1,1,-1,1,-1]
	possibilitiesC=[0,-1,1,0,-1,1,+1,-1]
	
	src=asearchNode(0,0,lsColumn,lsRow,None)
	heapq.heappush(openUCS,src)
	openUCSComp[src]=src.heur
	while openUCS:
		if not openUCS:
			return None
		currSRC=heapq.heappop(openUCS)
		del openUCSComp[currSRC]
		i=currSRC.x
		j=currSRC.y
		cost1=currSRC.cost
		if i==n and j==o:
			return currSRC
		for k in range(8):
			x=i+possibilitiesC[k]
			y=j+possiblititiesR[k]
			if isValid(x,y,i,j):
				q=abs(terrain[y][x]-terrain[j][i])
				if possibilitiesC[k]==0 or possiblititiesR[k]==0:
					cost2=q+10
				else:
					cost2=q+14			
				childHeur=heuristic(x,y,n,o)
				cost2=cost2+cost1
				f=childHeur+cost2
				agla=asearchNode(cost2,f,x,y,currSRC)
				if (not agla in openUCSComp) and (not agla in closedUCS):
					heapq.heappush(openUCS,agla)
					openUCSComp[agla]=agla.heur
				elif agla in openUCSComp:
					y=openUCSComp[agla]
					if agla.heur<y:
						openUCS.remove(agla)
						del openUCSComp[agla]
						heapq.heapify(openUCS)
						heapq.heappush(openUCS,agla)
						openUCSComp[agla]=agla.heur
				elif agla in closedUCS:
					y=closedUCS[agla]
					if agla.heur<y:
						del closedUCS[agla]
						heapq.heappush(openUCS,agla)
						openUCSComp[agla]=agla.heur
		closedUCS[currSRC]=currSRC.heur
	
	return None



def UCS(n,o):
	openUCS=[]
	closedUCS={}
	openUCSComp={}
	possiblititiesR=[-1,0,0,1,1,-1,1,-1]
	possibilitiesC=[0,-1,1,0,-1,1,+1,-1]
	
	src=NodeUCS(0,lsColumn,lsRow,None)
	heapq.heappush(openUCS,src)
	openUCSComp[src]=src.cost
	
	while openUCS:
		if not openUCS:
			return None
		currSRC=heapq.heappop(openUCS)
		del openUCSComp[currSRC]
		i=currSRC.x
		j=currSRC.y
		cost1=currSRC.cost
		if i==n and j==o:
			return currSRC
		for k in range(8):
			x=i+possibilitiesC[k]
			y=j+possiblititiesR[k]
			if isValid(x,y,i,j):
				if possibilitiesC[k]==0 or possiblititiesR[k]==0:
					cost2=cost1+10
				else:
					cost2=cost1+14			
				agla=NodeUCS(cost2,x,y,currSRC)
				if (not agla in openUCSComp) and (not agla in closedUCS):
					heapq.heappush(openUCS,agla)
					openUCSComp[agla]=agla.cost				
				elif agla in openUCSComp:
					y=openUCSComp[agla]
					if agla.cost<y:
						openUCS.remove(agla)
						del openUCSComp[agla]
						heapq.heapify(openUCS)
						heapq.heappush(openUCS,agla)
						openUCSComp[agla]=agla.cost
				elif agla in closedUCS:
					y=closedUCS[agla]
					if agla.cost<y:
						del closedUCS[agla]
						heapq.heappush(openUCS,agla)
						openUCSComp[agla]=agla.cost
		closedUCS[currSRC]=currSRC.cost	
	return None


	
def main():
	text_file=open("output.txt","w")
	s=str(algoUsed1)
	if s=="BFS":
		myans=""
		for i in range(noOfTargets):
			m=BFS(targetCoordinates[i][0],targetCoordinates[i][1])	
			if m==None:
				myans=myans+"\n"+"FAIL"
			if m!=None:
				ans=[]
				ans=pathWeWant(m,ans)
				mystr=""
				ans.reverse()
				for i in ans:
					mystr=mystr+str(i)
				mystr=mystr.strip()
				myans=myans+"\n"+mystr
		myans=myans.replace("]["," ")
		myans=myans.replace("[","")
		myans= myans.replace("]","")
		myans=myans.replace(", ",",")
		myans=myans.replace("  "," ")
		myans=myans.strip()
		myans=myans.strip('\n')
		text_file.write(myans)
		text_file.close()
	if s=="UCS":
		myans=""
		for i in range(noOfTargets):
			m=UCS(targetCoordinates[i][0],targetCoordinates[i][1])
			if m==None:
				myans=myans+"\n"+"FAIL"
			if m!=None:
				print(m.cost)

				ans=[]
				ans=pathWeWant(m,ans)
				mystr=""
				ans.reverse()
				for i in ans:
					mystr=mystr+str(i)
				myans=myans+"\n"+mystr				
		myans=myans.replace("]["," ")
		myans=myans.replace("[","")
		myans= myans.replace("]","")
		myans=myans.replace(", ",",")
		myans=myans.replace("  "," ")
		myans=myans.strip()
		text_file.write(myans)
		text_file.close()
	if s=="A*":
		myans=""
		for i in range(noOfTargets):
			m=A(targetCoordinates[i][0],targetCoordinates[i][1])
			if m==None:
				myans=myans+"\n"+"FAIL"
			if m!=None:
				print(m.cost)

				ans=[]
				ans=pathWeWant(m,ans)
				mystr=""
				ans.reverse()
				
				for i in ans:					

					mystr=mystr+str(i)

				myans=myans+"\n"+mystr	
		myans=myans.replace("]["," ")
		myans=myans.replace("[","")
		myans= myans.replace("]","")
		myans=myans.replace(", ",",")
		myans=myans.replace("  ","")
		myans=myans.strip()

		text_file.write(myans)
		text_file.close()
if __name__ == "__main__":
	#print("hey")
    main()
print("--- %s seconds ---" % (time.time() - start_time))











