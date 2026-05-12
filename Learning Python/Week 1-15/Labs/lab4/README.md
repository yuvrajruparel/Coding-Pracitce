# Lab 4: DNA Translation

## Overview

In this lab, you will write a program to read a sequence of DNA from a file and use a codon table to add amino acids to form a polypeptide chain. This will exercise your skills using top-down design, writing and testing functions, manipulating strings, and using lists to store and look up information.

If the biology domain for this is new to you, do not worry! Watch this [video on DNA translation](https://www.youtube.com/watch?v=bKIpDtJdK8Q).

## Collaboration Policy

This lab is intended to be collaborative. You are encouraged to ask questions of classmates and work through the math together. However, your submission must represent your own understanding of the assignment. You may not copy another person's code.

The reflection component of this assignment is individual.

## AI Policy

**Code allowable use: AI Tutor**  
AI can be used to answer questions a TA would be willing to answer. You may ask conceptual questions.

You may *not* use AI to generate code, either in part or wholesale.

**Reflection allowable use: AI-assisted editing**  
AI can be used to make improvements to the clarity or quality of your reflection. In this assignment, that means that answering the reflection questions must be done by you. You may (but do not have to) use AI to help you edit the language for the ideas you yourself came up with.

## Instructions

### Provided Files

We provide the test file `sample_short.txt`, which contains a sample coding strand, and a codon table in `translation_table.py`.

### Program Specifications

* Your code for this assignment should be in a Python file called `dna_translation.py`.
* In this file, write a program that will read a DNA sequence from a file, find the corresponding mRNA sequence, and determine the polypeptide chain, composed of amino acids, that it codes for.
* You are free to write one or several functions of your choice to read the DNA sequence from a file and find the mRNA sequence. Note that the provided DNA sequence may not be uppercase and is not the "template strand." That is, the mRNA you seek is the same as the input DNA with the thymine (T) bases swapped with uracil (U) bases.
* Write a function `translate` that has one parameter for the mRNA sequence to translate. This function should search for the first occurance of a start codon "AUG" and translate the section it starts to amino acids. Each codon maps to one amino acid, found in the provided translation table, where the 3D list is indexed by the first base, second base, then third base to find the amino acid. This function should build the polypeptide chain by creating a list of strings representing the three-letter short name for amino acids. The chain ends when a "Stop" codon is found. This function returns the list of amino acid strings as its answer.
* Write a function `translate_file` that puts together all of this functionality, such that it takes a filename as its parameter, calls each of your functions as needed, and prints the list returned by `translate`.
* When imported, your module should produce no output.
* When run as the main program, your program should call `translate_file` with the provided test file `sample_short.txt`.

## Submission

Recall from the course introduction that lab assignments are evaluated using specifications, the essential qualities your submission must have to be satisfactory. You can see all the specifications for this lab assignment in the rubric section of these instructions. Your submission must meet all of the specifications to receive credit. Submissions that are marked "Needs revisions" can be revised during the second submission window.

### What to Submit

The submission for this lab has two parts:

* Code (submit on Gradescope)
* Reflection (submit on Canvas)

#### Submit with GitLab

For this lab, you can choose between uploading your submission to Gradescope or using GitLab. To have Gradescope download files from your git repository, choose "Gitlab" as the submission type, and "Submit Project" for your individual git repository.

### Code

Submit your code on Gradescope, to the assignment of the same name. When the Gradescope autograder indicates you have passed all the test cases, you are done with the code part! If the autograder shows test cases that were not passed, enter these test cases into your program, and debug until you are satisfied.

### Reflection

Your reflection should answer the following questions in paragraph form, in 200–400 words:

* What was your process for devising the algorithm for the `translate` function?
* What challenges did you encounter in this lab?
* What role did collaboration play in your work?
* What new knowledge or skills did you acquire? (If not, describe how you applied your existing knowledge.)

*Reminder: the collaboration policy is that your reflection work is individual.* 
