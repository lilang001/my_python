# -*- coding: utf-8 -*-
__author__ = 'admin'

dashe = '\n'+'_'*50 #dashed line
exec_dict = {
    'f':"""
for %s in %s:
    print (%s)
        """,
    's':"""
%s=0
%s=%s
while %s <len(%s):
    print (%s[%s])
    %s=%s+1
    """,
    'n':"""
%s=%d
while %s<%d:
    print (%s)
    %s =%s+%d
    """
}

def main():
    ltype = input('Loop type?(For/While)')
    dtype = input('Data type?(Numer/seq)')
    if dtype == 'n':
        start = input('Starting value?')
        stop = input('Ending value?(non-inclusive)?')
        step = input('Stepping value?')
        seq = str(range(int(start),int(stop),int(step)))
    else:
        seq = input('Enter sequence:')
    var = input('Iterative variable name?')

    if ltype=='f':
        exec_str =exec_dict['f'] %(var, seq, var)
    elif ltype=='w':
        if dtype=='s':
            svar =input('Enter sequence name?')
            exec_str = exec_dict['s']%\
                       (var,svar,seq,var,svar,svar,var,var,var)
        elif dtype=='n':
            exec_str=exec_dict['n']%\
                     (var,start,var,stop,var,var,var,step)

    print (dashe)
    print ('your custon-generrated code:'+dashe)
    print (exec_str+dashe)
    print ('Test excution of the code:'+dashe)
    exec  (exec_str)
    print (dashe)

if __name__ == ('__main__'):
    main()

