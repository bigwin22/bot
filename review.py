import os
import discord

F = False
T = True

def review(reaction:str,name:str,y:str,m:str,d:str,author:str) -> None:
    '''별점 리뷰 관련 처리 코드'''
    new = 0
    emoji = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']

    schoolp = './school/'+name
    reviewp = './user/'+author+'/review/'
    today = y+m+d
    extension = '.gf'
    

    class object():
        def setdata(self):
            p = open(schoolp+'/total.gf','r')
            avgt = p.readline()
            avgt = float(avgt.strip('\n'))
            totalt = float(p.readline())
            p.close()

            self.avgt = avgt
            self.totalt = totalt
            self.sumt = self.avgt*self.totalt

            x = open(schoolp+'/'+today+'.gf', 'r')
            self.plus = x.readline()
            self.plus = float(self.plus.strip('\n'))
            x.close()

    def No():
        nonlocal new
        school = open(schoolp+'/'+y+m+d+'.gf', 'r')
        avg = school.readline()
        avg = float(avg.strip('\n'))
        total = float(school.readline())
        sum = avg*total
        school.close()

        user = open(reviewp+name+'/'+today+'.gf', 'w')
        user.write('0')
        user.close()

        treview = object()
        treview.setdata()
        user = open(reviewp+name+'/'+today+'.gf', 'w')
        user.write(str(emoji.index(reaction.emoji.name)+1))
        user.close()

        choice = emoji.index(reaction.emoji.name)+1
        avg = (sum+choice)/(total+1)
        

        school = open(schoolp+'/'+today+'.gf', 'w')
        school.write(str(float(avg))+'\n'+str(total+1))
        school.close()

        school = open(schoolp+'/'+today+'.gf', 'r')
        user   = open(reviewp+name+'/'+today+'.gf', 'r')
        em = school.readline()
        em = float(em.strip('\n'))
        school.close()
        user.close()
        treview.sumt -= treview.plus
        treview.sumt += em
        treview.avgt = treview.sumt/(treview.totalt+new)
        
        t = open(schoolp+'/total.gf','w')
        t.write(str(float(treview.avgt))+'\n'+str(treview.totalt+new))
        t.close()

    def Yes():
        nonlocal new
        treview = object()
        treview.setdata()

        school = open(schoolp+'/'+today+'.gf', 'r')
        avg = school.readline()
        avg = float(avg.strip('\n'))
        total = float(school.readline())
        sum = avg*total
        school.close()

        user = open(reviewp+name+'/'+today+'.gf', 'r')
        choice = float(user.readline())
        user.close()

        sum -= choice

        choice = emoji.index(reaction.emoji.name)+1

        user = open(reviewp+name+'/'+today+'.gf', 'w')
        avg = (sum+choice)/total
        user.write(str(emoji.index(reaction.emoji.name)+1))
        user.close()

        school = open(schoolp+'/'+today+'.gf', 'w')
        school.write(str(float(avg))+'\n'+str(total))
        school.close()

        school = open(schoolp+'/'+today+'.gf', 'r')
        em = school.readline()
        em = float(em.strip('\n'))
        treview.sumt -= treview.plus
        treview.sumt += em
        treview.avgt = treview.sumt/(treview.totalt+new)
        school.close()

        t = open(schoolp+'/total.gf','w')
        t.write(str(float(treview.avgt))+'\n'+str(treview.totalt+new))
        t.close()

   
    if os.path.isdir(schoolp) == F:
        os.makedirs(schoolp,exist_ok=T)
        p = open(schoolp+'/total.gf', 'w')
        p.write('0\n0')
        p.close()
    if os.path.isfile(schoolp+'/'+today+'.gf') == F:
        p = open(schoolp+'/'+today+'.gf', 'w')
        p.write('0\n0')
        p.close()        
        new = 1
        
    if os.path.isdir(reviewp+name) == F:
        os.makedirs(reviewp+name,exist_ok=T)
        No()
    else:
        if os.path.isfile(reviewp+name+'/'+y+m+d+'.gf') == F:
            No()
        else:
            Yes()
        