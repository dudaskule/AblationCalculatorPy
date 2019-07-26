import math
from sys import exit


LICENSE = '''



================================================================================
Copyright (c) 2019 Werkgroepmeteoren.nl

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
================================================================================



'''




README = '''



================================================================================
Ablation Calculator Python v1
================================================================================

The original program script written in BASIC was found on the Australian Space
Academy website: https://www.spaceacademy.net.au/watch/debris/metflite.htm

Consider checking out their website!

Note:
The website contains an error, the Zenith Angle in the example needs to be 0. NOT 45.

================================================================================

This Python program was converted to a UNIX executable using PyInstaller.
PyInstaller Website: https://www.pyinstaller.org

================================================================================

This program is available as a:
- .py script
- UNIX Executable

================================================================================



'''

print('')
print('')
print('')
print('Ablation Calculator Python v1')


def Main():
	print('')
	print('')
	print('')
	#input data
	imass = input('Initial Mass (kg): ')
	mdens = input('Density (kg/m^3): ')
	ivelk = input('Speed at Entry (km/s): ')
	zadeg = input('Zenith Angle (deg): ')

	imass = float(imass)
	mdens = float(mdens)
	ivelk = float(ivelk)
	zadeg = float(zadeg)

	#parameters
	pi = math.pi  	#You know me? Right? I am PI!!!!! One of the most famous numbers!!!
	dr = pi / 180	#degrees to radians
	Asf = 1.2		#meteoroid shape factor
	Le = 0.001		#luminous efficiency
	Dc = 1			#drag coefficient
	Htc = 0.15		#heat transfer coefficient
	Ha = 3000000	#heat of ablation (J/kg)

	#convert inputs
	mm = imass 					#current meteoroid mass (kg)
	mm = mm.real

	cza = math.cos(zadeg * dr)	#cosine of zenith angle
	cza = cza.real

	vel = ivelk * 1000			#current meteoroid velocity (m/s)
	vel = vel.real

	#loop values
	h = 150000		#starting height (m)
	t = 0			#time variable - initially zero seconds
	dt = 0.0001		#time step in seconds
	tprint = 1.5	#first print time (secs)

	print('')
	a = '  {:4}    {:6}   {:5}      {:5}   {:4}       {:6}'
	b = '  {:6}  {:6}   {:6}    {:6}   {:6}     {:6}' 
	print(a.format('TIME', 'HEIGHT', 'SPEED', 'DECEL', 'MASS', 'VISUAL'))
	print(b.format('(S)', '(KM)', '(KM/S)', '(M/S/S)', '(%)', 'MAG'))
	#f = '{:3.2f}    {:3.1f}     {:2.1f}    {:6.0f}   {:3.1f}     {:3.1f} {}' #format for table (OLD)
	f = '{:6.2f}    {:5.1f}     {:4.1f}    {:7.0f}   {:5.1f}     {:5.1f} {}'  #format for table (NEW)	

	while True:
		rho = 1.3 * math.exp(-h / 7000) #atmospheric density (kg/m^3) at height h km
		rho = float(rho.real)
		#now compute meteoroid deceleration and mass loss
		decl = Dc * Asf * rho * vel * vel / ((mm ** .33333) * (mdens ** .66667))
		decl = float(decl.real)
		
		ML = Htc * Asf * rho * vel * vel * vel * ((mm / mdens) ** .66667) / (2 * Ha)
		ML = float(ML.real)
		
		dv = decl * dt #velocity decrement = decleration * time_increment
		dv = float(dv.real)
		
		dm = ML * dt #mass decrement = mass_loss * time_increment
		dm = float(dm.real)
		
		t = t + dt #increment time
		t = float(t.real)
		
		h = h - vel * dt * cza #compute new height
		h = float(h.real)
		
		vel = vel - dv #new velocity
		vel = float(vel.real)
		
		mm = mm - dm #new mass
		mm = float(mm.real)
		
		Iv = .5 * Le * ML * vel * vel #visual power (watts)
		Iv = float(Iv.real)
		
		Mv = 6.8 - 2.5 * math.log(Iv * (100000 / h) ** 2) / 2.303 #visual magnitude
		Mv = float(Mv.real)
		
		fracmass = mm / imass #fractional mass remaining
		fracmass = fracmass.real

		if t > tprint: 					#print loop
			if Mv < 5:
				vis = 'vis'
			else:
				vis = ''				#is meteor visible

			print(f.format(t, h / 1000, vel / 1000, decl, fracmass * 100, Mv, vis))
			tprint = tprint + .5 #increment print time
			if vel < 1000:
				break
	Menu()

def Menu():
	print('')
	print('')
	Menu_Input = None
	while Menu_Input not in ("1", "2", "3"):
	    Menu_Input = input('''Choose an option:
[1]: Calculate
[2]: QUIT
[3]: Display README
[4]: Display LICENSE
>>> ''')
	    if Menu_Input == "1":
	         Main()
	    elif Menu_Input == "2":
	        print("Exiting...")
	        exit()
	    elif Menu_Input == "3":
	    	print(README)
	    elif Menu_Input == "4":
	    	print(LICENSE)
	    else:
	    	pass
	    

Menu()




