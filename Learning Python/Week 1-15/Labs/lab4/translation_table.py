# string contains bases in the order they reference in the table
RNA_BASES = 'UCAG'

# list of lists of lists representing the RNA codon table
# Find the amino acid that corresponds to a codon by indexing the table.
# e.g. GAU codon: G @ index 3, A @ index 2, U @ index 0, so
# RNA_CODON_TABLE[3][2][0] references 'Asp'
RNA_CODON_TABLE = [
    [['Phe', 'Phe', 'Leu', 'Leu'], ['Ser', 'Ser', 'Ser', 'Ser'], ['Tyr', 'Tyr', 'Stop', 'Stop'], ['Cys', 'Cys', 'Stop', 'Trp']], # U first letter
    [['Leu', 'Leu', 'Leu', 'Leu'], ['Pro', 'Pro', 'Pro', 'Pro'], ['His', 'His', 'Gln', 'Gln'], ['Arg', 'Arg', 'Arg', 'Arg']], # C first letter
    [['Ile', 'Ile', 'Ile', 'Met'], ['Thr', 'Thr', 'Thr', 'Thr'], ['Asn', 'Asn', 'Lys', 'Lys'], ['Ser', 'Ser', 'Arg', 'Arg']], # A first letter
    [['Val', 'Val', 'Val', 'Val'], ['Ala', 'Ala', 'Ala', 'Ala'], ['Asp', 'Asp', 'Glu', 'Glu'], ['Gly', 'Gly', 'Gly', 'Gly']], # G first letter
]
