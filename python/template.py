import os,sys,re,traceback,codecs
from datetime import datetime
from string import Template
import sys, getopt


class CommonGenerator:   
    def generate(self, argv):
        opts, args = getopt.getopt(argv, "hi:o:m:")
        input_file=""
        output_file=""
        adict = {}
        for op, value in opts:
            if op == "-i":
                input_file = value
                #print('输入：%s'%value)
            elif op == "-o":
                output_file = value
                #print('输出：%s'%value)
            elif op == "-m":

#简化处理 替换是段的话在段两端加入###，且段均放在最后
                bbFlag = "###" in value
                pairTmp = []
                if bbFlag:
                    pairTmp = value.split('###')
                    value = pairTmp[0]
                    pairTmp.remove(pairTmp[0])
                    #adict['CPPINCLUDE']=pairTmp[1]
                    #adict['CPPIMPL']=pairTmp[3]
                
                str_split = value.split()
                
                if bbFlag:
                    pairTmp.insert(0,str_split[-1])
                    str_split.remove(str_split[-1])                    
                    pairTmp.remove(pairTmp[-1])


                    for i in range(0, len(pairTmp)):
                        if i%2 == 0:
                            #print(pairTmp[i])
                            key = pairTmp[i].split('=')[0].strip()
                            #print(key)
                            #print(i+1)
                            adict[key]=pairTmp[i+1]
                    #print(adict)

                for strOne in str_split:
                    pair = strOne.split('=')
                    #print(strOne)
                    #print(pair)
                    adict[pair[0]] = pair[1]
                    
        #print(adict)
        #print('输入：%s'%input_file)
        #print('输出：%s'%output_file)
        

        lines = []

        #模版文件
        template_file = open(input_file,'r')
        #print(template_file.read())
        tmpl = Template(template_file.read())

        #模版替换
        lines.append(tmpl.safe_substitute(adict))

        if output_file != "":
            dst_file = open(output_file,'w')
            dst_file.writelines(lines)
            dst_file.close()
            #print ('generateFile %s over. ~ ~' % output_file)
        #else:
            #print ('generateStr over. ~ ~')
        lines = ''
        lines += tmpl.safe_substitute(adict)
        #print(lines)
        return lines
        
        
def main(argv):
    g = CommonGenerator()
    g.generate(argv)


if __name__ == "__main__":
    main(sys.argv[1:])
