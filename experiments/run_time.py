import numpy as np
import matplotlib.pyplot as plt




if __name__ == "__main__":
    data = np.array([2.407400608062744,
            4.626215696334839,
            7.351660966873169,
             9.876850128173828,
            12.253459215164185,
            15.433239698410034,
            17.866211652755737,
             20.367679595947266])
    #print(data[:,])
    plt.title("Indexer Scaling")

    plt.plot(np.arange(200,1800,200),data, label='Indexing time for different Sample sizes',marker=".")
    plt.legend()
    plt.xlabel("#Samples")
    plt.ylabel("Indexing Time (s)")
    plt.show()
