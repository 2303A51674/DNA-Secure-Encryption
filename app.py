# ================================
# STREAMLIT UI FOR DNA ENCRYPTION
# ================================

import streamlit as st
import random
import hashlib

# Fix randomness for demo
random.seed(42)

# -------------------------------
# DNA LOGIC (same as your system)
# -------------------------------

DNA_MAPS = [
    {'00': 'A', '01': 'T', '10': 'C', '11': 'G'},
    {'00': 'T', '01': 'A', '10': 'G', '11': 'C'},
    {'00': 'C', '01': 'G', '10': 'A', '11': 'T'},
]

DNA_BASES = ['A', 'T', 'C', 'G']


def text_to_binary(text):
    return ''.join(format(ord(c), '08b') for c in text)


def binary_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(c, 2)) for c in chars)


def encode_dna(binary, key_index):
    mapping = DNA_MAPS[key_index]
    return ''.join(mapping[binary[i:i+2]] for i in range(0, len(binary), 2))


def decode_dna(dna, key_index):
    mapping = DNA_MAPS[key_index]
    reverse_map = {v: k for k, v in mapping.items()}
    return ''.join(reverse_map[c] for c in dna)


def mutate_dna(dna, rate=0.2):
    dna_list = list(dna)
    mutation_info = []

    for i in range(len(dna_list)):
        if random.random() < rate:
            original = dna_list[i]
            choices = [b for b in DNA_BASES if b != original]
            dna_list[i] = random.choice(choices)
            mutation_info.append((i, original))

    return ''.join(dna_list), mutation_info


def reverse_mutation(dna, mutation_info):
    dna_list = list(dna)
    for pos, original in mutation_info:
        dna_list[pos] = original
    return ''.join(dna_list)


def fragment_data(data):
    return [data[:len(data)//3], data[len(data)//3:2*len(data)//3], data[2*len(data)//3:]]


def reassemble_data(parts):
    return ''.join(parts)


# -------------------------------
# AIS SYSTEM
# -------------------------------

class AIS:
    def __init__(self):
        self.normal = set()

    def profile(self, user):
        return hashlib.sha256(user.encode()).hexdigest()

    def train(self, user):
        self.normal.add(self.profile(user))

    def detect(self, user):
        return "NORMAL" if self.profile(user) in self.normal else "ANOMALY"


ais = AIS()
ais.train("user_1")


# -------------------------------
# STREAMLIT UI
# -------------------------------

st.set_page_config(page_title="DNA Secure Storage", layout="centered")

# 🎨 Light UI Styling
st.markdown("""
    <style>
    body {
        background-color: #f9fafb;
    }
    .main {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧬 Secure DNA Data Encryption System")
st.subheader("Patent Demonstration Interface")

# Input
text = st.text_input("Enter Text", "HelloWorld")
user = st.text_input("User Behavior Pattern", "user_1")

# Buttons
col1, col2 = st.columns(2)

if "data" not in st.session_state:
    st.session_state.data = None

# -------------------------------
# ENCRYPT BUTTON
# -------------------------------
if col1.button("🔐 Encrypt"):

    status = ais.detect(user)

    binary = text_to_binary(text)
    key = random.randint(0, 2)

    dna = encode_dna(binary, key)
    mutated, mutation_info = mutate_dna(dna)
    fragments = fragment_data(mutated)

    st.session_state.data = {
        "dna": dna,
        "mutated": mutated,
        "fragments": fragments,
        "mutation_info": mutation_info,
        "key": key
    }

    st.success("Encryption Successful!")

    st.write("### 🧬 DNA Encoding")
    st.code(dna)

    st.write("### 🔐 Mutated DNA")
    st.code(mutated)

    st.write("### 🧩 Fragments")
    st.write(fragments)

    st.write("### 🛡️ AIS Status")
    st.info(status)


# -------------------------------
# DECRYPT BUTTON
# -------------------------------
if col2.button("🔓 Decrypt"):

    if st.session_state.data:
        data = st.session_state.data

        dna = reassemble_data(data["fragments"])
        dna = reverse_mutation(dna, data["mutation_info"])
        binary = decode_dna(dna, data["key"])

        result = binary_to_text(binary)

        st.success("Decryption Successful!")
        st.write("### 📜 Original Text")
        st.code(result)
    else:
        st.warning("Please encrypt first!")