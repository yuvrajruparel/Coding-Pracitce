# Lab 6: GenAI

## Overview

In this lab, you will use generative AI as a tool to write, edit, and understand code to accomplish a new task: animating a plot. Specifically, you will work with DukeGPT to produce a program that can plot and animate the trajectory of a mass on a spring.

As you work through this lab, write your answers to the reflection questions in the provided file `report.md`.

## Learning Outcomes

The goal of this lab is to understand how to use generative AI models and large language models as a **tool** to assist you with programing.

Big questions this lab will help you answer:

- How can I prompt an LLM to generate code that solves a problem?
- What are some strengths and weakness of an LLM for generating code?
- How can I edit and understand code when authoring it in collaboration with genAI?

## Collaboration Policy

This lab is intended to be collaborative. You are encouraged to ask questions of classmates and compare results. However, your submission must only include code you have generated and edited. You may not copy another person's code.

The reflection component of this assignment is individual.

### AI Policy

**Code allowable use: AI Collaboration**  
AI should be used to generate the *first version* of code and may be used to improve its functionality. You are responsible for critically evaluating the result, ensuring it works, commenting the code to show your understanding, and making the requested edits yourself.

**Reflection allowable use: AI-assisted editing**  
AI can be used to make improvements to the clarity or quality of your reflection. In this assignment, that means that answering the reflection questions must be done by you. You may (but do not have to) use AI to help you edit the language for the ideas you yourself came up with.

## Instructions

### Part 1: Writing Code with GenAI

**Prompt**  
Suppose you were studying a common dynamical system—a mass on a spring.

Using DukeGPT, prompt for Python code that generates two animated plots of an object as it is dropped while being attached to a spring.

- Visualization of the object moving over time.
- The displacement of the spring over time.

The plots should be saved in the gif format.

**Fix**  

1. Paste the generated code in a file named `mass_spring_generated.py`.
2. Try to run the code (in VS Code). 
3. If there are errors, in the LLM output, highlight the line where the error arose, and prompt that that line has an error, and include the name and description of the error.
4. If further prompting does not result in working code, feel free to fix it yourself.

**Reflect**  

1. How many prompts did you have to exchange with the LLM? Did the code it provided work well in the first attempt, or did you need to interface with the LLM to get the desired output? 
2. Was there anything that the LLM struggled with in particular? What did it do well? 
3. Note how the problem is not well defined. Did the LLM make assumptions? What weight did it assign to the object? What was the spring constant? etc. 
4. How did your results compare to those around you? Did your algorithms run and look the same? What about the visualization aspect? 

### Part 2: Understanding AI-Generated Code

A key part of working with AI models is that you should **never** accept what they provide without critically evaluating the result. 

**Explain**  
Read through the code it gave you. For the parts that you don't understand or are new to you, ask the model to replace or explain. Highlight the line in question, and choose either "ask" if you have a specific question or "explain" if you want an explanation.

**Comment**  
Make a copy of your working code file, and name it `mass_spring_commented.py`. Add comments to the code to explain what it does. You can use your own prior knowledge of programming, and you can ask the LLM to "explain" anything new. Make sure you understand the code well!

Some questions that might be relevant to answer:

- What class in matplotlib lets you animate a figure?
- What does the animating function need to do?
- What type does Axes.plot() return?

**Reflect**  

1. How complex was the original code? Did you understand most of it or did you have to prompt the LLM to explain/change the code in any way?
2. Often, these models will over complicate a problem, introducing errors. Is this something you noticed in your code?
3. What was one new thing you learned from examining the generated code?

### Part 3: Working with AI-Generated Code

**Edit**  
Copy your commented code into a new code file `mass_spring_edited.py`.

Now, without using GenAI, edit the code from the previous parts to change:

- the output file names to be `spring_mass_motion.gif` and `spring_mass_displacement.gif`
- the mass attached to the spring to 5 kg 
- the spring constant to 10 N/m
- the x- and y-axis limits to show the whole animation
- Plot marker color to a new color

**Reflect**  

1. What did you find difficult about working with code that was drafted by GenAI?
2. What prior knowledge did you rely on to make the suggested changes?

## Submission

Submit your lab by 

1) Pushing to your individual Git repository, and
2) Submitting to Gradescope with the GitLab option.

The lab should be organized:

```
├── lab6 
│   ├── README.md 
│   ├── report.md 
│   ├── spring_mass_generated.py
│   ├── spring_mass_commented.py
│   ├── spring_mass_edited.py
│   ├── spring_mass_motion.gif
│   ├── spring_mass_displacement.gif
```

The grader will look for files in a `lab6` directory with these exact file names!

## Acknowledgements

Lab developed by Rokas Dargis, Fall 2025.
