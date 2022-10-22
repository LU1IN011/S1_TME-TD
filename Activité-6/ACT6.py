# Wilhem Blondel
import math

Point = Tuple[float, float]
Courbe = List[Point]

O : Point = (0.0 , 0.0)
tri1 : Courbe = [O, (0.0 ,0.3) , (0.4 ,0.0) , O]


def longueur_euclidienne(A: Point, B: Point) -> float:
    """Renvoie la longueur du segment AB"""
    x1, y1 = A
    x2, y2 = B
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

assert longueur_euclidienne(O, (1, 0)) == 1
assert longueur_euclidienne((1, 0), (1, 1)) == 1

def longueur_courbe(c: Courbe) -> float:
    """Renvoie la longueur d'une courbe donnée"""
    res: float = 0
    i: int
    for i in range(len(c)-1):
        res = res + longueur_euclidienne(c[i], c[i+1])
    return res
        
assert abs((longueur_courbe(tri1) - 1.2)) < 10**-12


def segment(A: Point, B: Point) -> Image:
    """Retourne l'image du segment [AB]"""
    xA, yA = A
    xB, yB = B
    return draw_line(xA, yA, xB, yB)

def image_courbe(c: Courbe) -> Image:
    """Retourne l'image de la courbe"""
    x1, y1 = c[0]
    x2, y2 = c[1]
    res: Image = draw_line(x1, y1, x2, y2)
    i: int
    for i in range(1, len(c) - 1):
        res = overlay(res, segment(c[i], c[i+1]))
    return res

# show_image(image_courbe(tri1))

def deplace(A: Point, where: str, to: float) -> Point:
    """Préconditions: where == "H" or where == "B" or where == "G" or where == "D"
    Déplace le point de tant vers la direction donnée: haut, bas, gauche ou droite"""
    x, y = A
    if where == "H":
        return x, y + to
    elif where == "B":
        return x, y - to
    elif where == "G":
        return x - to, y
    elif where == "D":
        return x + to, y

assert deplace(O, "G", 1) == (-1.0, 0.0)
assert deplace(O, "H", 0.5) == (0.0, 0.5)

def iteration_active(i: int, limite: int) -> int:
    """Préconditions i >= 0 and limite > 0
    Retourne la valeur de variable d'itération i restreinte jusqu'à la limite donnée
    Renvoie 0 quand cette limite est atteinte"""
    return i - i // limite * limite

assert iteration_active(5, 4) == 1
assert iteration_active(6, 7) == 6
assert iteration_active(15, 4) == 3


def spirale(ori: Point, dec: float, n: int) -> Courbe:
    """Renvoie une image de spirale de decalage donnée avec un nomre d'itération donné"""
    c: Courbe = [ori]
    prev: Point
    i: int
    which_loop:int
    for i in range(1,n+1):
        prev = c[i - 1]
        which_loop = iteration_active(i, 4)
        if which_loop == 1:
            c.append(deplace(prev, "D", dec*i))
        elif which_loop == 2:
            c.append(deplace(prev, "H", dec*i))
        elif which_loop == 3:
            c.append(deplace(prev, "G", dec*i))
        elif which_loop == 0:
            c.append(deplace(prev, "B", dec*i))
    return c

# show_image(image_courbe(spirale(O, 0.01, 400)))

def convertion_radian(angle: float) -> float:
    """Converti l'angle en degré vers le radian"""
    return angle*math.pi/180

assert convertion_radian(30) == math.pi/6
assert convertion_radian(60) == math.pi/3
assert convertion_radian(120) == 2*math.pi/3

def convertion_angle(rad: float) -> float:
    """Converti l'angle en radian vers le degré"""
    return rad/math.pi * 180

assert convertion_angle(math.pi) == 180
assert convertion_angle(math.pi/4) == 45
assert convertion_angle(3*math.pi/2) == 270

def deplace_diag(p: Point, angle: float, to: float) -> Point:
    """Effectue le décalage diagonale du point fourni dans l'angle en degré souhaité
    L'angle donnée est dans le sens trigonométrique"""
    radian_angle: float = convertion_radian(angle)
    a: float = to * math.sin(radian_angle)
    b: float = to * math.cos(radian_angle)
    return deplace(deplace(p, "H", a), "D", b)


def deplace_diag_rad(p: Point, angle: float, to: float) -> Point:
    """Effectue le décalage diagonale du point fourni dans l'angle en radian souhaité
    L'angle donnée est dans le sens trigonométrique"""
    a: float = to * math.sin(angle)
    b: float = to * math.cos(angle)
    return deplace(deplace(p, "H", a), "D", b)
    

