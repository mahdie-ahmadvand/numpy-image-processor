import matplotlib
import numpy as np
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

#///////////////  نمودار خطی تابع سینوس

x = np.linspace(0,4* np.pi,200)
y = np.sin(x)
plt.figure(figsize=(8,4))
plt.plot(x,y,label="sin(x)",color="blue" , linewidth=2)
plt.title("نمودار تابع سینوس")
plt.xlabel("x")
plt.ylabel("sin(x)")
plt.legend()
plt.grid(True,linestyle="--",alpha=0.5)
plt.tight_layout()
plt.savefig("sine_plot.png",dpi=300)
plt.show()

#/////////////// نمودار میله ای

categories = ["A" , "B" , "C" , "D" , "E"]
values = [12 , 27 , 18 , 35 , 21]

rgb_color = [(0.2,0.4,0.7),(0.3,0.6,0.4),(0.8,0.3,0.3),(0.5,0.4,0.7),(0.8,0.7,0.4)]
plt.figure(figsize=(6,4))
plt.bar(categories,values,color=rgb_color,label="مقادیر")
plt.title("نمودار میله ای ساده")
plt.xlabel("دسته")
plt.ylabel(" مقدار ")
plt.legend()
plt.grid(axis="y", linestyle = "--", alpha=0.7 , color = (0.8,0.8,0.8))
plt.tight_layout()
plt.show()


#////////////////////  دو نمودار با هم

fig , axes = plt.subplots(1,2,figsize=(12,4))

axes[0].plot(x , np.cos(x) , label="cos(x)" , color=(0.1,0.6,0.3),linewidth=2)
axes[0].set_title("تابع کسینوس")
axes[0].set_xlabel("x")
axes[0].set_ylabel("cos(x)")
axes[0].legend()
axes[0].grid(True,linestyle="--",alpha=0.7, color = (0.8,0.8,0.8))


axes[1].plot(x, np.sin(x) * np.exp(-x/10) , label="میراشونده" , color = (0.8,0.2,0.2) , linewidth=2 )
axes[1].set_title("نوسان میرا شونده")
axes[1].set_xlabel("x")
axes[1].set_ylabel("دامنه")
axes[1].legend()
axes[1].grid(True,linestyle="--", alpha=0.7 , color = (0.8,0.8,0.8) )

plt.tight_layout()
plt.show()


