import subprocess
import matplotlib.pyplot as plt
import seaborn as sns

REFERENCE_LEN = None

def set_reference():
    res = subprocess.run(
        ["seqkit", "stats", f"datasets/misc/ref.fna"],
        capture_output=True,
        text=True
    )
    res = res.stdout.split('\n')
    labels, values = res[0].split(), res[1].split()
    nBases = values[labels.index('sum_len')]
    global REFERENCE_LEN
    REFERENCE_LEN = int(nBases.replace(",",""))
    print("REFERENCE_LEN:", REFERENCE_LEN)

def assignment1(id):
    res = subprocess.run(
        ["seqkit", "stats", f"datasets/{id}/{id}.fastq"],
        capture_output=True,
        text=True
    )
    res = res.stdout.split('\n')
    labels, values = res[0].split(), res[1].split()

    nReads, nBases = values[labels.index('num_seqs',)], values[labels.index('sum_len')]
    coverage = int(nBases.replace(",",""))/REFERENCE_LEN
    print("nReads:", nReads, "| nBases:", nBases, "| Coverage:", coverage)

    res = subprocess.run(
        ["seqkit", "sample", f"datasets/{id}/{id}.fastq", "-p", str(50/coverage)],
        capture_output=True,
        text=True
    )
    res = res.stdout.split('\n')
    lengths = [int(s.split('=')[1]) for s in res if 'length=' in s]
    sns.histplot(lengths)
    plt.savefig(f"static/graphs/{id}_read_length_hist.png")

    return

def assignment2(id, nThreads=10, reffile="datasets/misc/ref.fna"):
    with open(f"datasets/{id}/subsample_50_{id}.fastq", 'w') as f, open(f"datasets/{id}/raven_subsample_50_{id}.fasta", 'w') as output:
        subprocess.run(
            ["raven", "--threads", f"{nThreads}", f.name], 
            stdout=output
        )
    print("raven conversion done")

    with open(f"datasets/{id}/raven_subsample_50_{id}.fasta", 'w') as f, open(f"datasets/{id}/minigraph_subsample_50_{id}.paf", 'w') as output:
        res = subprocess.run(
            ["minigraph", "-xasm", "-K1.9g", "--show-unmap=yes", "-t", f"{nThreads}", reffile, f.name], 
            stdout=output
        )
        print(res)

    res = subprocess.run(
        ["paftools.js", "asmstat", reffile+".fai", "--showunmap=yes", "-t", f"{nThreads}", reffile, f"datasets/{id}/minigraph_subsample_50_{id}.paf"],
        capture_output=True,
        text=True
    )
    print(res)

if __name__ == "__main__":
    set_reference()

    for i in ["SRR11434954"]:
        print("\n########## RUNNING FOR ID:", i, "##########\n")
        assignment1(i)

