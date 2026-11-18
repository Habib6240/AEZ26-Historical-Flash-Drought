import numpy as np
a=6378137.0; f=1/298.257223563; b=a*(1-f); e2=f*(2-f); ep2=e2/(1-e2)
def vincenty(l1,p1,l2,p2):
    U1=np.arctan((1-f)*np.tan(np.radians(p1)));U2=np.arctan((1-f)*np.tan(np.radians(p2)))
    L=np.radians(l2-l1);lam=L.copy() if hasattr(L,'copy') else L
    for _ in range(100):
        sS=np.sqrt((np.cos(U2)*np.sin(lam))**2+(np.cos(U1)*np.sin(U2)-np.sin(U1)*np.cos(U2)*np.cos(lam))**2)
        cS=np.sin(U1)*np.sin(U2)+np.cos(U1)*np.cos(U2)*np.cos(lam); sig=np.arctan2(sS,cS)
        sa=np.cos(U1)*np.cos(U2)*np.sin(lam)/np.where(sS==0,1,sS); c2a=1-sa**2
        c2m=np.where(c2a==0,0,cS-2*np.sin(U1)*np.sin(U2)/np.where(c2a==0,1,c2a))
        C=f/16*c2a*(4+f*(4-3*c2a)); lam_new=L+(1-C)*f*sa*(sig+C*sS*(c2m+C*cS*(-1+2*c2m**2)))
        if np.all(np.abs(lam_new-lam)<1e-13): lam=lam_new;break
        lam=lam_new
    u2=c2a*(a*a-b*b)/(b*b);A=1+u2/16384*(4096+u2*(-768+u2*(320-175*u2)));B=u2/1024*(256+u2*(-128+u2*(74-47*u2)))
    ds=B*sS*(c2m+B/4*(cS*(-1+2*c2m**2)-B/6*c2m*(-3+4*sS**2)*(-3+4*c2m**2)))
    return b*A*(sig-ds)
def perimeter_km(r): return vincenty(r[:-1,0],r[:-1,1],r[1:,0],r[1:,1]).sum()/1000
# UTM (Kruger series, 6th order)
def utm(lon,lat,lon0,k0=0.9996,FE=500000.0,FN=0.0):
    n=f/(2-f); A=a/(1+n)*(1+n**2/4+n**4/64+n**6/256)
    al=[n/2-2*n**2/3+5*n**3/16+41*n**4/180-127*n**5/288+7891*n**6/37800,
        13*n**2/48-3*n**3/5+557*n**4/1440+281*n**5/630-1983433*n**6/1935360,
        61*n**3/240-103*n**4/140+15061*n**5/26880+167603*n**6/181440,
        49561*n**4/161280-179*n**5/168+6601661*n**6/7257600,
        34729*n**5/80640-3418889*n**6/1995840, 212378941*n**6/319334400]
    p=np.radians(lat);l=np.radians(lon-lon0)
    t=np.sinh(np.arctanh(np.sin(p))-2*np.sqrt(n)/(1+n)*np.arctanh(2*np.sqrt(n)/(1+n)*np.sin(p)))
    xi=np.arctan2(t,np.cos(l)); eta=np.arctanh(np.sin(l)/np.sqrt(1+t*t))
    x=xi.copy();y=eta.copy()
    for j,aj in enumerate(al,1):
        x=x+aj*np.sin(2*j*xi)*np.cosh(2*j*eta); y=y+aj*np.cos(2*j*xi)*np.sinh(2*j*eta)
    return FE+k0*A*y, FN+k0*A*x
def utm_scale_conv(lon,lat,lon0):
    p=np.radians(lat);l=np.radians(lon-lon0);return np.degrees(l*np.sin(p))  # approx convergence
