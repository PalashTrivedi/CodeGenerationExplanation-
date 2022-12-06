import os
import cohere
import streamlit as st
from streamlit_ace import st_ace


from dotenv import load_dotenv

load_dotenv()

API_KEY = "dmE81ptspfXXAsmVD8Q6BsDg4NFSZ4wvR2tFLUUn"
co = cohere.Client(API_KEY)


def open_files(filename):
    """Read a file and returns lines"""
    with open(filename, "r") as file:
        lines = file.read()
        return lines


def generate(prompt, max_tokens, temperature):
    response = co.generate(
        model="xlarge",
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        k=0,
        p=0.75,
        frequency_penalty=0,
        presence_penalty=0,
        stop_sequences=["--", "==", ".", "prompt", "Language", "completion", "\n\n"],
        return_likelihoods="NONE",
    )
    return response.generations[0].text


def explain(prompt, max_tokens, temperature):
    response = co.generate(
        model="xlarge",
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        k=0,
        p=0.75,
        frequency_penalty=0,
        presence_penalty=0,
        stop_sequences=["--", "==", ".", "prompt", "Language", "completion", "\n\n"],
        return_likelihoods="NONE",
    )
    return response.generations[0].text


st.title("<//Featuring code generation and explanation using Cohere//>")

TAB1, TAB2 = st.tabs(["Code Generation Playground", "Code Explanation Playground"])

with TAB1:

    # st.markdown("Generation pla")
    USER_INPUT = st.text_input(
        "Enter text prompt below",
        max_chars=100,
        placeholder="Write a code to print hello world.",
        key="123",
    )
    if st.button("Generate"):
        with st.spinner("Please wait"):
            if len(USER_INPUT) <= 10:
                st.error("The input should have more characters")
            else:
                PROMPT = open_files("./codegeneration.txt").replace(
                    "<<USER_INPUT>>", USER_INPUT
                )
                RESPONSE = (
                    generate(PROMPT, max_tokens=300, temperature=0.7)
                    .replace("--", "")
                    .replace("==", "")
                    .replace("completion", "")
                    .replace("Language", "")
                    .replace("prompt", "")
                )
                st_ace(
                    value=RESPONSE,
                    language="python",
                    height=320,
                    theme="chrome",
                    readonly=True,
                )


with TAB2:
    st.markdown("Enter code below...")
    TEXT = st.text_area(label="Code", height=320)
    if st.button("Explain"):
        with st.spinner("Please wait"):
            PROMPT = open_files("./codeexplain.txt").replace("<<USER_INPUT>>", TEXT)
            RESPONSE = (
                generate(PROMPT, max_tokens=300, temperature=0.7)
                .replace("--", "")
                .replace("==", "")
                .replace("completion", "")
                .replace("Language", "")
                .replace("prompt", "")
            )
            st.text_area(label="Explanation", value=RESPONSE, height=150)
