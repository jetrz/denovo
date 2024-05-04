import subprocess
import matplotlib.pyplot as plt
import seaborn as sns

def main(id):
    print("\n########## RUNNING FOR ID:", id, "##########\n")

    res = subprocess.run(
        ["seqkit", "stats", f"code/datasets/misc/{id}.fastq"],
        capture_output=True,
        text=True
    )
    res = res.stdout.split('\n')
    labels, values = res[0].split(), res[1].split()

    nReads, nBases = values[labels.index('num_seqs',)], values[labels.index('sum_len')]
    print("nReads:", nReads, "| nBases:", nBases)

    res = subprocess.run(
        ["seqkit", "sample", "code/datasets/misc/SRR12801740.fastq", "-n", "5000"],
        capture_output=True,
        text=True
    )
    res = res.stdout.split('\n')
    lengths = [int(s.split('=')[1]) for s in res if 'length=' in s]
    sns.histplot(lengths, bins=100)
    plt.show()

    return

if __name__ == "__main__":
    for i in ["SRR12801740", "SRR11434954"]:
        main(i)

