from threading import Thread , Event;
from sys import argv , executable
from os import system , getpid , close , execv
from psutil import Process
from datetime import datetime


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Sudoku :
	boxes = [
		[(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)],
		[(3,0),(3,1),(3,2),(4,0),(4,1),(4,2),(5,0),(5,1),(5,2)],
		[(6,0),(6,1),(6,2),(7,0),(7,1),(7,2),(8,0),(8,1),(8,2)],
		[(0,3),(0,4),(0,5),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5)],
		[(3,3),(3,4),(3,5),(4,3),(4,4),(4,5),(5,3),(5,4),(5,5)],
		[(6,3),(6,4),(6,5),(7,3),(7,4),(7,5),(8,3),(8,4),(8,5)],
		[(0,6),(0,7),(0,8),(1,6),(1,7),(1,8),(2,6),(2,7),(2,8)],
		[(3,6),(3,7),(3,8),(4,6),(4,7),(4,8),(5,6),(5,7),(5,8)],
		[(6,6),(6,7),(6,8),(7,6),(7,7),(7,8),(8,6),(8,7),(8,8)]];
	
	def __init__(self) :
		#self.data = data
		self.state = True;
		self.getData();
		if self.mode in ["-s","-S"] :
			if not self.checkPreSol() : print(bcolors.FAIL + "repeated values found..." + bcolors.ENDC);self.askAgain()
			try : self.getAns();
			except IndexError : print(bcolors.FAIL + "the puzzle values given are not correct..." + bcolors.ENDC);self.askAgain()  
			self.checkSol();
			if self.state == False : print(bcolors.FAIL + "something went wrong..." + bcolors.ENDC);self.askAgain()
			self.viewData();
			print("generated and checked at" , datetime.now().strftime("%A, %d. %B %Y %I:%M:%S %p") , end="\n\n");self.askAgain()
			#print(self.targetPoints);
			#print(self.data);
			#print(self.mode)
			#exit(0);
		if self.mode in ["-v","-V"] :
			self.checkSol();
			if self.state == True : print(bcolors.OKGREEN + "the given solution is correct" + bcolors.ENDC);self.askAgain()
			else : print(bcolors.FAIL + "the given solution is Wrong" + bcolors.ENDC);self.askAgain()
			#exit(0);

	@staticmethod
	def askAgain() :
		def _restart_program(args):
		    """Restarts the current program, with file objects and descriptors cleanup"""
		    try:
		        p = Process(getpid())
		        for handler in p.open_files() + p.connections():
		            close(handler.fd)
		    except Exception as e: print("error found > " , e)

		    python3 = executable
		    print(args)
		    execv(python3 , ["python3"] + [__file__] + args) 

		def _ask() :
			ans = input("do you want to play again ? (y / n) : ");
			if not ans.lower() == "y" : print(bcolors.OKGREEN + "program exit successfully..." + bcolors.ENDC);exit(0);
			_restart_program(input(">>> ").split());

		_ask();

	def viewData(self) :
		system("clear");
		print("\n\n====================\n" , bcolors.HEADER + "S o l u t i o n" + bcolors.ENDC ,"\n====================\n\n");
		for row in range(9) :
			for col in range(9) :
				if (row,col) in self.targetPoints :
					print(" " , bcolors.OKBLUE + str(self.data[row][col]) + bcolors.ENDC , " |" , end="");
				else :
					print(" " , bcolors.BOLD + str(self.data[row][col]) + bcolors.ENDC , " |" , end="");			
			line = "-----+" * 9;
			print("\n" + line);
		print("\n")

		
	def getData(self) :
		data = argv;
		data.pop(0);
		if len(data) == 0 : print(bcolors.FAIL + "No data is given..." + bcolors.ENDC);self.askAgain()
		if data[0] not in ["-s","-S","-v","-V","-e","-E","-h","-H"] : print(bcolors.FAIL + "bad args specified, use -s -v -e -h" + bcolors.ENDC);self.askAgain()
		mode = data.pop(0);
		if mode == "-e" or mode == "-E" : print(bcolors.OKGREEN + "program exit successfully..." + bcolors.ENDC);exit(0);
		if mode == "-h" or mode == "-H" : print(bcolors.BOLD + """
|-	use `suduko` command to solve a suduko puzzle or to check a solution
|-	-s or -S : give a list of 81 cell with optionally ][ in which the value `_` represent an
|	unknown value that will be solved
|
|-	-v or -V : give a list of 81 cell with optionally ][ in which all cell contains a value
|	and the checker will check your solution
|
|-	-e or -E : exit the program
|
|-	-h or -H : show program manual  
		""" + bcolors.ENDC);self.askAgain()
		if len(data) == 0 : print(bcolors.FAIL + "no puzzle data found..." + bcolors.ENDC);self.askAgain()
		if data[0].startswith("[") : data[0] = data[0].replace("[" ,"",1)
		if data[-1].endswith("]") : data[-1] = data[-1].replace("]","",1);
		#if len(data) != 81 : print("not enought puzzles..");exit(0)

		targetPoints = [];
		filtered = [];
		i,j = 0,0;
		group = 0;
		for point in data :
			if point == "" : continue;
			if group % 9 == 0 : filtered.append([]);
			group += 1;
			if point.isdigit() and int(point) >= 1 and int(point) <= 9 :
				filtered[-1].append(int(point));
			elif point == "_" and mode in ["-s" , "-S"] : filtered[-1].append(-1);targetPoints.append((j,i))
			else :
				print(bcolors.FAIL + "bad puzzle number, numbers should be from 1 to 9 only..." + bcolors.ENDC);
				self.askAgain()
			if i == 8 : i = 0;j += 1;
			else : i += 1; 
		if not (len(filtered) == 9 and len(filtered[-1]) == 9) : print(bcolors.FAIL + "not enought puzzles or too much..." + bcolors.ENDC);self.askAgain()
		self.data = filtered
		self.mode = mode;
		self.targetPoints = targetPoints;
		#print(self.data);
		#print(self.mode);




	
	def getSurroundedNumbers(self , row , column) :
		surround = [self.data[row][i] for i in range(9) if self.data[row][i] != -1 and i != column] + [self.data[i][column] for i in range(9) if self.data[i][column] != -1 and i != row]
		startRow = int(row / 3) * 3
		startCol = int(column / 3) * 3
		for i in range(startRow , startRow + 3) :
			for j in range(startCol , startCol + 3) :
				if self.data[i][j] != -1 and not (i == row and j == column): surround.append(self.data[i][j])
		return surround

	
	def getAns(self) :
		row = 0;
		col = 0;
		lastSolvedPoints = [];
		flag = False;
		while True :
			if self.data[row][col] == -1 or flag == True:
				notSafePoints = self.getSurroundedNumbers(row , col);
				if flag == False : x = 1;
				else : x = self.data[row][col] + 1;self.data[row][col] = -1;
				for i in range(x , 10) :
					if i not in notSafePoints :
						self.data[row][col] = i;
						lastSolvedPoints.append((row,col));
						flag = False;
						break;
				if self.data[row][col] == -1 or flag == True :
					last = lastSolvedPoints.pop();
					row = last[0];
					col = last[1];
					flag = True;
					col -= 1;
			if col == 8 : 
				col = 0;
				row += 1;
			else : col += 1;
			#if row == 9 : return self.data;
			if row == 9 : break; 

	@staticmethod
	def _startThread(func , args) :
		thrd = Thread(target=func,args=args)
		thrd.start();


	def checkSol(self) :
		e = Event();
		self.countLiveThreads = 0;
		self.state = True;
		def checkLine(shape) :
			for row in range(9) :
				if self.state == False : break;
				temp = [i for i in range(1 , 10)];
				for col in range(9) :
					if shape == "r" : value = self.data[row][col];
					elif shape == "c" : value = self.data[col][row];
					else : raise TypeError("type not specified --use r or c");
					#print(value);
					if value >= 1 and value <= 9 : 
						if value in temp : temp.remove(value);
					else : self.state = self.state and False;
				if len(temp) != 0 : self.state = self.state and False;
			#e.set();
			self.countLiveThreads += 1;

		def checkSubgrids() :
			def checkSubgrid(box) :
				temp = [i for i in range(1 , 10)];
				for point in box :
					value = self.data[point[0]][point[1]];
					if value >= 1 and value <= 9 : 
						if value in temp : temp.remove(value);
					else : self.state = self.state and False;
				if len(temp) != 0 : self.state = self.state and False;
				self.countLiveThreads += 1;

			for box in self.boxes :
				Sudoku._startThread(lambda : checkSubgrid(box) , ());

			while self.countLiveThreads != 11 : pass;
			e.set();

		Sudoku._startThread(lambda : checkLine("r")  , ());
		Sudoku._startThread(lambda : checkLine("c")  , ());
		Sudoku._startThread(lambda : checkSubgrids() , ());
		e.wait();
		return self.state;


	def checkPreSol(self) :
		def isSafe(numbers=[]) :
			for num in numbers :
				if numbers.count(num) != 1 and num != -1 : return False;
			return True;
		for row in range(9) :
			if not isSafe(self.data[row]) : return False;
		for col in range(9) :
			column = [];
			for row in range(9) : column.append(self.data[row][col]);
			if not isSafe(column) : return False;
			column = [];
		for i in range(9) :
			box = [];
			for point in self.boxes[i] :
				box.append(self.data[point[0]][point[1]]);
			if not isSafe(box) : return False;
			box = [];
		return True;


#print(Sudoku(data).checkSol())
if __name__ == "__main__" : Sudoku()


"""
[1 _ _ _ _ _ 4 _ _
 4 _ _ _ 5 _ 1 9 _ 
 _ _ _ _ 2 7 _ 8 6 
 _ 5 6 _ _ 1 _ _ 4 
 _ _ _ 2 _ 8 _ _ _ 
 8 _ _ 5 _ _ 2 1 _ 
 6 8 _ 1 9 _ _ _ _ 
 _ 2 9 _ 3 _ _ _ 8 
 _ _ 7 _ _ _ _ _ _]
"""

