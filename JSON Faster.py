import sublime
import sublime_plugin
import sys

INDENT = 2
OCC = 0
OFFSET = 0 

class ExampleCommand(sublime_plugin.TextCommand):

    def currentCaret(self):
        return self.view.sel()[0].begin()

    def caculateLastBraces(self,cp):
        #得到当前point所在的行
        lineRegion = self.view.line(cp)
        #得到行头到光标的区域
        line0_caret = sublime.Region(lineRegion.begin(),cp)
        #得到光标前的所有字符
        allChar = self.view.substr(line0_caret)
        #得到行区域大小
        return line0_caret.size()

    def printOut(self,edit,ofs,indent):
        for x in range(0,ofs+indent):
            self.view.insert(edit,self.currentCaret()," ")

    def findCursor(self,edit,startPoint):
        cRegion = self.view.find("\"\"", startPoint)
        return cRegion.a + 1


    def run(self,edit):

        OCC = self.currentCaret()
        OFFSET = self.caculateLastBraces(OCC)

        self.view.insert(edit,OCC,"{\n")
        self.printOut(edit,OFFSET,INDENT)
        self.view.insert(edit,self.currentCaret(),"\"\" : \"\"\n")
        self.printOut(edit,OFFSET,0)
        self.view.insert(edit,self.currentCaret(),"}")

        #把光标放到双引号位置
        cs = sublime.Region(self.findCursor(edit,OCC),self.findCursor(edit,OCC))
        self.view.sel().clear()
        self.view.sel().add(cs)

class TabCommand(sublime_plugin.TextCommand):

    def currentCaret(self):
        return self.view.sel()[0].begin()

    def findCursor(self,edit,startPoint):
        cRegion = self.view.find("\"\"", startPoint)
        return cRegion.a + 1

    def run(self,edit):
        cs = sublime.Region(self.findCursor(edit,self.currentCaret()),self.findCursor(edit,self.currentCaret()))
        self.view.sel().clear()
        self.view.sel().add(cs)

class addKeyValueCommand(sublime_plugin.TextCommand):

    def currentCaret(self):
        return self.view.sel()[0].begin()

    def printOut(self,edit,ofs,indent):
        for x in range(0,ofs+indent):
            self.view.insert(edit,self.currentCaret()," ")

    def findCursor(self,edit,startPoint):
        cRegion = self.view.find("\"\"", startPoint)
        return cRegion.a + 1

    def run(self,edit):

        OCC = self.currentCaret()
        # OFFSET = self.caculateLastBraces(OCC)
        #在末尾位置加上逗号和换行  ********可以增加一个引号的逗号的**********
        lineLastPoint = self.view.line(self.currentCaret()).b
        self.view.insert(edit,lineLastPoint,",\n")
        #st得到第一个引号所在在总buffer的偏移
        lr = self.view.line(OCC)
        st = self.view.find("\"",lr.a).a
        #由于根据self.view.sel() 得到光标，光标显示在本行，把光标移入下一行首
        #得到光标并移入下一行
        r,c = self.view.rowcol(OCC)
        #根据行和列，得到总体偏移量
        off = st - self.view.text_point(r,0)
        #跟局行和列，得到光标位置
        nextPoint = self.view.text_point(r+1,0)
        #把光标移动到下列
        cs = sublime.Region(nextPoint,nextPoint)
        self.view.sel().clear()
        self.view.sel().add(cs)
        #得到当前光标后，把光标移动到指定位置
        self.printOut(edit,off,0)
        self.view.insert(edit,self.currentCaret(),"\"\" : \"\"")
        #添加键值对后，在把光标移动到输入位置
        csa = sublime.Region(self.findCursor(edit,nextPoint),self.findCursor(edit,nextPoint))
        self.view.sel().clear()
        self.view.sel().add(csa)

class subKeyValueCommand(sublime_plugin.TextCommand):

    def currentCaret(self):
        return self.view.sel()[0].begin()

    def run(self,edit):
        #直接删除当前行
        lineRegion = self.view.full_line(self.currentCaret())
        self.view.erase(edit,lineRegion)
        #把光标移到最后一个双引号中 ******删除的时候想想如何把整个行个删了
        p = self.view.find_by_class(self.currentCaret(),False,sublime.CLASS_PUNCTUATION_END)
        #把逗号删除
        comma = sublime.Region(p-1,p)
        self.view.erase(edit,comma)
        #把光标移动到引号内
        cs = sublime.Region(p - 2,p - 2)
        self.view.sel().clear()
        self.view.sel().add(cs)

# class deleteQuoCommand(sublime_plugin.TextCommand):

#     def currentCaret(self):
#         return self.view.sel()[0].begin()

#     def run(self,edit):
#         #得到双引号内区域
#         quoRegion = self.view.expand_by_class(self.currentCaret(), sublime.CLASS_PUNCTUATION_START)
#         #已经包括“了，加1就是”所占的区域
#         pr = sublime.Region(quoRegion.a,quoRegion.a + 1)
#         #如果后面直接接“则是当前buffer两边找，如果不接则找到末尾引号删除
#         print(self.view.substr(pr))
#         if self.view.substr(quoRegion.b - 1) == "\"":
#             print('a')
#             fr = sublime.Region(quoRegion.b - 2,quoRegion.b - 1)
#         else:
#             fr = sublime.Region(quoRegion.b - 1,quoRegion.b)
        
#         self.view.erase(edit,pr)
#         self.view.erase(edit,fr)

       
class outCommand(sublime_plugin.TextCommand):

    def currentCaret(self):
        return self.view.sel()[0].begin()

    def printOut(self,edit,ofs,indent):
        for x in range(0,ofs+indent):
            self.view.insert(edit,self.currentCaret()," ")

    def findCursor(self,edit,startPoint):
        cRegion = self.view.find("\"\"", startPoint)
        return cRegion.a + 1

    def run(self,edit):
        #找到}这个字符，然后光标在其后,其实真正光标在其前
        bra = self.view.find("}", self.currentCaret()).b
        #把光标插入到大括号后边
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(bra,bra))
        #插入回车到下一行
        self.view.insert(edit,self.currentCaret(),",\n")
        #找到下一个大括号，下一个括号在什么位置，然后往前移两个位置
        braa = self.view.find("}",self.currentCaret()).a
        #更具这个位置找到当前行的位置
        line = self.view.line(braa).a
        #相减得到缩进位置
        p = braa - line
        #根据这个位置进行缩进
        self.printOut(edit,p,INDENT)
        #插入键值对时加两个位置
        self.view.insert(edit,self.currentCaret(),"\"\" : \"\"")
        #插入后当前光标在“”后边，把光标插入第一个双引号中
        #首先得到当前光标的行
        s = self.view.line(self.currentCaret()).a
        #插入到相应的位置
        csa = sublime.Region(self.findCursor(edit,s),self.findCursor(edit,s))
        self.view.sel().clear()
        self.view.sel().add(csa)








                   