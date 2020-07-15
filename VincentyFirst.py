""" 
        Vincenty Yöntemi:

Büyük uzunluklarda çözüm sağlayan bu
yöntemde yarıçapı ekvator yarıçapı kadar olan
bir yardımcı küreden yararlanılır. Jeodezik eğri
ile yardımcı kürede oluşan büyük daire yayı
arasında ilişki kurularak oluşturulan iç içe
eşitliklere dayalı bir çözüm yapılmıştır.

"""
### Birinci temel ödevde hesaplanacak şekilde ayarlandı!

from math import sin, cos, tan, sqrt, radians, atan, asin
 
def hesapla(derece: int, dakika: int, saniye: float) -> float:
    return derece + dakika / 60 + saniye / 3600

# GRS80 elipsoidine göre hesaplar yapılacaktır.
# Büyük yarıeksen metre cinsinden,
a: float = 6378137.000
# Basıklık (f),
f: float = 1 / 298.257222101
# Küçük yarıeksen metre cinsinden,
b: float = 6356752.314140347
# Kutup eğrilik yarıçapı metre cinsinden,
c: float = 6399593.6259
# Bu kısımda m ile n değerlerini hesaplıyoruz.
e: float = (sqrt(a ** 2 - b ** 2)) / a
eu: float = e / sqrt(1 - e ** 2)
 
print(f"a değeri: {a}")
print(f"f değeri: {f}")
print(f"b değeri: {b}")
print(f"c değeri: {c}")
print(f"e degeri: {e}")
print(f"e` degeri: {eu}")
print("m değeri: ", e ** 2)
print("n değeri: ", eu ** 2)
 
print("==============================")
 
# φ = Enlem (elipsoidal) == enlem,
enlem: float = float(input("Enlem değerini giriniz: "))
# λ = Boylam == boylam,
boylam: float = float(input("Boylam değerini giriniz: "))
# S = Jeodezik eğri uzunluğu == S,
S: float = float(input("Jeodezik eğri uzunluğunu giriniz: "))
# α = Azimut == alfa1,
alfa1: float = float(input("Azimut değerini giriniz: "))
  
print("enlem değeri radyan: ", enlem)
print("boylam değeri radyan: ", boylam)
print("alfa1 değeri radyan: ", alfa1)
print("==============================")

"""
İlk olarak birinci noktanın enlemi ( β1),
yardımcı küre üzerinde ekvatordan birinci
noktaya kadar açısal büyük daire yayı
uzunluğu (σ1) ve jeodezik eğrinin ekvatordaki
azimutu (αek) hesaplanır.

"""
# tan(β_1) = (1/sqrt(1+n))*tan(enlem) == Beta1
def beta(eu: float, enlem: float) -> float:
    return atan((1 / sqrt(1 + eu ** 2)) * tan(enlem))
 
if beta(eu, enlem) == 0.6790364576072638:
    print("Beta1 Dogru")
 
Beta1: float = atan((1 / sqrt(1 + eu ** 2)) * tan(enlem))
# tan(σ_1) = (tan(Beta1)/cos(alfa1)) == Sigma1
Sigma1: float = atan(tan(Beta1) / cos(alfa1))
# sin(α_ek) = cos(Beta1)*sin(alfa1) == alfaEk
alfaEk: float = asin(cos(Beta1) * sin(alfa1))
# u^2 = pow(n*(cos(alfaEk)),2) == uKare
uKare: float = eu ** 2 * (cos(alfaEk) ** 2) 
# A == A
A: float = 1 + (uKare / 16384) * (4096 + uKare * (-768 + uKare * (320 - 175 * uKare)))
# B == B
B: float = (uKare / 1024) * (256 + uKare * (-128 + uKare * (74 - 47 * uKare)))
 
print(
    f"""
Beta1 değeri: {Beta1} 
Sigma1 değeri: {Sigma1} 
alfaEk değeri: {alfaEk} 
uKare değeri: {uKare}
A değeri: {A}
B değeri: {B}
"""
)
 
Sigma: float = S / (b * A)
IkiSigmaM = 2 * Sigma1 + Sigma
 
print(f"Sigma: {Sigma}")
 
def find_dSigma(sigma) -> float:
 
    IkiSigmaM = 2 * Sigma1 + sigma
 
    p1 = B * sin(sigma)
    p2 = cos(IkiSigmaM)
    p3 = 1 / 4 * B
    p4_1 = cos(sigma) * (-1 + 2 * (cos(IkiSigmaM) ** 2))
    p4_2 = (
        (1 / 6 * B)
        * cos(IkiSigmaM)
        * (-3 + (4 * sin(sigma) ** 2))
        * (-3 + (4 * cos(IkiSigmaM) ** 2))
    )
 
    return p1 * (p2 + p3 * (p4_1 - p4_2))

"""
∆σ parametresi, σ başlangıç değeri,
σ = S / (b * A)
alınarak, ∆σ parametresindeki değişim 10-14
değerinden küçük oluncaya iteratif olarak
aşağıdaki bağıntılarla hesaplanır.

"""

tol = pow(10.0, -14.0)
print("\n\n##### DONGU BASLADI #####\n\n")
i = 0
 
dSigma = find_dSigma(Sigma)
SigmaLoop = Sigma
 
while True:
    temp = SigmaLoop
    dSigma = find_dSigma(SigmaLoop)
    SigmaLoop = (S / (b * A)) + dSigma
    IkiSigmaM = 2 * Sigma1 + SigmaLoop
    diff = temp - SigmaLoop
 
    print(
        f"cos2SigmaM: {cos(IkiSigmaM)} # Dsigma: {dSigma} # Sigma: {SigmaLoop:.25f} # Diff: {diff:.20f}"
    )
 
    if diff < tol:
        break
    # ikisigma - dsigma - sigma

print("===================================================")
# Döngüden çıktıktan sonra diğerlerini hesaplar ve yazdırır.
# C 
C: float = f / 16 * ((cos(alfaEk) ** 2) * (4 + f * (4 - 3 * (cos(alfaEk) ** 2))))
print(f"C: {C}")
# dom 
dom: float = atan((sin(Sigma) * sin(alfa1)) / (cos(Beta1) * cos(Sigma)-sin(Beta1) * sin(Sigma) * cos(alfa1)))
print(f"dom: {dom}")
# dlon
dlon: float = dom - (1-C) * f * sin(alfa1) * (Sigma + C * sin(Sigma) * (cos(IkiSigmaM) + C * cos(Sigma) * (-1 + 2 * (cos(IkiSigmaM) ** 2))))
print(f"dlon: {dlon}")
# Enlem
Enlem: float = atan((sin(Beta1) * cos(Sigma) + cos(Beta1) * sin(Sigma) * cos(alfa1)) / ((1 - f) * ((sin(alfa1) ** 2) + sin(Beta1) * sin(Sigma) - cos(Beta1) * cos(Sigma) * cos(alfa1) ** 2) ** 1/ 2))
print(f"Enlem: {Enlem}")
# Boylam
Boylam: float = atan((sin(Sigma) * sin(alfa1)) / cos(Beta1) * cos(Sigma) - sin(Beta1) * sin(Sigma) * cos(alfa1))
print(f"Boylam: {Boylam}")
# azimutIki == alfa2
alfa2: float = atan(sin(alfaEk) / (-sin(Beta1) * sin(Sigma) + cos(Beta1) * cos(Sigma) * cos(alfa1)))
print(f"alfa2: {alfa2}")