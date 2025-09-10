# LogicTree: Structured Proof Exploration for Coherent and Rigorous Logical Reasoning with Large Language Models

<div align="center">

[![EMNLP-Published](https://img.shields.io/badge/EMNLP-Published-green)](https://arxiv.org/pdf/2504.14089)
[![arXiv](https://img.shields.io/badge/arXiv-2504.14089-red)](https://arxiv.org/abs/2504.14089)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/downloads/release/python-390/)

</div>

This is the implementation of the paper __LogicTree: Structured Proof Exploration for Coherent and Rigorous Logical Reasoning with Large Language Models__, published in EMNLP 2025 Main Conference.

__LogicTree__ is a modular framework that leverages test-time scaling to strengthen LLM reasoning. 

__Main contributions:__
- Algorithm-guided tree search for structured reasoning.
- Knowledge caching to reuse past reasoning and prevent redundancy.
- Search optimization to simplify combinatorial search into linear process.

<p align="center">
  <img src="overview.png" alt="overview" />
</p>

## Setup

1. Set up [OpenAI API key](https://platform.openai.com/docs/overview) and store it in the environment variable `OPENAI_API_KEY`  (in [`run.py`](run.py#L15)).

2. To run our code, please install all the packages by using the following command:
```
pip install -r requirement.txt
```

3. Our LLM prompting implementations are built upon the open-source contributions from [Microsoft Guidance](https://github.com/guidance-ai/guidance).

