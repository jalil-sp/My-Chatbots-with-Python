# Iteration 2

In this iteration, I completed the WordReductionBot, the MyReductionTFIDBot,
and the ADSReductionTFIDFBot. This was a very informational iteration as I learned a
lot of useful new techniques that can be implemented in chatbots. The scenario that
outlines all the bots created in this iteration is as follows: A user is coming to our chatbot
to learn if their device is compatible with remote video calling, if not our bot can assist in
the beginning stages of troubleshooting.

For the first bot of this iteration, WordReductionBot, I explored several different
ways to perform word reductions with the goal of getting closer to the actual meaning of
a request. For the reduction I learned about reducers, creating a reduction engine
object, and how to call the reduction inside the main function. I learned that I major
shortcoming of word reduction is that one must understand the problem well but also
when given multiple dependencies how is the order assigned, i.e. what is more
important to key on?

To address the shortcoming above, MyReductionTFIDBot was created. Here I
learned the usefulness of implementing TF-IDF(Term Frequency-Inverse Document
Frequency) to statistically find the document that matches the user’s message the best
and respond back with the corresponding response.

Next, through learning about ADS(Alternative Direct Syntax), I was able to take
commands from a grammar file that I created to do request pre-processing, word
reduction/replacement and post-processing rules of an input phrase before searching
for an appropriate response. I combined this knowledge with what I learned about TF-
IDF to create my ADSReductionTFIDBot. Through using ADS, the reduction can be taken
out of the coding realm and defined by business managers quickly and easily, however
using multiple ADS files will require several coding steps and any very specific
customization of phrases would require additional code.
