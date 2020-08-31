import matplotlib.pyplot as plt
import csv

time = []
velocity_kmh = []
velocity_ms = []
with open('labdata.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    for row in reader:
        time.append(float(row[0]))
        velocity_kmh.append(float(row[1]))
        velocity_ms.append(float(row[2]))


#plot data
plt.figure()
plt.title('velocity (km/h) vs time (s)')
plt.xlabel('time (s)')
plt.ylabel('velocity (km/h)')
plt.scatter(time, velocity_kmh)
#plt.show()

plt.figure()
plt.title('velocity (m/s) vs time (s)')
plt.xlabel('time (s)')
plt.ylabel('velocity (m/s)')
plt.scatter(time, velocity_ms)
#plt.show()


# compute approximations for acceleration and displacement
acceleration = []
midpoint_time = []
displacement = []

trapezoidal_sum = 0
for i in range(len(velocity_ms) - 1):
    acceleration.append((velocity_ms[i+1] - velocity_ms[i]) / (time[i+1] - time[i]))
    midpoint_time.append((time[i] + time[i+1])/2)
    trapezoidal_sum += .5*(velocity_ms[i] + velocity_ms[i+1])*(time[i+1] - time[i])
    displacement.append(trapezoidal_sum)

#plot acceleration
plt.figure()
plt.title('acceleration (m/s^2) vs time (s)')
plt.xlabel('time (s)')
plt.ylabel('acceleration (m/s^2)')
plt.plot(midpoint_time, acceleration)
#plt.show()

#plot displacement
plt.figure()
plt.title('displacement (m) vs time (s)')
plt.xlabel('time (s)')
plt.ylabel('displacement (m)')
plt.scatter(midpoint_time, displacement)

plt.show()
