# limits to stop iteration
limit_max = 10**8
limit_min = 0.00001
n_max = 200

#color palete (110 colors)
color = [(128,0,0)	,
(139,0,0)	,
(165,42,42)	,
(178,34,34)	,
(220,20,60)	,
(255,0,0)	,
(255,99,71)	,
(255,127,80)	,
(205,92,92)	,
(240,128,128)	,
(233,150,122)	,
(250,128,114)	,
(255,160,122)	,
(255,69,0)	,
(255,140,0)	,
(255,165,0)	,
(255,215,0)	,
(184,134,11)	,
(218,165,32)	,
(238,232,170)	,
(189,183,107)	,
(240,230,140)	,
(128,128,0)	,
(255,255,0)	,
(154,205,50)	,
(85,107,47)	,
(107,142,35)	,
(124,252,0)	,
(127,255,0)	,
(173,255,47)	,
(0,100,0)	,
(0,128,0)	,
(34,139,34)	,
(0,255,0)	,
(50,205,50)	,
(144,238,144)	,
(152,251,152)	,
(143,188,143)	,
(0,250,154)	,
(0,255,127)	,
(46,139,87)	,
(102,205,170)	,
(60,179,113)	,
(32,178,170)	,
(47,79,79)	,
(0,128,128)	,
(0,139,139)	,
(0,255,255)	,
(0,255,255)	,
(224,255,255)	,
(0,206,209)	,
(64,224,208)	,
(72,209,204)	,
(175,238,238)	,
(127,255,212)	,
(176,224,230)	,
(95,158,160)	,
(70,130,180)	,
(100,149,237)	,
(0,191,255)	,
(30,144,255)	,
(173,216,230)	,
(135,206,235)	,
(135,206,250)	,
(25,25,112)	,
(0,0,128)	,
(0,0,139)	,
(0,0,205)	,
(0,0,255)	,
(65,105,225)	,
(138,43,226)	,
(75,0,130)	,
(72,61,139)	,
(106,90,205)	,
(123,104,238)	,
(147,112,219)	,
(139,0,139)	,
(148,0,211)	,
(153,50,204)	,
(186,85,211)	,
(128,0,128)	,
(216,191,216)	,
(221,160,221)	,
(238,130,238)	,
(255,0,255)	,
(218,112,214)	,
(199,21,133)	,
(219,112,147)	,
(255,20,147)	,
(255,105,180)	,
(255,182,193)	,
(255,192,203)	,
(250,235,215)	,
(245,245,220)	,
(255,228,196)	,
(255,235,205)	,
(245,222,179)	,
(255,248,220)	,
(255,250,205)	,
(250,250,210)	,
(255,255,224)	,
(139,69,19)	,
(160,82,45)	,
(210,105,30)	,
(205,133,63)	,
(244,164,96)	,
(222,184,135)	,
(210,180,140)	,
(188,143,143)	,
(255,228,181)]



def tuple2complex2list(func):
    """decorator to convert function arguments\n
    we call function with tuples, and expect list of two lists of coordinates[[x],[y]]\n
    which is natural input for pyqtgraph\n
    but calculation itself are much more conviniet with complex numbers
    """
    def wrap(*args, **kwargs):
        # convert to complex if necessery 
        Z = kwargs['Z']
        if not isinstance(Z[-1], complex):
            kwargs['Z'] = [complex(Z[0], Z[1])]
        C = kwargs['C']
        if not isinstance(C, complex):
            kwargs['C'] = complex(C[0], C[1])
        
        # call func with complex
        Z = func(*args, **kwargs)
        
        # convert back to list
        Zx=[]
        Zy=[]
        [[Zx.append(zi.real),Zy.append(zi.imag)] for zi in Z]
        
        return [Zx,Zy]
    return wrap


@tuple2complex2list
def mandel_seq(Z=(0, 0), C=(0, 0)):
    """z=z^2+C
    calculate list of z coordinates for each iteration\n
    Z is tuple of coordinates (zx,zy)\n
    C is tuple (cx,cy)\n
    (Z and C can be also complex number)
    return Z as list of x_coord list, y_coord list [[x1,x2...],[y1,y2,...]]
    """
    # limits to stop iteration
    global limit_max
    global limit_min
    global n_max

    # dla kazdej wspolrzednej, bierze ostatni element, 
    # oblicza z^2+c i dopisuje na koniec listy
    Z.append(Z[-1] **2 + C)
    
    z = [abs(Z[-1].real), abs(Z[-1].imag)]
    if not any([True for zi in z if zi > limit_max or zi < limit_min or len(Z) > n_max]):        
        [mandel_seq(Z=Z,C=C)]
    
    return Z[1:] # pierwszy element kazdej wspolrzednej jest zero

def colorDiverged(cords):
    """Return color depending of level of diverge\n
    When diverged return black (0,0,0)\n
    Other way return color (r,g,b), depending on number of iterations\n
    the limit is n_max iterations or any coord larger than limit_max
    """
    X = 0
    Y = 1
    global limit_max
    global limit_min
    global color

    if max(cords[X]) > limit_max or max(cords[Y]) > limit_max or (len(cords[X]) > n_max and min(cords[X]) < limit_min):
        return color[int((len(color) / n_max) * len(cords[X])) - 1]
    else:
        return (0,0,0)