def angle_seg(A: Point, B: Point) -> float:
    """Détermine l'angle en radian formé par la droite AB par rapport à l'axe x dans le sens trigonométrique"""
    
    xB, yB = B
    xA, yA = A
    I: Point = (xB, yA)
    l_AI: float = longueur_euclidienne(A, I)

    # Evaluation de la position de B par rapport à A dans le cercle trigonométrique

    # On met A en tant qu'origine du repère pour le calcul
    x: float = xA*(-1)
    y: float = yA*(-1)

    # On vérifie la poisition de B par rapport à A
    a: float = xB + x
    b: float = yB + y

    if(a == 0 and b == 0):
        # L'angle est nul
        return 0

    if(a <= 0 and b >= 0):
        # second quartier du cercle
        return math.pi - math.acos(l_AI/ longueur_euclidienne(A, B))

    if(a <= 0 and b <= 0):
        # troisième quartier du cercle
        return math.pi + math.acos(l_AI/ longueur_euclidienne(A, B))

    if(a >= 0 and b <= 0):
        # quatrième quartier du cercle
        return  - math.acos(l_AI/ longueur_euclidienne(A, B))

    # Premier quartier du cercle
    return math.acos(l_AI/ longueur_euclidienne(A, B))


def fragment(A: Point, B: Point) -> Courbe:
    """Fragmente le segment donné à la manière du fractale de Koch"""
    c: Courbe = [A]
    angle: float = angle_seg(A, B)
    taille: float = longueur_euclidienne(A, B)
    p1: Point = deplace_diag_rad(A, angle, 1/3*taille)
    c.append(p1)
    c.append(deplace_diag_rad(p1, angle + convertion_radian(60), 1/3*taille))
    c.append(deplace_diag_rad(A, angle, 2/3*taille))
    c.append(B)

    return c

# show_image(image_courbe(fragment(O, (-0.5, 0))))
    
def append_list(source: List[T], destination: List[T]) -> List[T]:
    """Modifie la liste source pour y ajouter la liste de destination
    La liste source est volontairement modifié elle-même"""
    e: T
    for e in destination:
        source.append(e)
    return source

def triangle_de_rayon_r(p: Point, r: float) -> Courbe:
    """Renvoie la courbe correspondant au triangle de rayon r"""
    # Traçage des points du triangle donné

    S: Point = deplace(p, "H", r) # Sommet
    A: Point = deplace_diag(p, 210, r) # Point inférieur gauche
    B: Point = deplace_diag(p, -30, r) # Point inférieur droit

    return [A, S, B, A]

def courbe_flocon(p: Point, r: float, n: int) -> Courbe:
    """Préconditions r >= 0 and n >= 0
    Retourne le flocon de Koch avec le rayon du triangle et le nombre d'itération indiquée"""
    

    P1: Point
    P2: Point

    c: Courbe = triangle_de_rayon_r(p, r)
    c_prev: Courbe

    i: int
    j: int
    for i in range(1, n+1):
        c_prev = c
        c = []
        for j in range(0, len(c_prev)-1):
            P1 = c_prev[j]
            P2 = c_prev[j+1]
            append_list(c, fragment(P1, P2))
        
    return c

# show_image(image_courbe(courbe_flocon(O, 0.8, 6)))

# Suggestion 3

def courbe_dragon(A: Point, B: Point, n: int) -> Courbe:
    """Préconditions n >= 0
    Retourne la coubre correspondant à la courbe du dragon à partir du segment [AB]""" 
    c: Courbe = [A, B]
    c_prev: Courbe
    taille: float
    P1: Point
    P2: Point
    angle: float
    i: int
    j: int
    for i in range(1, n+1):
        c_prev = c
        c = []
        for j in range(0, len(c_prev)-1):

            P1 = c_prev[j]
            P2 = c_prev[j+1]

            taille = longueur_euclidienne(P1, P2)
            angle = angle_seg(P1, P2)
            
            c.append(P1)
            if(j%2 == 0):
                c.append(deplace_diag_rad(P1, angle + math.pi/4, math.sqrt(1/2*taille**2)))
            else:
                c.append(deplace_diag_rad(P1, angle - math.pi/4, (math.sqrt(1/2*taille**2))))
        c.append(c_prev[-1])
    return c

# show_image(overlay(image_courbe(courbe_dragon((-0.5, 0), (0.5, 0), 2)), (image_courbe(courbe_dragon((-0.5, 0), (0.5, 0), 1)))))

# show_image(image_courbe(courbe_dragon((-0.5, 0), (0.5, 0), 14)))
            

