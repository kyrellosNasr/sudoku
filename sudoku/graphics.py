from tkinter import Tk , Frame , Label , LabelFrame , Entry , Radiobutton , BooleanVar , Button , END
from initiate import Sudoku , bcolors

class MainWin(Tk , Sudoku) :
	def __init__(self , title , *args , **kwargs) :
		Tk.__init__(self,*args,**kwargs);
		self.title(title);
		self.resizable(False , False);
		self.drawBoxes();
		self.mode = BooleanVar();
		self.mode.set(True);
		self.drawChoice()
		self.doBtn = Button(self,text=" Try ",bg="#452",fg="#FFF",command=self._onClick)
		self.doBtn.grid(row=4,column=0,pady=10,padx=5,ipady=2,sticky="we")
		self.bind("<Return>",self._onClick)


	def drawBoxes(self) :
		self._boxes = [];
		frame = Frame(self,bg="#000")
		frame.grid(row=0,column=0,padx=5,pady=5)
		for i in range(9) :
			for j in range(9) :
				temp = Entry(frame,borderwidth=1,width=4,font=("Consolas",12),justify="center",relief="ridge")
				temp.grid(row=i,column=j,ipady=3)
				if j in [3,6] : temp.grid(row=i,column=j,ipady=3,padx=(2,0))
				if i in [3,6] : temp.grid(row=i,column=j,ipady=3,pady=(2,0))
				temp.grid(row=i,column=j,ipady=3);
				self._boxes.append((temp , i , j));


	def drawChoice(self) :
		frame = LabelFrame(self,text="Mode")
		frame.grid(row=1,column=0,sticky="we",padx=5,pady=5);
		Radiobutton(frame,text="solve",variable=self.mode , value=True).grid(row=0,column=1,pady=(0,8))
		Radiobutton(frame,text="check",variable=self.mode , value=False).grid(row=0,column=3,pady=(0,8))
		frame2 = LabelFrame(self,text="Console")
		frame2.grid(row=2,column=0,sticky="we",padx=5,pady=5);
		self.debug = Label(frame2,text="\n\n")
		self.debug.grid(row=0,column=0,ipadx=5,pady=(8,0))
		rstLbl = Label(self,text="reset ?",fg="blue",cursor="hand2")
		rstLbl.grid(row=3,column=0,sticky="w",padx=5,pady=0);
		rstLbl.bind("<Button-1>",self._resetPuzzle);


	def getData(self) :
		self.data = [[]];
		col = 0;
		for point in self._boxes :
			value = point[0].get().replace(" ","");
			
			if value == "" and not self.mode.get() : self.data = [[]];return -1;
			if value == "" : 
				self.data[-1].append(-1);
				col += 1;
				if col % 9 == 0 : self.data.append([]);
				continue;
			if value.isdigit() and int(value) >= 1 and int(value) <= 9 :
				self.data[-1].append(int(value));
			else :
				self.data = [[]];
				#print("error 2");
				return -2;
			col += 1;
			if col % 9 == 0 : self.data.append([]);
		self.data.pop();
		#print(self.data)
		return True;

	def _onClick(self,event=None) :
		if self.getData() in [-1,-2] : self._report("puzzle are not numbers from 1-9 or not compatible with\nmode\n" , "f");return;
		if self.mode.get() :
			#if mode is solving
			if self.checkPreSol() :
				try :
					self.getAns();
				except IndexError : self._report("puzzle combinations are wrong\n","f");return;
				if self.checkSol() : 
					#print(self.data);
					self._report("solution listed above\n\n","s")
					self._putData()
				else :
					self._report("something went wrong\n\n","f");
			else : 
				self._report("puzzle data are repeated\n\n","f");
		else :
			#if mode is checking
			if self.checkSol() :
				self._report("solution is right\n\n","s");
			else : 
				self._report("solution is wrong\n\n","f");

		
	def _report(self , text , label) :
		if label == "s" :
			self.debug.configure(text=text,fg="green");
		elif label == "f" : 
			self.debug.configure(text=text,fg="red");

	def _putData(self) :
		for row in range(9) :
			for col in range(9) :
				order = ((row * 9) - (9 - col)) + 9
				entry = self._boxes[order][0];
				if entry.get().replace(" ","") == "" : entry.configure(fg="#FFF",bg="blue");entry.insert(0,self.data[row][col]);
				else : entry.configure(fg="#000",bg="#FFF");

	def _resetPuzzle(self,event) :
		for entry in self._boxes :
			entry[0].configure(bg="#FFF",fg="#000");
			entry[0].delete(0,END)
			entry[0].insert(0,"");

	def run(self) :
		self.mainloop();





MainWin("jesus christ").run()
"""
row = 8;
col = 8;
print( ((row * 9) - (9 - col)) + 9 )
"""